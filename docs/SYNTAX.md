# File suffix
.dust     # source code written by humans

# Comments
# everything after # is ignored

# Top-level Declarations
input <name>[, <name>…]         # Declare input signals
output <name>[, <name>…]        # Declare output signals
var <name> [= <initial_value>] # Declare global state variables (optional initial value)

# Functions
def <snake_case_identifier>():
    # Statements go inside functions, indented

# Statements (inside functions)
# --- Control Flow ---
if <boolean expression>:        # Conditional execution
    # indented statements
# (Optional else/elif not specified yet)

loop:                           # Infinite loop
    # indented statements

repeat <integer> times:         # Loop N times
    # indented statements

while <boolean expression>:     # Loop while condition is true
    # indented statements

wait until <boolean expression> # Pause execution until condition is true

call <function_name>()          # Execute another defined function

# --- Actions ---
activate(<output_name>)         # Turn an output ON
deactivate(<output_name>)       # Turn an output OFF
delay(<ticks>)                  # Pause execution for N ticks
pulse(<output_name>, <ticks>)   # Activate, delay N ticks, then deactivate

# --- State Manipulation ---
set <name> = <value>            # Assign a value to a variable

# Boolean Grammar
<expr> ::= <name> | <integer> | <string> | # Literals and variable names
           not <expr> |
           <expr> and <expr> |
           <expr> or <expr> |
           <expr> == <expr> | <expr> != <expr> | # Comparisons
           <expr> > <expr> | <expr> < <expr> |
           <expr> >= <expr> | <expr> <= <expr>

# Notes:
# - Indentation is significant for defining blocks (if, loop, repeat, while, def).
# - Variable scope (global vs. local) is currently assumed global or function-level.
# - String/integer values are introduced for variables/set.

