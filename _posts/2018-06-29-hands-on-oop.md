---
title: Hands on Object-Oriented Programming
author: Peter Hill
---

Object-Oriented Programming (OOP) is one of the major paradigms in
programming. Last week, I gave an intro talk on the main principles of
OOP, contrasting it to other programming paradigms like imperative and
functional programming. We also looked at some examples of using OOP
in Python, Fortran and C++. This week, we're getting our hands dirty
actually writing some OOP from scratch in Python.

# Outline

- Classes and Instances
- Abstraction
- Encapsulation
- Inheritance
- Polymorphism

Code shamelessly stolen from <https://www.youtube.com/watch?v=qxOqZQ1fWNw>

# Recap on OOP

## The Four Pillars

- **Abstraction**: hide the details
- **Encapsulation**: protect the details
- **Inheritance**: things can be a subtype of another thing
- **Polymorphism**: things can act like other things

# Before we begin...

- [Download the tests](/resources/inventory_tests.tar) and unpack the
  tests:

```bash
$ tar xvf inventory_tests.tar
```

- Install pytest:

```bash
$ pip3 install --user pytest
```

- You might need to add the following to your `PATH`:

```bash
$ export PATH=~/.local/bin:$PATH
$ which pytest
```

# Classes and Instances

## Inventories and Items

- Make a file `inventory.py`
- Let's start with a very simple class:

```python
class Item:
    """A generic item

    Attributes
    ----------
    name : str
        The name of the item

    """
    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    sword = Item("Sword")
    falafel = Item("Falafel")

    print(sword)
    print(falafel)
```

Then run it:

```bash
$ python3 ./inventory.py
<__main__.Item object at 0x...>
<__main__.Item object at 0x...>
```

The `0x...` is the address in memory of the instance

## More useful printing

Let's add the "magic method" `__str__` which converts an object to a
string:

```python
class Item:
    ...
    def __str__(self):
        return self.name
```

- Now what happens when you run the file?

## Beginner

- We're going to be making a container for `Item`s, so will need to
  know how big they are
- Give `Item`s a `size` attribute
- Add the `size` in `__str__` so we know how big the `Item` is
  when we `print` it
    - Hint: the tests are looking for something like "size 2"
- Don't forget to update the docstring for `Item`
- Download the tests from ... and run `pytest -q test_inventory01.py`
  to check your work

## Advanced

- The `__repr__` method returns a string that can reproduce the object
  using `eval`:
    - `eval(repr(Item("Falafel", 1))) == Item("Falafel", 1)`
- Add the `__repr__` method
- Also add a `test_repr_pack` method to `test_inventory01.py` to check
  `__repr__` works
    - Hint: You might also add `__eq__` to test for equality

# Inheritance and Polymorphism

## Different types of Items

- All `Item`s have a name and a size
- `Item`s are kind of abstract though, and different `Item`s do
  different things
- What do all good games need? Weapons and food!

```python
class Weapon(Item):
    pass

class Food(Item):
    pass

...

sword = Weapon("Sword", 8)
falafel = Food("Falafel", 1)

print(sword)
print(falafel)

isinstance(sword, Weapon) # True
isinstance(sword, Food)   # False
isinstance(sword, Item)   # True
```

- `pass` tells Python to do nothing
    - We've essentially made two aliases for `Item`
- `isinstance` tells us if an object is an instance of a particular
  type
- Let's do something a little fancy to tell the difference:

```python
class Item:
    ...
    def __str__(self):
        class_name = self.__class__.__name__
        return ("{} is a {} of size {}".format(self.name, class_name, self.size)
```

- `__class__` is the class object of an object
    - In Python, everything is an object!
- `__name__` is the name of the class

- `print(sword)` is now a bit more informative

## Specialising subtypes

- If `Weapon`s and `Food` behaved completely identically, we wouldn't
  need to subclass them
- Let's give a `power` attribute to `Weapon`s:

```python
class Weapon(Item):
    """An Item suitable for fighting with

    Attributes
    ----------
    name : str
        The name of the item
    size : int
        How many spaces in a Pack the Item takes up
    power : int, float
        How much damage the Weapon does
    """
    def __init__(self, name, size, power):
        self.name = name
        self.size = size
        self.power = power
```

