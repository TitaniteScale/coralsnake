import os
import sys

def process_imports(filename, seen=None):
    """Read a .dust file, inline any import statements, and return the expanded lines."""
    if seen is None:
        seen = set()
    abs_path = os.path.abspath(filename)
    if abs_path in seen:
        raise RuntimeError(f"Circular import detected: {filename}")
    seen.add(abs_path)

    dirname = os.path.dirname(abs_path)
    expanded_lines = []
    with open(abs_path, 'r') as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith('import '):
                # Extract path between quotes
                import_path = stripped.split('import',1)[1].strip().strip('"').strip("'")
                import_abs = os.path.abspath(os.path.join(dirname, import_path))
                # Recursively process imports
                imported_lines = process_imports(import_abs, seen)
                expanded_lines.extend(imported_lines)
            else:
                expanded_lines.append(line)
    return expanded_lines

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/import.py <file.dust>")
        sys.exit(1)
    filename = sys.argv[1]
    try:
        expanded = process_imports(filename)
        print(''.join(expanded))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
