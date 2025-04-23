# CoralSnake Syntax Reference

This file provides an overview of the syntax used in CoralSnake `.dust` scripts. It is intended as a quick-access reference for developers.

## File Type
`.dust` — CoralSnake source files

## Comments
```dust
# Anything after `#` is ignored (full-line or end-of-line comments)
```

<details>
<summary><strong>Imports</strong></summary>

```dust
import "<relative/path/to/file.dust>"
# Inline another .dust file; supports nested imports, error on circular import
```
</details>

<details>
<summary><strong>Top-Level Declarations</strong></summary>

```dust
input <name>[, <name>…]        # Declare one or more input signals
output <name>[, <name>…]       # Declare one or more output signals
var <name> [= <initial_value>] # Declare global variables (optional initial value)
```
</details>

<details>
<summary><strong>Top-Level Calls</strong></summary>

```dust
call <function_name>(<expr>[, <expr>…])  # Execute a function at script entry
```
</details>

<details>
<summary><strong>Function Definitions</strong></summary>

```dust
def <snake_case_identifier>([<param>[, <param>…]]):
    # Define a function with zero or more parameters
    # Function body is indented statements
```
</details>

<details>
<summary><strong>Statements (Inside Functions)</strong></summary>

### Control Flow
```dust
if <boolean expression>:
    # Execute indented block if true
else:
    # Execute indented block if the `if` condition was false
while <boolean expression>:
    # Repeat indented block while true
repeat <integer> times:
    # Repeat indented block N times
loop:
    # Infinite loop of the indented block
```

### Function Calls
```dust
call <function_name>([<expr>[, <expr>…]])  # Invoke another defined function
```

### Actions
```dust
activate(<output_name>)         # Turn an output ON
deactivate(<output_name>)       # Turn an output OFF
delay(<expr>)                   # Pause execution for N ticks
pulse(<output_name>, <integer>) # Activate, wait, then deactivate
```

### State Manipulation
```dust
set <name> = <value>            # Assign a value to a variable
```
</details>

<details>
<summary><strong>Expressions</strong></summary>

```dust
<expr> ::= <name> | <integer> | "<string>"
         | not <expr>
         | <expr> and <expr>
         | <expr> or <expr>
         | <expr> == <expr> | <expr> != <expr>
         | <expr> > <expr> | <expr> < <expr>
         | <expr> >= <expr> | <expr> <= <expr>
```
</details>

<details>
<summary><strong>Notes</strong></summary>

- Indentation **must** use 4 spaces; it is significant for block structure.
- Top-level `call` statements are grouped into an implicit `__main__` function when parsing.
- `else:` is supported immediately after an `if` block; `elif` is not yet implemented.
- The `wait until <expr>` syntax is currently not implemented.
- Parameterized functions and argument passing allow for reusable standard libraries (e.g., logic gates).
- Execution notes (via `analyze_execution`) display function signatures and call arguments but do not yet simulate full state/timing.
</details>
