# CoralSnake 🐍

## A DSL for Minecraft Redstone

CoralSnake is a simple Domain Specific Language (DSL) designed to describe Redstone logic in Minecraft. The goal is to write `.dust` files using CoralSnake syntax, and eventually have an interpreter generate step-by-step build instructions or schematics for the described contraption.

## Current Status (v0.4 - Parser)

*   **Parsing:** The interpreter (`coral_interpreter.py`) can currently parse `.dust` files written using the defined syntax. It understands inputs, outputs, variables, function definitions, and various control flow/action statements (loops, conditions, delays, etc.).
*   **Structure Output:** Running the interpreter prints a structured view of the parsed program, showing indentation and the sequence of commands.
*   **Material Estimation:** The interpreter provides a basic estimate of the Redstone component types likely needed based on the commands used in the `.dust` file.
*   **Execution:** **Execution logic (handling loops, conditions, state changes, timing) is NOT YET IMPLEMENTED.** The interpreter only parses the structure at this stage.

## Syntax

The language syntax is defined in [`docs/SYNTAX.md`](docs/SYNTAX.md). It uses indentation for structure and aims for readability.

## Usage

To parse a CoralSnake file and see the parsed structure and estimated materials:

```bash
python coral.py <your_file.dust>
```

Example:
```bash
python coral.py examples/clock.dust
```

## Getting Started

To run the CoralSnake parser, make sure you have Python 3 installed. Then from your terminal:

1. Install Python:
   - Windows: Download and install from [Python.org](https://www.python.org/downloads/)
   - Mac: Use Homebrew: `brew install python3`
   - Linux: Python is usually pre-installed, or use: `sudo apt install python3`

2. Download CoralSnake:
   ```bash
   # Clone the repository
   git clone [REPO_URL]
   
   # Go into the project folder
   cd coralsnake
   ```

3. You're ready to run CoralSnake!


```bash
python3 coral.py your_file.dust
```

This will display the parsed structure and an estimate of Redstone components needed.

## VS Code Extension

CoralSnake has an official [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TitaniteScale.coralsnake) for syntax highlighting and language support.

## Icon

![CoralSnake Language Icon](assets/icon.png)


To install:
- Search for "CoralSnake" in the VS Code Extensions Marketplace, or
- Install directly using the `.vsix` if downloaded locally.

## Snippets

**Example Code (clock.dust):**
![The example illustrates clearly structured definitions for basic logical gates (AND, OR, XOR, NOT), demonstrating syntax highlighting and readability provided by the extension.](assets/code1.jpg)


```

**Interpreter Output:**
```
![Running coral.py to interpret examples/clock.dust shows the parsed structure and estimated materials needed](assets/output1.gif)


## Examples / Demos

Basic examples can be found in the `examples/` directory.

**(More detailed examples and demos demonstrating generated build instructions are planned for future versions!)**

## Future Work

*   Implement the execution engine to simulate the Redstone logic.
*   Develop the build instruction generation based on parsed and executed logic.
*   Potentially add support for schematic generation (.litematic, .schem).
*   Refine syntax and add more advanced Redstone concepts.

## License

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.
