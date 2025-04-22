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

    for func_name, fdata in program_data['functions'].items():
        # fdata has 'params' and 'steps'
        steps = fdata.get('steps', [])
        for step in steps:
            command = step.get('cmd')
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
                materials.add("Comparator") # Often used for signal strength/state checks
                materials.add("Redstone Torch") # Often used in logic gates
            elif command in ['loop_start', 'repeat_start']:
                # Loops/repeats often need clocks or counters
                materials.add("Redstone Dust")
                materials.add("Repeater") # Often used in clocks/timers
                materials.add("Redstone Torch") # Often used in clocks/counters
            # 'call' doesn't directly map to a specific component type easily

    # Basic building blocks are almost always needed for anything non-trivial
    if materials: # Only add blocks if other components are present
         materials.add("Solid Building Blocks")

    return sorted(list(materials)) 