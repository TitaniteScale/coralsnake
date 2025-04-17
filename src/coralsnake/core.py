# src/coralsnake/core.py

import sys
from .parser import parse_dust_lines
from .materials import estimate_materials
from .printer import format_parsed_program, format_materials_list, format_execution_notes

def process_dust_file(filepath):
    """Reads, parses, analyzes, and formats the output for a .dust file."""
    try:
        with open(filepath) as f:
            # Read lines, strip trailing whitespace, handle basic cleaning
            lines = [ln.rstrip() for ln in f]
            # Further cleaning (remove empty, comments) could be done here or in parser
            # For now, assume parser handles it if needed by its logic.

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return None # Indicate failure
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

    # Parse the cleaned lines
    parsed_program = parse_dust_lines(lines)
    if parsed_program is None: # Check if parsing itself indicated failure (optional)
        print(f"Error: Failed to parse {filepath}. See syntax warnings.", file=sys.stderr)
        # Parsing already printed warnings, maybe return empty dict or specific error signal?
        return None # Or potentially return the partial program if useful

    # Estimate materials
    estimated_mats = estimate_materials(parsed_program)

    # Format the output sections
    parsed_output = format_parsed_program(parsed_program, filepath)
    materials_output = format_materials_list(estimated_mats)
    notes_output = format_execution_notes()

    # Combine and return the full output string
    full_output = f"{parsed_output}\n{materials_output}\n{notes_output}"
    return full_output 