---
layout: post
title: Test Driven Development
author: Peter Hill, Stephen Biggs-Fox
tags: testing practical basics
---

Testing your code is an essential part of good practice in software
development, but you sometimes hear that it takes too long to write
them therefore they're not worth the cost. Today, we talked about how
in reality, writing tests can actually speed up the time to results,
and how even writing the tests _first_ can lead to faster development
and more confident code.

# Introduction

![Image ref:
<https://usercontent2.hubstatic.com/8530569_f520.jpg>](/img/tdd_191113/coding-life.jpg)

# Outline

- Unit Testing
- Test Driven Development (TDD)
- Summary and Further Reading

# Unit Testing is a Safety Net

![](/img/tdd_191113/climbing.jpg)
Image ref:
<http://www.fitnessbin.com/wp-content/uploads/2015/12/Rock-Climbing-4.jpg>

Testing lets us write new code and modify existing code with
confidence, by catching bugs as soon as they're introduced.

# Unit Testing is a Safety Net

![](/img/tdd_191113/testing_pyramid.png)

Cheap, independent unit tests should form the base of our testing
frameworks, although we still need to test how individual pieces are
put together.

Given a big system with lots of pieces like the illustration below,
there are lots of places we could test. We could test the whole
program (highlighted in purple). We could test smaller components,
like those in pink. Or we could test the very smallest bits, like
those in green:

![](/img/tdd_191113/code-pics-04.png)

If we just have tests at the top level, when one of them goes wrong,
we may have no idea whereabouts in the big system the error is coming
from.

![](/img/tdd_191113/code-pics-06.png)

Whereas when testing individual units, if one of those tests go wrong,
we may be able to pinpoint the exact line with the error almost
immediately.

![](/img/tdd_191113/code-pics-08.png)

# Unit Testing is a Safety Net

## Summary

- Bugs are a fact of life
- Tests give you confidence in your code
- Unit tests pinpoint location of bugs
- Write more unit tests than full system tests

# Test Structure: Setup, Exercise, Assert

Let's start with a toy calculator module, `calculator.py`:

``` python
def add(lhs, rhs):
    "Adds the rhs to the lhs"
    return lhs + rhs
```

And a corresponding test in a separate file, `test_calculator.py`:

``` python
import calculator


def test_add_both_positive():
    # Setup
    a = 3
    b = 2
    # Specify expected result
    expected = 5
    # Exercise system under test
    actual = calculator.add(a, b)
    # Verify result
    assert actual == expected
```

Now we can run `pytest`:

```shell
$ pytest
======================== test session starts =========================
platform linux -- Python 3.7.3, pytest-5.2.2
rootdir: /home/peter/Documents/Physics_Coding_Club/191113_TDD/examples
collected 1 item

test_calculator.py .                                           [100%]

========================= 1 passed in 0.01s ==========================
```

- `pytest` is a Python test runner and framework
- Automagically finds and runs tests:
    - Files named `test_*.py` or `*_test.py`
    - Functions beginning with `test`
    - Classes beginning with `Test`
- Works with `assert` statements
- Fancier features like fixtures

<https://docs.pytest.org/>

# Installing `pytest`

## On Linux:

```bash
$ pip3 install --user pytest
```

or

```bash
$ conda install pytest
```

## On Windows:

- Either use `pip` or `conda` if you already use them
- If you use Spyder, you'll need to install `spyder-unittest` from the
  `spyder-ide` channel:

1. Open Anaconda Navigator
2. Go to `Environments`
3. Click `Channels` in the right hand pane then click `Add...`
4. Type `https://conda.anaconda.org/spyder-ide`
5. Click `Update Channels` then close that window
6. Click `Update index` in the right hand pane
7. Change the drop-down box to `Not installed` then search for
   `spyder`
8. Check `spyder-unittest` then click `Apply`
9. In Spyder, you can then run the tests from the `Run` menu


![](/img/tdd_191113/./conda_spyder_pytest_install.png)

# Running `pytest`

``` bash
# Find all test files in all subdirectories and run all tests
$ pytest
# Run all tests in a specific file
$ pytest ./test_calculator.py
# Run just one test in a file
$ pytest ./test_calculator.py::test_add_both_positive
```

# Exercise - Write Some Unit Tests

1. Download the basic `calulator.py` file from:
   <https://physicscodingclub.github.io/examples/tdd_19113/calculator.py>
    - Or write your own!
2. Make another file, `test_calculator.py` and write a function
   `test_add_two_positive` that uses `assert` to check the result of
   calling `calculator.add` with two positive numbers
3. Run `pytest` (or `Run > Run unit tests` in Spyder)
    - For those running `pytest` directly, experiment with passing
      `--verbose` or `--quiet`
4. Write some more tests for adding different combinations of numbers:
   both positive, both negative, one of each
    - Try using `pytest -k <part of test name>` to selectively run
      tests
5. Change `calculator.add` to be wrong so you can see what failing
   tests look like
6. **Extention**: what happens if you write a test to use floats? Why
   would `assert actual == expected` not be so great here? Read the
   documentation for `math.isclose` and see if you can use that
7. **Extention**: can you extend `calculator.add` to work with strings
   and/or lists instead of integers?

# Test Driven Development (TDD) - A Different Mindset

![Image ref:
<http://www.fitnessbin.com/wp-content/uploads/2015/12/Rock-Climbing-4.jpg>](/img/tdd_191113/climbing.jpg)

# Test First!?

Instead of trying to test existing code, write code to pass a set of
tests

1.  Identify desired functionality
2.  Write failing test
3.  Make it compile as quickly as possible
4.  Make it pass a quickly as possible
5.  Remove duplication while maintaining 100% pass rate
6.  Repeat as required


![Image ref:
<https://leantesting-wp.s3.amazonaws.com/resources/wp-content/uploads/2015/02/tdd-circle-of-life.png>](/img/tdd_191113/tdd.png)

# Fail, Pass, Refactor: A Simple Example

Here's how to do it in practice. We add a new test _before_ writing
the implementation.

``` python
import calculator


def test_add_both_positive():
    assert calculator.add(3, 2) == 5

def test_subtract_both_positive():
    assert calculator.subtract(10, 8) == 2
```

We know it's going to fail, so let's check it does:

```
========================= test session starts =========================
platform linux -- Python 3.7.3, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
rootdir: /home/peter/Documents/Physics_Coding_Club/191113_TDD/examples/02
collected 2 items

test_calculator.py .F                                           [100%]

============================== FAILURES ===============================
_____________________ test_subtract_both_positive _____________________

    def test_subtract_both_positive():
>       assert calculator.subtract(10, 8) == 2
E       AttributeError: module 'calculator' has no attribute 'subtract'

test_calculator.py:9: AttributeError
===================== 1 failed, 1 passed in 0.02s =====================
```

3\.  **Make it compile as quickly as possible**

What's the simplest thing we can write that will **compile**?

``` python
def subtract():
    pass
```

```
========================= test session starts =========================
platform linux -- Python 3.7.3, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
rootdir: /home/peter/Documents/Physics_Coding_Club/191113_TDD/examples/02
collected 2 items

test_calculator.py .F                                           [100%]

============================== FAILURES ===============================
_____________________ test_subtract_both_positive _____________________

    def test_subtract_both_positive():
>       assert calculator.subtract(10, 8) == 2
E       TypeError: subtract() takes 0 positional arguments but 2 were given

test_calculator.py:9: TypeError
===================== 1 failed, 1 passed in 0.02s =====================
```

Ok, need a bit more!

``` python
def subtract(lhs, rhs):
    pass
```


```
============================== FAILURES ===============================
_____________________ test_subtract_both_positive _____________________

    def test_subtract_both_positive():
>       assert calculator.subtract(10, 8) == 2
E       assert None == 2
E        +  where None = <function subtract at 0x7f983019af28>(10, 8)
E        +    where <function subtract at 0x7f983019af28> =
                    calculator.subtract

test_calculator.py:9: AssertionError
===================== 1 failed, 1 passed in 0.02s =====================
```

Excellent, so it's now actually running our code, although the tests
still fail.

4\.  **Make it pass a quickly as possible**

What's the **simplest** way we can make this pass the test?

``` python
def subtract(lhs, rhs):
    return 2
```

Does that pass the test?


``` 
========================= test session starts =========================
platform linux -- Python 3.7.3, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
rootdir: /home/peter/Documents/Physics_Coding_Club/191113_TDD/examples/02
collected 2 items

test_calculator.py ..                                           [100%]

========================== 2 passed in 0.01s ==========================
```

It's dumb, but it works!

5\.  **Remove duplication while maintaining 100% pass rate**

We duplicated the `2` from the test, let's remove it

``` python
def subtract(lhs, rhs):
    return 10 - 8
```

``` 
========================= test session starts =========================
platform linux -- Python 3.7.3, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
rootdir: /home/peter/Documents/Physics_Coding_Club/191113_TDD/examples/02
collected 2 items

test_calculator.py ..                                           [100%]

========================== 2 passed in 0.01s ==========================
```

Test still passes! Let's remove the duplicated `10` and `8`:

``` python
def subtract(lhs, rhs):
    return lhs - rhs
```


``` 
========================= test session starts =========================
platform linux -- Python 3.7.3, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
rootdir: /home/peter/Documents/Physics_Coding_Club/191113_TDD/examples/02
collected 2 items

test_calculator.py ..                                           [100%]

========================== 2 passed in 0.01s ==========================
```

And we're done!

6\.  **Repeat as required**

Now we keep going to add new features.

# Exercise - Write Some Unit Tests

1. Using `calculator.py` and `test_calculator.py` that you have
   already developed, test and implement `multiply` and `divide` using
   test driven development
2. Implement some extra features using TDD, e.g.
    - handle floats (see `math.isclose`)
    - handle two numbers passed in as strings
    - element-wise array operations (see `numpy.allclose`)
    - raise exceptions for invalid inputs (see `pytest.raises`)

# A Word of Warning:  Pick the right tool for the right job!

![](/img/tdd_191113/progress-vs-time.png)

# Summary

- Unit Testing
    - Unit Testing is a Safety Net
    - Unit Test Structure: Setup, Exercise, Assert
- Test Driven Development (TDD)
    - A Different Mindset
    - Test First!
    - Fail, Pass, Refactor
- Pick the Right Tool for the Right Job

# Testing Frameworks in Other Languages

## Python

- `pytest`: <https://docs.pytest.org/>
- `unittest` -- built in

## C++

- `googletest`: <https://github.com/google/googletest>
- `catch2`: <https://github.com/catchorg/Catch2>

## Fortran

- `pfunit`: <https://github.com/Goddard-Fortran-Ecosystem/pFUnit>

## R

- `testthat`: <https://github.com/r-lib/testthat>

# Further Reading

![Image ref:
<http://d.gr-assets.com/books/1372039943l/387190.jpg>](/img/tdd_191113/tdd-book.jpg)

![Image ref:
<https://images-eu.ssl-images-amazon.com/images/I/518yKmNefUL.jpg>](/img/tdd_191113/legacy_code.jpg)

- <https://martinfowler.com/articles/practical-test-pyramid.html>
- <https://www.codesimplicity.com/post/the-philosophy-of-testing>


# Acknowledgements

- Adapted from slides and examples by SN Biggs
- Creative Commons Attribution-ShareAlike 4.0 International
- <http://www-users.york.ac.uk/~snb519/coding-club-tdd-examples/slides.pdf>
