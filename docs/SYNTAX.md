# Syntax Reference for CoralSnake

## File Suffix
.dust     # CoralSnake source files

## Comments
# Anything after `#` is ignored (full-line or end-of-line comments)

## Imports (Top-Level)
`import "<relative/path/to/file.dust>"`
# Inline another .dust file; supports nested imports, error on circular import

## Top-Level Declarations
`input <name>[, <name>…]`        # Declare one or more input signals
`output <name>[, <name>…]`       # Declare one or more output signals
`var <name> [= <initial_value>]` # Declare global variables (optional initial value)

## Top-Level Calls
`call <function_name>(<expr>[, <expr>…])`  # Execute a function at script entry

## Function Definitions
`def <snake_case_identifier>([<param>[, <param>…]]):`
    # Define a function with zero or more parameters
    # Function body is indented statements

## Statements (inside functions)

### Control Flow
`if <boolean expression>:`
    # Execute indented block if true
`else:`
    # Execute indented block if the `if` condition was false
`while <boolean expression>:`
    # Repeat indented block while true
`repeat <integer> times:`
    # Repeat indented block N times
`loop:`
    # Infinite loop of the indented block

### Function Calls
`call <function_name>([<expr>[, <expr>…]])`  # Invoke another defined function

### Actions
`activate(<output_name>)`         # Turn an output ON
`deactivate(<output_name>)`       # Turn an output OFF
`delay(<expr>)`                   # Pause execution for N ticks (`<expr>` is a variable or integer literal)
`pulse(<output_name>, <integer>)` # Activate output, wait N ticks, then deactivate

### State Manipulation
`set <name> = <value>`            # Assign a value (literal or variable) to a variable

## Expressions (Boolean and Values)
```
<expr> ::= <name> | <integer> | "<string>"        # Literals and variable names
         | not <expr>
         | <expr> and <expr>
         | <expr> or <expr>
         | <expr> == <expr> | <expr> != <expr>      # Equality
         | <expr> > <expr> | <expr> < <expr>        # Comparison
         | <expr> >= <expr> | <expr> <= <expr>
```

## Notes
- Indentation **must** use 4 spaces; it is significant for block structure.
- Top-level `call` statements are grouped into an implicit `__main__` function when parsing.
- `else:` is supported immediately after an `if` block; `elif` is not yet implemented.
- The `wait until <expr>` syntax is currently not implemented.
- Parameterized functions and argument passing allow for reusable standard libraries (e.g., logic gates).
- Execution notes (via `analyze_execution`) display function signatures and call arguments but do not yet simulate full state/timing.
