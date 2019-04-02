---
title: Python packaging
subtitle: Your code is important too
author: Ben Dudson
tags: Python packaging
---

The code we write is often a means to an end: our main outputs are
papers, PhD theses, talks and grants. But a lot of work goes into
writing the code, and often this work is lost when someone leaves, and
repeated by the next person. The code is also a record of how results
were generated.

This week, Ben led us through how and why to make your code available
to others, and in particular how to package python projects.


Why (and why not) make your code open?
======================================

**Pros**

* Enables your work to have a wider impact; others can build on what you have done
* Something to be known for when building a career
* Widens the number of collaborators, potential coauthors
* You can benefit from fixes and improvements
* The code commits are a public record

**Cons**

* A significant effort to document, tidy code
* Time investment in supporting other users.
  Less time doing physics research

Most software projects are abandoned
====================================

[columns]

[column=0.65]

* As of April 2017, GitHub claims to have 57 million repositories [Wikipedia]
* In 2012 a presentation on Ohloh (now Open Hub) showed:
    * Only 5% of projects had a commit in the last year and more than one committer
    * Only about half of projects had more than one committer
    * 17% of projects had a commit in the last year
    
<https://www.slideshare.net/blackducksoftware/open-source-by-the-numbers> 

[column=0.35]

\begin{figure}
\centering
\includegraphics[width=\textwidth]{project_commits.png}

\includegraphics[width=\textwidth]{project_team.png}
\caption{}
\end{figure}

[/columns]

Barriers to adopting code
=========================

* Finding the code (**)
* Understanding what it does
* Getting it installed (**)
* Learning how to use it
* Fixing it when something goes wrong

The Tale of J.Random Newbie: <http://www.catb.org/~esr/writings/taoup/html/ch16s01.html>

Finding the code
================

* Use a public repository like GitHub or BitBucket
* Some languages have package indexes
    * Python PyPI <https://pypi.python.org/pypi>  (**)
    * Julia <https://pkg.julialang.org/>
    * Haskell Hackage <https://hackage.haskell.org/>
    * Perl CPAN <https://www.cpan.org/>
    * Common Lisp QuickLisp <https://www.quicklisp.org/beta/>
* A website linking to the repo can help Google
    * Readthedocs - Documentation (see later)
    * github.io web hosting
    * University of York home pages

Understanding what a code is/does
=================================

[columns]

[column=0.5]

If you are making code available, you should include
these text files:

* README, describing what the code does
* LICENSE, specifying the license/copyright
* INSTALL, with instructions on how to install it

Github and other online repositories make these part of the project front page

[column=0.5]

\begin{figure}
\centering

\includegraphics[width=\textwidth]{numpy_license.png}

\includegraphics[width=\textwidth]{numpy_github.png}
\caption{}
\end{figure}

[/columns]

Understanding what a code is/does
=================================

[columns]

[column=0.5]

If you are making code available, you should include
these text files:

* README, describing what the code does
* LICENCE, specifying the license/copyright
* INSTALL, with instructions on how to install it

Github and other online repositories make these part of the project front page

[column=0.5]

\begin{figure}
\centering

\includegraphics[width=\textwidth]{numpy_license.png}

\includegraphics[width=\textwidth]{numpy_github_raw.png}
\caption{}
\end{figure}

[/columns]


Installing code
===============

If your code is hard to install, people need a very strong motivation or they will not do it.

* Compiled languages (C, Fortran etc.) need to be compiled:
```configure, make, make install```

* Python and other languages need an interpreter e.g. Python 2 or 3 installed
* Most code needs libraries

Help your users (and yourself) by:

* Documenting the libraries your code needs
* Documenting the install process
* Having a Makefile or other build system
* (Preferably) having a configuration script and install target

Python packaging
================

Python code is organised into packages, which are just directories and files

```bash
thing/
     __init__.py
     code.py
```

* ``__init__.py`` does not have to contain anything, just exist

If ``thing`` is in your current directory, or in the ``PYTHONPATH`` environment variable, then you can run:

```python
from thing import code

code.myfunction()
```

Tidying up the interface
========================

What if we try something slightly different:

```python
import thing
thing.code.myfunction()
-> AttributeError: module 'thing' has no attribute 'code'
```

When we import ``thing`` we don't automatically import the ``code.py`` file.
This is what the ``__init__.py`` file is for.

