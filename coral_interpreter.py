#!/usr/bin/env python3
"""
CoralSnake Interpreter v0.3
Reads a .dust file and parses extended syntax including loops, vars, etc.
NOTE: Does not yet EXECUTE loops, conditions, or manage state.
"""

import sys, re

if len(sys.argv) < 2:
    print("Usage: python coral_interpreter.py <filename.dust>")
    sys.exit(1)

FILE = sys.argv[1]

inputs, outputs, variables = [], [], {}
# Structure: List of tuples (command, value, indent_level)
# Value can be simple (name, ticks) or complex (condition string, var details)
parsed_program = {
    'inputs': [],
    'outputs': [],
    'global_vars': {},
    'functions': {}
}
current_function = None

with open(FILE) as f:
    lines = [ln.rstrip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

# --- Pass 1: Parse declarations and function structure ---
indent_level = 0
for ln in lines:
    stripped_ln = ln.strip()
    leading_spaces = len(ln) - len(ln.lstrip(' '))
    current_indent = leading_spaces // 4 # Assuming 4-space indents

    # --- Top-Level Declarations ---
    if current_indent == 0:
        current_function = None # Exit function context if we de-indent to 0
        if stripped_ln.startswith("input"):
            parsed_program['inputs'].extend([x.strip() for x in stripped_ln[5:].split(",")])
        elif stripped_ln.startswith("output"):
            parsed_program['outputs'].extend([x.strip() for x in stripped_ln[6:].split(",")])
        elif stripped_ln.startswith("var"):
            match = re.match(r"var\s+(\w+)\s*(?:=\s*(.*))?", stripped_ln)
            if match:
                var_name, initial_value = match.groups()
                # Store initial value as string for now
                parsed_program['global_vars'][var_name] = initial_value.strip() if initial_value else None
        elif stripped_ln.startswith("def"):
            match = re.match(r"def\s+(\w+)\s*\(\s*\)\s*:", stripped_ln)
            if match:
                current_function = match.group(1)
                parsed_program['functions'][current_function] = [] # Initialize function step list
            else:
                print(f"Syntax warning: Malformed function definition: {ln}")
        elif stripped_ln: # Non-empty line at indent 0 that isn't a declaration
            print(f"Syntax warning: Unexpected statement outside function: {ln}")

    # --- Statements inside Functions ---
    elif current_function:
        steps_list = parsed_program['functions'][current_function]

        # Actions
        m_act = re.match(r"activate\((\w+)\)", stripped_ln)
        m_deact = re.match(r"deactivate\((\w+)\)", stripped_ln)
        m_delay = re.match(r"delay\((\w+)\)", stripped_ln)
        m_pulse = re.match(r"pulse\((\w+)\s*,\s*(\d+)\)", stripped_ln)
        # State
        m_set = re.match(r"set\s+(\w+)\s*=\s*(.*)", stripped_ln)
        # Control Flow
        m_call = re.match(r"call\s+(\w+)\s*\(\s*\)", stripped_ln)
        m_if = re.match(r"if\s+(.*):", stripped_ln)
        m_while = re.match(r"while\s+(.*):", stripped_ln)
        m_repeat = re.match(r"repeat\s+(\d+)\s+times:", stripped_ln)
        m_loop = re.match(r"loop:", stripped_ln)
        m_wait = re.match(r"wait\s+until\s+(.*)", stripped_ln)

        if m_act:
            steps_list.append(('activate', m_act.group(1), current_indent))
        elif m_deact:
            steps_list.append(('deactivate', m_deact.group(1), current_indent))
        elif m_delay:
            steps_list.append(('delay', m_delay.group(1), current_indent))
        elif m_pulse:
            steps_list.append(('pulse', (m_pulse.group(1), int(m_pulse.group(2))), current_indent))
        elif m_set:
            # Store value as string for now
            steps_list.append(('set', (m_set.group(1), m_set.group(2).strip()), current_indent))
        elif m_call:
            steps_list.append(('call', m_call.group(1), current_indent))
        elif m_if:
            # Store condition string
            steps_list.append(('if_start', m_if.group(1).strip(), current_indent))
        elif m_while:
            steps_list.append(('while_start', m_while.group(1).strip(), current_indent))
        elif m_repeat:
            steps_list.append(('repeat_start', int(m_repeat.group(1)), current_indent))
        elif m_loop:
            steps_list.append(('loop_start', None, current_indent))
        elif m_wait:
            steps_list.append(('wait', m_wait.group(1).strip(), current_indent))
        elif stripped_ln: # Catch other non-empty lines inside functions
             print(f"Syntax warning: Unrecognized statement in function '{current_function}': {ln}")

    elif stripped_ln: # Non-empty line outside function and not a declaration
        print(f"Syntax warning: Unexpected statement: {ln}")

# --- Function to Estimate Materials ---
def estimate_materials(program_data):
    """Analyzes parsed program data to suggest required Redstone component types."""
    materials = set()

    if program_data['inputs']:
        materials.add("Input Interface (e.g., Lever, Button)")
    if program_data['outputs']:
        materials.add("Output Interface (e.g., Lamp, Piston)")
        materials.add("Redstone Dust") # Outputs always need wiring

    if program_data['global_vars']:
        # Basic assumption: variables imply some form of memory
        materials.add("Memory Component (e.g., Latch, Counter)")
        materials.add("Redstone Dust")
        materials.add("Redstone Torch") # Torches often used in memory

    for func_name, steps in program_data['functions'].items():
        for command, value, indent in steps:
            if command in ['activate', 'deactivate']:
                materials.add("Redstone Dust")
            elif command in ['delay', 'pulse']:
                materials.add("Redstone Dust")
                materials.add("Repeater")
            elif command == 'set':
                # Setting variables reinforces the need for memory/logic
                materials.add("Memory Component (e.g., Latch, Counter)")
                materials.add("Redstone Dust")
                materials.add("Redstone Torch")
            elif command in ['if_start', 'while_start', 'wait']:
                # Conditions imply logic gates
                materials.add("Redstone Dust")
                materials.add("Comparator")
                materials.add("Redstone Torch")
            elif command in ['loop_start', 'repeat_start']:
                # Loops/repeats often need clocks or counters
                materials.add("Redstone Dust")
                materials.add("Repeater")
                materials.add("Redstone Torch")
            # 'call' doesn't directly map to a specific component type easily

    # Basic building blocks are almost always needed for anything non-trivial
    if materials: # Only add blocks if other components are present
         materials.add("Solid Building Blocks")

    return sorted(list(materials))

# --- Pass 2: Print Parsed Structure (No Execution Yet) ---
print(f"\nBuild plan for `{FILE}`")
print("Inputs :", ", ".join(parsed_program['inputs']))
print("Outputs:", ", ".join(parsed_program['outputs']))
print("Globals:", parsed_program['global_vars'])

for func_name, steps in parsed_program['functions'].items():
    print(f"\nFunction `{func_name}` Parsed Steps:")
    step_num = 1
    for command, value, indent in steps:
        indent_str = "  " * indent
        output = f"{step_num}. {indent_str}"
        if command == 'activate':
            output += f"→ Power **{value}**"
        elif command == 'deactivate':
            output += f"→ Depower **{value}**"
        elif command == 'delay':
            output += f"⏲ Wait {value} ticks"
        elif command == 'pulse':
            output += f"⚡ Pulse **{value[0]}** for {value[1]} ticks"
        elif command == 'set':
            output += f"≔ Set **{value[0]}** = {value[1]}"
        elif command == 'call':
            output += f"↳ Call function `{value}`"
        elif command == 'if_start':
            output += f"❓ If ({value}):"
        elif command == 'while_start':
            output += f"↺ While ({value}):"
        elif command == 'repeat_start':
            output += f"🔁 Repeat {value} times:"
        elif command == 'loop_start':
            output += f"🔄 Loop indefinitely:"
        elif command == 'wait':
            output += f"⏳ Wait until ({value})"
        else:
            output += f"Unknown command: {command} {value}" # Fallback
        print(output)
        step_num += 1

# --- Print Estimated Materials ---
estimated_mats = estimate_materials(parsed_program)
print("\n--- Estimated Materials ---")
if estimated_mats:
    for mat in estimated_mats:
        print(f"- {mat}")
else:
    print("No components identified (empty or very simple program).")

print("\n--- Execution Notes ---")
print("- This output shows the PARSED structure. Indentation indicates nesting.")
print("- Execution logic (loops, conditions, state, timing) is NOT implemented yet.")
print("- Block endings (e.g., end of 'if') are inferred by de-indentation but not explicitly marked.")