- Here we are **overriding** the `__init__` method from `Item`
- When we make a new `Weapon`, we now call `Weapon.__init__` instead
  of `Item.__init__`
- But aren't we just repeating code from `Item.__init__`?
- What if we had a whole chain of inheritance?
- `super()` is the answer: this essentially gets the parent type of
  our object:

```python
class Weapon(Item):
    def __init__(self, name, size, power):
        super().__init__(name, size)
        self.power = power

    def __str__(self):
        return "{} and power {}".format(super().__str__(), self.power)
```

- What about entirely new methods?

```python
class Weapon(Item):
    ...
    def attack(self):
        """Attack wildly

        """
        print("You attack for {} damage!".format(self.power))
```

- We can `attack` with `Weapon`s, but not with a generic `Item`:

```python
sword = Weapon("Sword", 8, 4)
falafel = Food("Falafel", 1, 12)

# This is ok
sword.attack()

# This is not!
falafel.attack()
```

## Beginner

- Add a `potency` attribute to `Food`
- Add a `eat` method to `Food` that prints a string that says you heal
  "`potency` health"
- Don't forget the docstrings!
- Check your work by running `pytest -q test_inventory02.py`

## Advanced

- Make a subclass of `Weapon` called `RangedWeapon` that has a `range`
  attribute
- Override the `attack` method to take a `distance` argument that
  reduces the `power` to zero outside of `range`
    - Hint: use `super()` to call `Weapon.attack` with the adjusted
      `power`
- Don't forget to add tests to check your work

# Abstraction and Encapsulation

## Putting the Items away

- Making a pack that can store items
- Has a list that we can add items to
- We'll want some control over what items we store
    - e.g. make sure they are items, and we don't overfill the pack
- `add` and `remove` methods
- we're encapsulating the data, protecting it from direct modification

```python
class Pack:
    def __init__(self, capacity):
        self.capacity = capacity
        # Single underscore to mark this as "private"
        self._contents = []

    def add(self, item):
        """Add an Item to the Pack

        Parameters
        ----------
        item : Item
            An Item to store in the pack

        """
        self._contents.append(item)
```

- We've *encapsulated* the container to hide the implementation detail
  of how `Item`s are actually stored
    - `_contents` is hidden
- Prevents direction modification of the `_contents`
- Allows us to change the implementation details later, providing we
  don't change the interface (`add(self, item)`)

## More useful

- A `Pack` has a `capacity`: we can't put infinite `Item`s in it
- `Pack.add` should check we can store an `Item` before letting us do
  so!
- Let's add a method for finding out how much stuff we've got in our `Pack`:

```python
class Pack:
    ...
    def space_used(self):
        """Returns the total size of the items in this Pack

        """
        total_size = 0
        for item in self._contents:
            total_size += item.size
        return total_size
```

- We've *abstracted* over the details of calculating how much space
  we've used in the `Pack`
- This goes hand-in-hand with the encapsulation of `_contents`

## Beginner

- Implement `space_left`, `is_full` and `is_empty`
    - Hint: `space_left` should return an integer, and `is_full/empty`
      should return `True` or `False`
- Add a check to `add` to make sure we only put `Weapon`s and `Food`
  in the `Pack`
    - Hint: what do they have in common?
- Add a check to `add` to make sure there's enough space to fit the
  `Item` in the `Pack`
    - Hint: `raise` a `ValueError` if there isn't
- Check your work by running `pytest -q test_inventory03.py`

## Advanced

- Implement `has_item` which takes a string and returns `True` if
  there is an `Item` of that name in the `Pack`
- Implement `remove` which takes a string, and if there's an `Item` of
  that name in the `Pack`, remove it from `_contents` and return the
  `Item`
    - Hint: you probably want `enumerate` and `list.pop`
- Don't forget to add tests and check your work

## Other things to do!

- Change `_content` to a dictionary with the `Item` name as the key,
  and a tuple containing the `Item` and how many there are as the
  value