In ``__init__.py``

```python
from . import code
```

The ``code`` file is then imported automatically when ``thing`` is imported.

**Note**: The format of these relative imports have changed from Python 2 to Python 3.


Python installation: ``setuptools``
===================================

A small python script ``setup.py`` can be used to specify

* Which libraries or packages your code depends on
* How to compile any C or Fortran code included in your package

These scripts can then automatically install your code.

```python
from setuptools import setup

setup(
    name = "Thing",
    version = "0.1",
    packages = ["thing"]
    )
```

<https://packaging.python.org/tutorials/distributing-packages/>

Testing your installation process
=================================

Installing in your system paths is not a good idea, particularly when testing. Instead:

```bash
$ python setup.py install --user
...
creating thing.egg-info
installing library code to build/bdist.linux-x86_64/egg
...
creating 'dist/thing-0.1-py3.6.egg' and adding 'build/bdist.linux-x86_64/egg' to it
...
Processing thing-0.1-py3.6.egg
Installed /home/bd512/.local/lib/python3.6/site-packages/thing-0.1-py3.6.egg
Processing dependencies for thing==0.1
Finished processing dependencies for thing==0.1
```

Console and GUI scripts
=======================

If your project is supposed to be run as an application,
``setuptools`` can automatically create executables that will work
under both Linux and Windows:

```python
setup(
      ...
      entry_points={'console_scripts': [
                        'script = package.__main__:main'],
                    'gui_scripts': [
                        'app = package.__main__:gui'},
      )
```

This will create an executable called ``script`` (or ``script.exe``
for Windows) that imports the function ``main`` from
``package.__main__`` and then calls it with no arguments.

The ``gui_scripts`` only makes a difference on Windows, where it will
launch the program without opening a console window.

Entry points
============

Here's a basic console entry point function in ``package/__main__.py``:

```python
import sys

def main(args=None):
   """The main routine"""
   if args is None:
       args = sys.argv[1:]
   print("This was called with command line arguments: ", args)

if __name__ == "__main__":
    main()
```

The magic ``__name__ == "__main__"`` part allows the package to be
invoked with ``python -m <package>`` to run the ``main()`` function

Dependencies
============

``setuptools`` also handles dependencies, and will fetch packages from PyPI as needed.

```python
setup(
      ...
      install_requires=['numpy>=1.8',
                        'scipy>=0.14',
                        'matplotlib>=1.3'],
      )
```

* Can specify a minimum version, an exact version (``==``), or more complicated ranges
* Dependencies can be at a web address or repository (git/hg/svn) if they have a ``setup.py`` file or are a single python file


Distributing python packages: PyPI
==================================

* Register an account on <https://pypi.python.org/pypi>

* Build a *source distribution*

```bash
   $ python setup.py sdist
```

* [Optional] Create a *wheel* (various types, pre-built)

```bash
    $ pip install --user wheel
    $ python setup.py bdist_wheel --universal
```

* Install ``twine`` (> 1.8.0) and upload the project (may need ``~/.pypirc`` )

```bash
   $ pip install --user twine
   $ twine upload dist/*
```

Distributing Packages: <https://packaging.python.org/tutorials/distributing-packages/>

More complicated projects
=========================

The ``setup.py`` script can handle much more complex situations
(NumPy,SciPy)

* Cython

```python
   from setuptools.extension import Extension
   from Cython.Build import cythonize
   import numpy

   extensions = [ Extension("somemodule",
                            ["somemodule.pyx"],
                            include_dirs=[numpy.get_include()])
                ]
   setup(...
         ext_modules=cythonize(extensions)
         )

```
<https://copyninja.info/blog/cython_setuptools.html>

More complicated projects
=========================

The ``setup.py`` script can handle much more complex situations
(NumPy,SciPy)

* Cython
* C, Fortran extensions
* Installation scripts
* Installing your code as a script (executable command)

Conclusions
===========

* Making your code available is generally a good thing
* Important to include README, LICENSE, documentation, tests
* Make life easier for new users


* Python ``setuptools`` very easy to set up for simple projects
* More complicated projects are... more complicated
* Uploading to PyPI makes installing your code easy. The process has changed several times, so documentation not consistent

One I made earlier...
``` bash
    $ pip install freegs
```


<https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/>

