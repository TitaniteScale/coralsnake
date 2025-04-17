def format_parsed_program(parsed_program, filename):
    """Formats the parsed program structure and estimated materials into a string."""
    output_lines = []

    output_lines.append(f"\nBuild plan for `{filename}`")
    output_lines.append("Inputs : " + (", ".join(parsed_program['inputs']) if parsed_program['inputs'] else "None"))
    output_lines.append("Outputs: " + (", ".join(parsed_program['outputs']) if parsed_program['outputs'] else "None"))
    output_lines.append("Globals: " + (str(parsed_program['global_vars']) if parsed_program['global_vars'] else "{}"))

    for func_name, steps in parsed_program['functions'].items():
        output_lines.append(f"\nFunction `{func_name}` Parsed Steps:")
        step_num = 1
        if not steps:
            output_lines.append("  (No steps defined)")
            continue

        for step in steps: # Step is a dict
            command = step['cmd']
            value = step['val']
            indent = step['indent']
            line = step['line']

            indent_str = "  " * indent
            line_prefix = f"L{line:<3}"
            step_prefix = f"{step_num}."

            output = f"{line_prefix} {step_prefix:>3} {indent_str}"

            if command == 'activate':
                output += f"→ Power **{value}**"
            elif command == 'deactivate':
                output += f"→ Depower **{value}**"
            elif command == 'delay':
                output += f"⏲ Wait {value} ticks" # value is string (var or number)
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

            output_lines.append(output)
            step_num += 1

    return "\n".join(output_lines)

def format_execution_notes():
    """Returns standard execution notes."""
    notes = [
        "\n--- Execution Notes ---",
        "- This output shows the PARSED structure. Indentation indicates nesting.",
        "- Execution logic (loops, conditions, state, timing) is NOT implemented yet.",
        "- Block endings (e.g., end of 'if') are inferred by de-indentation but not explicitly marked."
    ]
    return "\n".join(notes)

def format_materials_list(materials):
    """Formats the list of estimated materials."""
    output_lines = ["\n--- Estimated Materials ---"]
    if materials:
        for mat in materials:
            output_lines.append(f"- {mat}")
    else:
        output_lines.append("No components identified (empty or very simple program).")
    return "\n".join(output_lines) 