"""
Verbose version of testCalculator

Copyright 2017 Steve Biggs

This file is part of coding-club-tdd-examples.

coding-club-tdd-examples is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

coding-club-tdd-examples is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with coding-club-tdd-examples.  If not, see http://www.gnu.org/licenses/.
"""

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
