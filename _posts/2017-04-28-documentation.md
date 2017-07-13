---
layout: post
title: Documentation
subtitle: Helping future you
classoption: aspectratio=169
theme: York169dark
---

It happens to the best of us -- you come across some incomprehensible
code and wonder "who on earth wrote this?" only to discover it was
you, a mere six months ago. Writing documentation is one of those
tasks that often feels like a bit of a chore, but is a vital skill for
anyone writing software, and can help you avoid scenarios like the
above.

# Outline

- What is documentation?
- Why is documentation important?
- Types of documentation
- How to write documentation

# What is documentation?

## The Code Itself

- Function/variable names should be self-documenting (the **what**)

## Comments

- Inline with the source code
- Detail **why** something is done a particular way
- "Private" documentation, not generally seen by users, but useful for developers

## Documentation

- Usually "out of source", but can be inline
- Detail **what** something does, and **how** it does it
- "Public" documentation, seen by users

# Why is documentation important?

- Everybody hates trying to use undocumented code
    - Even worse trying to modify someone else's!
- Reduces time to get new users/developers up to speed
- Not just for other people, useful for you in six months
- Comments important to explain "magic"
- Can increase/mitigate "bus factor"
    - Number of people needed to be hit by a bus before the project dies
- Detail gotchas and (hidden) assumptions
- Pull in new users!
    - If they don't know what it does/how it works, how do they know it's what they want?

If it doesn't have documentation, no one knows how it works!

# Types of documentation

## The code itself

- Code should try and be as self-explanatory as possible
- Which is more understandable:

```python
def calc(d):
    ...
    return l, p
```

or

```python
def fft(signal):
    ...
    return frequency, phase
```


- Try to make names descriptive, rather than using symbols from equations
    - `n` versus `density`
- Don't needlessly abbreviate names
    - `indx` might be obvious, but `temp_denom`?
- Functions/subroutines should generally be verbs ("**do** thing"),
  variables should be nouns ("this is **a** thing")

# Types of documentation

## Comments

- Don't just repeat what the code does
    - The code should make that obvious already
- Do explain reasons for doing something

```python
    # Numpy doesn't normalise FFT
    frequency = rfft(signal)/len(signal)
```

- Do explain "magic"
    - The below is the famous "fast inverse square root" code from
    [Quake III](https://github.com/id-Software/Quake-III-Arena/blob/master/code/game/q_math.c#L552)

```c
float Q_rsqrt( float number )
{
	long i;
	float x2, y;
	const float threehalfs = 1.5F;

	x2 = number * 0.5F;
	y  = number;
	i  = * ( long * ) &y;                       // evil floating point bit level hacking
	i  = 0x5f3759df - ( i >> 1 );               // what the fuck? 
	y  = * ( float * ) &i;
	y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
//	y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration, this can be removed

	return y;
}
```

# Types of documentation

## README file

- Every project should have a README!
- Details what the code is _for_
    - Most web repos will render READMEs in pretty HTML
- Ideally also tells you how to get it up and running
    - How to get access
    - Where to download from
    - How to install (including dependencies!)
    - How to run tests/examples
- Signposts new users in directions of other sources of information
    - FAQ, papers, forums, etc.

# Types of documentation

## Full reference guide

- Documents every (!) function, class and global variable
- Usually quite technical, but if documenting "public API", might need
  to be more readable
- In-source/in-line documentation useful for this

## Tutorials

- Explain line-by-line a few simple examples
- Have a couple of different complexities
    - Simplest possible use vs more advanced use

# Types of documentation

## Help message

- If run from the command line, most users will expect `program --help` to output something useful
- Should display:
    - brief synopsis on what your program does
    - how to run your program
    - list of all command line options
- Python's builtin `argparse` module makes a lot of this easy
    - Similar tools for other languages, e.g. FLAP for Fortran
        - Good example of documentation too!

# Types of documentation

## Error message

- Error messages are documentation too!
- Be clear and unambiguous:
    - `ERROR: function call failed`
    - `ERROR: Couldn't calculate inverse Laplacian, input matrix singular (inverse.cpp: line 345)`

# How to write documentation

## Pick a simple format

- Markdown, reStructuredText are good examples
- Plain text files that can be compiled to other formats
    - This talk written in Markdown, compiled to PDF with pandoc
- Simple formatting allows you to focus on content
- Export to appropriate format (e.g. HTML for web, PDF for hard copy)

## Define your terms

- Most users are not likely to be experts
- Make sure to define terms when you first use them
- Preferably include a glossary

# How to write documentation

## "In source/line" documentation

- Document the function right at the function definition
- Easier to update the documentation when changing code
    - But still not automatic! Still needs effort to ensure it's in sync
- Some IDEs can display such documentation when e.g. hovering over function name
- Can have separate public/private documentation in header/source file (depending on language!)
- Not appropriate for everything
    - General overview, how separate pieces fit together, should usually be out of source

# How to write documentation

## Documentation builders

- Built in to some languages like Python:

```python
def foo(a, b):
"""
Foos a and b together, returning a list of the results
"""
```

- Tools exist for other languages, e.g. Doxygen, Ford

```cpp
//> Foos a and b together, returning a list of the results
std::list<result> foo(int a, int b) {
```

```fortran
!! Foos a and b together, returning a list of the results
function(a, b) result(list)
```

# How to write documentation

## Documentation builders

- Take the in-source docs and compile into e.g. LaTeX, PDF, HTML
    - HTML could then be put on your project website
    - Most allow LaTeX equations directly in text
- Readthedocs can build your documentation automatically when pushing to web repo (GitHub, Bitbucket, etc.)
    - Mainly designed for Python, but can be made to work with other languages too

# Summary

- Name things well
- Write a README
- Write inline documentation
- Keep it up-to-date
