import re
import sys

def parse_dust_lines(lines):
    """Parses cleaned lines from a .dust file into a structured program dictionary."""
    parsed_program = {
        'inputs': [],
        'outputs': [],
        'global_vars': {},
        'functions': {} # function_name: {'params': [...], 'steps': [...]}
    }
    current_function = None
    current_params = []
    warnings = [] # Collect syntax warnings

    # --- Pass 1: Parse declarations and function structure ---
    for line_num, ln in enumerate(lines, 1): # Add line numbers for warnings
        stripped_ln = ln.strip()
        if not stripped_ln or stripped_ln.startswith("#"): # Skip empty lines/comments already
            continue

        leading_spaces = len(ln) - len(ln.lstrip(' '))
        current_indent = leading_spaces // 4 # Assuming 4-space indents

        # --- Top-Level Declarations ---
        if current_indent == 0:
            current_function = None # Exit function context if we de-indent to 0
            current_params = []
            if stripped_ln.startswith("input"):
                parsed_program['inputs'].extend([x.strip() for x in stripped_ln[5:].split(",")])
            elif stripped_ln.startswith("output"):
                parsed_program['outputs'].extend([x.strip() for x in stripped_ln[6:].split(",")])
            elif stripped_ln.startswith("var"):
                match = re.match(r"var\s+(\w+)\s*(?:=\s*(.*))?", stripped_ln)
                if match:
                    var_name, initial_value = match.groups()
                    parsed_program['global_vars'][var_name] = initial_value.strip() if initial_value else None
                else:
                    warnings.append(f"L{line_num}: Malformed var declaration: {ln}")
            elif stripped_ln.startswith("def"):
                match = re.match(r"def\s+(\w+)\s*\(([^)]*)\)\s*:", stripped_ln)
                if match:
                    current_function = match.group(1)
                    param_str = match.group(2).strip()
                    params = [p.strip() for p in param_str.split(",") if p.strip()] if param_str else []
                    current_params = params
                    if current_function in parsed_program['functions']:
                        warnings.append(f"L{line_num}: Warning - Redefining function '{current_function}'")
                    parsed_program['functions'][current_function] = {'params': params, 'steps': []}
                else:
                    warnings.append(f"L{line_num}: Malformed function definition: {ln}")
            elif stripped_ln.startswith("call"):
                # Top-level call statements go into an implicit __main__ function
                current_function = '__main__'
                if current_function not in parsed_program['functions']:
                    parsed_program['functions'][current_function] = {'params': [], 'steps': []}
                match_call = re.match(r"call\s+(\w+)\s*\(([^)]*)\)", stripped_ln)
                if match_call:
                    call_name = match_call.group(1)
                    arg_str = match_call.group(2).strip()
                    args = [a.strip() for a in arg_str.split(',') if a.strip()] if arg_str else []
                    parsed_program['functions'][current_function]['steps'].append({
                        'cmd': 'call', 'val': {'name': call_name, 'args': args},
                        'indent': 0, 'line': line_num
                    })
                else:
                    warnings.append(f"L{line_num}: Malformed call statement: {ln}")
            elif not any(stripped_ln.startswith(kw) for kw in ["input", "output", "var", "def", "call"]):
                warnings.append(f"L{line_num}: Unexpected statement outside function: {ln}")

        # --- Statements inside Functions ---
        elif current_function:
            # Ensure the function exists (might fail on malformed def)
            if current_function not in parsed_program['functions']:
                warnings.append(f"L{line_num}: Statement found, but not inside a valid function definition: {ln}")
                continue # Skip this line if the function context is broken

            steps_list = parsed_program['functions'][current_function]['steps']

            # Actions
            m_act = re.match(r"activate\((\w+)\)", stripped_ln)
            m_deact = re.match(r"deactivate\((\w+)\)", stripped_ln)
            m_delay = re.match(r"delay\((\w+)\)", stripped_ln) # Accepts variable or number string
            m_pulse = re.match(r"pulse\((\w+)\s*,\s*(\d+)\)", stripped_ln) # Duration must be number
            # State
            m_set = re.match(r"set\s+(\w+)\s*=\s*(.*)", stripped_ln)
            # Control Flow
            m_if = re.match(r"if\s+(.*):", stripped_ln)
            m_while = re.match(r"while\s+(.*):", stripped_ln)
            m_repeat = re.match(r"repeat\s+(\d+)\s+times:", stripped_ln)
            m_loop = re.match(r"loop:", stripped_ln)
            m_call = re.match(r"call\s+(\w+)\s*\(([^)]*)\)", stripped_ln)
            if m_call:
                call_name = m_call.group(1)
                arg_str = m_call.group(2).strip()
                args = [a.strip() for a in arg_str.split(",") if a.strip()] if arg_str else []
                steps_list.append({
                    'cmd': 'call',
                    'val': {'name': call_name, 'args': args},
                    'indent': current_indent,
                    'line': line_num
                })

            if stripped_ln == "else:":
                steps_list.append({'cmd': 'else', 'val': None, 'indent': current_indent, 'line': line_num})
            elif m_act:
                steps_list.append({'cmd': 'activate', 'val': m_act.group(1), 'indent': current_indent, 'line': line_num})
            elif m_deact:
                steps_list.append({'cmd': 'deactivate', 'val': m_deact.group(1), 'indent': current_indent, 'line': line_num})
            elif m_delay:
                steps_list.append({'cmd': 'delay', 'val': m_delay.group(1), 'indent': current_indent, 'line': line_num})
            elif m_pulse:
                steps_list.append({'cmd': 'pulse', 'val': (m_pulse.group(1), int(m_pulse.group(2))), 'indent': current_indent, 'line': line_num})
            elif m_set:
                steps_list.append({'cmd': 'set', 'val': (m_set.group(1), m_set.group(2).strip()), 'indent': current_indent, 'line': line_num})
            elif m_call:
                # Already handled above
                pass
            elif m_if:
                steps_list.append({'cmd': 'if_start', 'val': m_if.group(1), 'indent': current_indent, 'line': line_num})
            elif m_while:
                steps_list.append({'cmd': 'while_start', 'val': m_while.group(1), 'indent': current_indent, 'line': line_num})
            elif m_repeat:
                steps_list.append({'cmd': 'repeat_start', 'val': int(m_repeat.group(1)), 'indent': current_indent, 'line': line_num})
            elif m_loop:
                steps_list.append({'cmd': 'loop_start', 'val': None, 'indent': current_indent, 'line': line_num})
            else:
                warnings.append(f"L{line_num}: Unexpected statement: {ln}")

    # Optionally print syntax warnings
    for warning in warnings:
        print(f"Syntax Warning: {warning}", file=sys.stderr)

    return parsed_program