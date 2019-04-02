---
layout: post
title: Tests and testing
subtitle: Testing scientific codes - the basics
author: Peter Hill
tags: testing basics
---

Along with version control, tests are essential to good practice for
developing software. Having tests makes it easier to reason about
changes, and ensure trust in the outputs of your code. And if you
can't trust your code, you can't trust the papers written using the
results...

# Testing scientific code

- What are tests?
- Why are tests important?
- How to test your code
- Resources

# What are tests?

- You might already test
- Run a "standard" case, eyeball the result, check a number
- This is a test!

![exp_growth_test](/img/testing/exp_growth_test.png)

# What are tests?

## Types of test

- Integrated tests
    - Test whole program at once (or large chunks)
    - Most likely do something like this already
    - “Known good” answer (“regression test”)
- Unit tests
    - Test individual pieces (functions, subroutines, objects)
    - Useful as part of test driven development (TDD)

# Why are tests important?

- Code is wrong → wrong results → bad things happen
    - Need to be confident of results
    - Bugs are a fact of life
- How do you change code?
    - Either _"Edit and Pray"_ or _"Cover and Modify"_
- Proper tests will:
    - Catch common bugs
    - Catch edge cases
    - Catch errors early
    - Reduce time to solution
    - Allow you to make changes confidently

If it doesn’t have tests, it’s wrong!

# How to test

## What does good testing look like?

- Cover as much of the code as possible
- Each test should cover as little as possible (localisation)
- Should run fast! (“1/10 second is too slow”)
- Should be automated as much as possible
- Should run as often as possible
- Verification and validation
    - "Have we done the **thing** right?" vs "Have we done the **right** thing?"
    - Future topic!

# How to test

## How do I get started? Seems hard...

- Testing “legacy” code different to starting fresh
- No “one size fits all”
- Lots of guides on internet written for e.g. web development, enterprise systems, not scientific computing
- Exact method can be language dependent

# How to test

## Solutions
- _Working Effectively with Legacy Code_ - Michael C. Feathers
- Test driven development for new codes
- Integrated tests good start
- Lots of frameworks available for every language (cppunit, funit, pytest)
- Continuous integration tools (Travis CI, Jenkins)

# Getting started

![exp_growth_test](/img/testing/exp_growth_test.png)

```python
from numpy import isclose
from sys import exit

data = run_test_case()
answer = analyse_data(data)
real_answer = 0.24

if isclose(answer, real_answer):
    print("Test passed!")
    exit(0)
else:
    print("ERROR! Bad result")
    exit(1)
```

[/columns]

# Getting more tests in

## How to add tests to existing code?

- Add tests as you need to change things
- Find seams -- "places to alter code behaviour without editing in place"

## But I need to change the code in order to add a test in order to change the code?

1. Find change point
2. Find seam to insert test
3. Break dependencies
4. Write tests
5. Make changes

# Types of seams

## Preprocessor seam
- Redefine function with preprocessor macro

## Link seam
- Switch out function at link time

## Object seam
- Switch out object for testing ("fake") object

# Test driven development (TDD)

## Building your code around tests

- Write tests first
- Then write code!
    - Looks like more effort to begin with, but then always confident of results
- Write tests → Write simplest implementation → Debug/fix tests → Optimise
- Find bug → Write test → Fix bug → Run test

# Frameworks and Continuous Integration

## Frameworks

- Deal with setup and teardown between individual tests
- Run everything that e.g. looks like _test\_function_ in a file

## Continuous Integration

- Run on every commit/pull request
- Integrations into popular VCS websites (Travis CI)
    - Or run locally (Jenkins)
- No changes get into master/trunk without passing tests
- Run automatically, so no effort aside from initial setup

# Resources:

- _Working Effectively with Legacy Code_ - MC Feathers (ISBN: 9780131177055)
- _Software Engineering for Science_ - JC Carver, NP Chue Hong, GK Thiruvathukal (ISBN: 9781498743853)
- _Dealing with Risk in Scientific Software Development_ - R Sanders, D Kelly (IEEE Software, 25(4), July 2008)
- Python test frameworks: Pytest, nose, unittest
- C test frameworks: Check, CUnit, Autounit
- C++ test frameworks: Boost, Catch, CppUnit
- Fortran test frameworks: FRUIT, pFUnit, Ftnunit
- Continuous integration: Travis CI, Jenkins, GitLab CI

# Summary

## Good tests:

- Cover as much of the code as possible
- Each test should cover as little as possible (localisation)
- Should run fast! (“1/10 second is too slow”)
- Should be automated as much as possible
- Should run as often as possible

## 

- Write tests
- Automate them

