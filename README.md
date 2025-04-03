# Mordorlang

## Language Design and Implementation

#### University of Derby

# MordorLang Usage Instructions

Welcome to MordorLang! This guide explains the syntax, keywords, and usage for writing and running programs in MordorLang. The language supports standard programming constructs (variables, expressions, control flow) with a twist: you can use both standard and Black Speech keywords.

## Table of Contents

- [Getting Started](#getting-started)
- [Lexical Conventions](#lexical-conventions)
- [Basic Syntax](#basic-syntax)
- [Keywords and Their Black Speech Equivalents](#keywords-and-their-black-speech-equivalents)
- [Control Flow](#control-flow)
  - [If / Elif / Else Statements](#if--elif--else-statements)
  - [While Loops](#while-loops)
- [Block Structures](#block-structures)
- [Input/Output](#inputoutput)
- [Sample Program](#sample-program)
- [Running a MordorLang Program](#running-a-mordorlang-program)

## Getting Started

1. **Installation:**  
   Ensure you have a Python environment set up (MordorLang is implemented in Python). Clone the repository and install any dependencies as needed.

2. **Files Overview:**  
   - **Lexer:** Converts your source code into tokens, including handling both standard and Black Speech keywords.
   - **Parser:** Builds an Abstract Syntax Tree (AST) from the tokens.
   - **Interpreter:** Walks the AST, managing environments, executing statements, and handling function calls.

## Lexical Conventions

- **Tokens:** The language recognizes numbers, strings (delimited by double quotes), identifiers, and special symbols (such as `=`, `+`, `-`, etc.).
- **Comments:** (If implemented, add instructions here – if not, state that comments are not supported.)

## Basic Syntax

- **Statements:** Each statement ends with a semicolon (`;`).
- **Expressions:** Support arithmetic operations (`+`, `-`, `*`, `/`), comparisons, and logical operations.
- **Variables:** Declare and assign variables with the `=` operator. For example:  
  ```mordor
  orcs = 0;
  ```

## Keywords and Their Black Speech Equivalents

You can use either the standard keywords or their Black Speech alternatives. For example:

| Standard  | Black Speech |
| --------- | ------------ |
| if        | gul          |
| elif      | guulnakh     |
| else      | skai         |
| while     | arburz       |
| print     | krimp        |
| return    | zagh         |
| and       | agh          |
| or        | urz          |

Feel free to mix and match as desired.

## Control Flow

### If / Elif / Else Statements

The conditional construct supports both single-statement bodies and block structures. The syntax can be written with or without parentheses around the condition.

**Example using Black Speech:**

```mordor
gul (orcs == 10000) {
    krimp("Orcs have reached their full might!");
} gul-nakh (humans == 10000) {
    krimp("It's a draw!");
} skai {
    krimp("Humans are winning!");
};
```

### While Loops

A `while` loop (or `arburz` in Black Speech) repeats the block of code as long as its condition evaluates to true.

**Example:**

```mordor
arburz (orcs < 10000) {
    orcs = orcs + 1;
    krimp("Total orcs = " + orcs);
};
```

## Block Structures

- **Blocks:** Multiple statements can be grouped inside braces `{ ... }`.  
- **Scoping:** A new block creates a new environment. Assignments within a block update the global variable if it already exists in an outer scope (thanks to the modified assignment method).


## Input/Output

- **Printing:** Use `print` or its Black Speech alias `krimp` to output values.  
  ```mordor
  krimp("Hello, MordorLang!");
  ```

## Sample Program

Below is a sample program using Black Speech keywords. This example demonstrates variable assignments, a while loop, and nested if/elif/else blocks:

```mordor
orcs = 0;
humans = 1900;
krimp("We begin with " + orcs + " orcs");

arburz (orcs < 10000) {
    orcs = orcs + 1;
    gul (orcs == 10000) {
        krimp("We have an Orc army worthy of the Eye! orcs = " + orcs);
        gul (humans > 10000) {
            krimp("Humans Beat Orcs");
        } gul-nakh (humans == 10000) {
            krimp("It's a draw!");
        } skai {
            arburz (humans < 10001) {
                humans = humans + 1;
            }
        };

        gul (humans > orcs) {
            krimp("Forth Egorlas!");
            krimp("Humanity Wins");
        };
    }
};
```

## Running a MordorLang Program

1. **Write Your Program:**  
   Create a file (e.g., `example.mordor`) and write your MordorLang code in it.

2. **Run the Interpreter:**  
   Execute your program using the provided main script. For example, in your terminal:  
   ```bash
   python main.py ./examples/example.mordor
   ```
   The interpreter will lex, parse, and execute your code accordingly.

3. **Troubleshooting:**  
   If variables do not seem to update correctly, remember that block scopes create new environments. The interpreter’s assignment logic has been designed to update variables in the parent environment if they exist.  
   
Happy coding in MordorLang!

---

This document serves as a guide for both new users and developers looking to understand and work with MordorLang. Feel free to expand these instructions as you add new features or improvements.