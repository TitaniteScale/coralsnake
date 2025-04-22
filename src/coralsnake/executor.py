# Execution logic for .dust programs

def analyze_execution(parsed_program):
    """
    Returns a list of execution notes describing what would happen if the program ran.
    Handles parameterized functions and argument-passing.
    """
    notes = []
    functions = parsed_program.get('functions', {})
    # Show each function signature
    for fname, fdata in functions.items():
        params = fdata.get('params', [])
        steps = fdata.get('steps', [])
        param_str = ', '.join(params)
        notes.append(f"Function '{fname}({param_str})':")
        for step in steps:
            cmd = step.get('cmd')
            val = step.get('val')
            if cmd == 'call' and isinstance(val, dict):
                call_name = val.get('name')
                call_args = val.get('args', [])
                notes.append(f"  - call {call_name}({', '.join(call_args)})")
            else:
                notes.append(f"  - {cmd} {val}")
    if not notes:
        notes.append("No executable steps found in this program.")
    return notes