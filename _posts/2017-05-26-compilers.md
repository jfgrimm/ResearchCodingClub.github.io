---
layout: post
title: Compilers
author: Peter Hill
---

We often treat compilers as a bit of a black-box, without really
understanding what it is they are doing. Today, I will take a brief
tour through the different parts of a compiler to hopefully demystify
them somewhat.

# Compilers

- What is a compiler?
- How does a compiler work?
- How to use a compiler
- Different compilers

# What is a compiler?

- Turns human-readable source code into machine-readable code
- May do optimisations of code to make it faster/more efficient


- First true compilers written in 1950s (Grace Hopper)
- First *self-hosting* compiler written in 1962 (Lisp, Tim Hart and Mike Levin)

- Most popular modern compilers written in C

# Interpreted vs compiled?

- Not really that much difference
- Languages can both be interpreted and compiled
    - Depends on implementation
- Compiled implementations turn human readable code “directly” into machine code (e.g. x86)
- Interpreted ones instead transform source into another form ("bytecode"), and a second program runs this form
- *Just in time* (JIT) compilation is essentially an interpreter that compiles the second form into machine code when run
- Interpreted languages often have a *REPL*: Read - eval(uate) - print loop
    - e.g. Python, MATLAB, Haskell

# Stages of compiling

## High level

- Preprocessing (only in some languages)
- Compilation
- Linking

## Preprocessing

- Only applies to some languages like C, C++, Fortran
- Expands text “macros”

# Stages of compiling

## Compilation

- Produces machine code (eventually)
- More details later
- Might have several stages

## Linking

- Takes output of compilation of one or more files
- Resolves references between files or to external libraries
- Assigns final memory addresses to functions, variables, etc.

# Actual phases of compiling

## Lexical analysis (lexer)

- Scan text and turn into tokens (tokenisation) 
    - e.g. keyword, type name, symbol
    - Attaches meaning to text
- Programming languages are typically *regular languages*
    - i.e. can be parsed with regular expressions or finite state machines

```
number = [ "-" ] digit {digit}*
digit = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
        
42 => (number 42)
57g => Error!
``` 

# Actual phases of compiling

## Syntax analysis (parser)

- Parses tokens, converting them to abstract syntax tree (AST)
    - Very similar to lexer, but operates on tokens rather than text
    - Attaches meaning to tokens
- Might be based on *context-free grammar* rather than regular expression
- Checks AST for syntactic validity (i.e. is it grammatical?)
    - Text might make sense for lexer, but tokens might not make sense together

```
add = number + number

(number 42) (symbol +) (number 2) => [add 42 2]
(number 57) (letter g) (number -12) => Error!
```

# Actual phases of compiling

## Semantic analysis

- Chuck out nonsense!
- Wrong type, missing or duplicate declaration, bad arguments
- Check names are in scope
- Generate symbol table
    - What does `add` mean?
    
```C
int foo = 42;     // Ok
int bar = "hello" // Error!
int foo;          // Error!
```

# Actual phases of compiling

## Intermediate code generation (intermediate representation, IR)

- Turn AST into lower-level form
- Allows decoupling of source language and machine code
    - Don't need to rewrite whole compiler for every new architecture or language!
    - Separate front-end and back-end
- Can apply optimisations to intermediate form
    - Replace expressions with equivalent, simpler form
    - Remove unreachable bits of code
    - Do more complicated optimisations

# Actual phases of compiling

## Code generation
- Generate actual machine code!
- Turns IR into specific machine code for a particular architecture (e.g. x86 or ARM)
    - Select appropriate instructions
- Order instructions in efficient way

# Real example - Hello world in C

## Source code

```C
#include <stdio.h>

int main() {
  printf("Hello world!\n");
  return 0;
}
```

## Save intermediate files

```bash
gcc -S -save-temps -masm=intel hello.c
```

# Real example - Hello world in C

## Preprocessed/Intermediate form

```C
# 1 "hello.c"
# 1 "<built-in>"
...
extern int printf (const char *__restrict __format, ...);
...
# 3 "hello.c"
int main() {
  printf("Hello world!\n");
  return 0;
}
```

# Real example - Hello world in C

## Assembly

```nasm
.LC0:
        .string "Hello world!"
...
main:
.LFB0:
        .cfi_startproc
...
        mov     edi, OFFSET FLAT:.LC0
        call    puts
        mov     eax, 0
```

# Basic use of gcc

```
# Separate compile and link steps
gcc -g -c file1.c -o file1.o
gcc -g -c file2.c -o file2.o
gcc -g -o executable file1.o file2.o -lexternal
---
# All-in-one
gcc -o executable file1.c file2.c -lexternal
```

- `-o` for output name
- `-c` for just compile, don't link
- `-l` for external libraries
- `-g` for including debug symbols

# Why use different compilers

- Good to use variety though, even if just for compiling and not for production
- Helps you stick to the standard ("portable code")
    - Implementations might have extensions, or even different behaviour
    - e.g. size of certain types, effects of "undefined behaviour"
    - Essential for running on different architectures
- Catch different errors, give different warnings
    - Not just outright bugs, but "suspicious" code too
- Do different optimisations
- Enable different tools
    - e.g. LLVM/Clang allow export of the AST, allowing refactoring tools, etc.

# Useful tools

## nm

- See symbols in object file/executable
- `nm hello.o`:

```
0000000000000000 T main
                 U puts
```

- `T`: in "text" (code) section
- `U`: undefined (or defined elsewhere)
- `D`: in "data" section (initialised data)

# Useful tools

## ldd

- See what libraries are dynamically linked
- `ldd hello`:

```
linux-vdso.so.1 =>  (0x00007fff31d8f000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f19a6c97000)
/lib64/ld-linux-x86-64.so.2 (0x000055fe86d83000)
```

- First and last are special libraries
    - `linux-vdso.so` is inserted by kernel for making system calls
    - `ld-linux-x86-64.so` is *program interpreter* used for actually running the program
- `libc` is C standard library, location of `printf`
