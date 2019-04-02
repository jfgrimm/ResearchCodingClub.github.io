---
title: Getting ORGanised
author: Peter Hill
tags: emacs org-mode text-editing
---

There are a thousand apps for organising your life, calendars, todo
lists, note trackers, but the big kahuna, the true Swiss army knife is
org-mode. Out of the box, org-mode understands LaTeX and code
snippets, todo lists and bookmarks, projects and agendas. Best of all,
it comes with a powerful text editor, Emacs! This week, Ben gave us a
live demo of org-mode in Emacs

You can get the original org-mode file from [here][orgfile]

# What is ORG mode?     

-   Text-based way to organise notes, links, code, and more
-   **Time management tool**
    -   TODO lists
    -   Tasks, projects
-   Table editor, spreadsheet
-   Interactive code notebook
-   Can be exported to LaTeX, markdown, HTML,&#x2026;

All in Emacs!

[Setup Emacs configuration](https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/7-org-mode.el)

[Reference / summary](https://github.com/caiorss/Emacs-Elisp-Programming/blob/master/Org-Mode.org)

# The ORG file format     

A simple text format like Markdown. 

-   Anything can be edited, fixed easily by hand if needed.
-   You can start simple, and discover extra features
    [Try Alt right/left, shift right/left, TAB to collapse/expand]

```
* Some section
** A subsection
*** Subsection
**** subsubsection
  - list
  - another item
    - sub-items
** Another subsection
```

# Links     

Links files, URLs, shell command, elisp, DOI, &#x2026;

<http://www.google.com>

<10.5281/zenodo.2530733>

[link](http://en.wikipedia.org)


# LaTeX     

-   Standard LaTeX formulae are recognised and rendered

Inline like this \(e^{i\pi} = -1\)

\[
e^{i\theta} = \cos\left(\theta\right) + i\sin\left(\theta\right)
\]

Toggle equation view: C-c C-x C-l 


# Tables     

-   Start creating a table with "| headings |" then TAB
-   Alt + arrow keys move columns, rows
-   Functions can also manipulate cells

```
| b | a       | c |
|   |         |   |
|   | kjdhfsf |   |
```

# Source code, notebooks     

-   Type "<s TAB" (other shortcuts for Examples, Quotes, &#x2026;)
-   Supports [many languages](https://orgmode.org/manual/Languages.html)
-   C-c C-c runs the code block

```
#+BEGIN_SRC python :results output
print("hello")
#+END_SRC

#+RESULTS:
: hello
```

# Tables and code blocks     

-   Tables can be used as input and output to code blocks
-   Provides a way to pass data between languages

```
#+NAME: cxx-generate
#+BEGIN_SRC C++ :includes <iostream> 
for(int i = 0; i < 5; i++) {
  std::cout << i << ", " << i*i*i - 2*i << "\n";
}
#+END_SRC

#+RESULTS: cxx-generate
| 0 |  0 |
| 1 | -1 |
| 2 |  4 |
| 3 | 21 |
| 4 | 56 |

#+BEGIN_SRC python :var data=cxx-generate
import matplotlib.pyplot as plt
import numpy as np
d = np.array(data)
plt.plot(d[:, 0], d[:, 1])
plt.show()
#+END_SRC

#+RESULTS:
: None
```

# Task management     

Creating tasks in org-mode: 

-   Add "TODO" to the start of a (sub)section (or S-right)
-   C-c C-d to choose a deadline from calendar
-   C-c a   to see Agenda views


```
** Project1
*** TODO thing1
   DEADLINE: <2019-02-22 Fri>
*** TODO thing2
    DEADLINE: <2019-02-20 Wed>
** Project2
*** TODO do something
    DEADLINE: <2019-02-27 Wed>
*** TODO send email
```

# More task management     

-   Once tasks are done they can be marked "DONE"
-   Other states can be customised: NEXT, WAITING, CANCELLED,&#x2026;
    S-right to cycle between states, type C-c C-t 
    or just write yourself.

```
** DONE that thing
   CLOSED: [2019-02-18 Mon 10:28]
   - State "DONE"       from "WAITING"    [2019-02-18 Mon 10:28]
   - State "WAITING"    from "DONE"       [2019-02-18 Mon 10:27] \\
     waiting for X
```

This can be customised to fit your preferred way of working

-   Getting Things Done (GTD)


# Time management     

How much time to you spend on each task?

-   C-c C-x C-i  clock in
-   C-c C-x C-o  clock out
-   C-c a c      Agenda clock view
-   C-c C-x C-r  Insert / update clock table

# Presentations!     

This presentation is Org mode with [org-show](https://github.com/jkitchin/scimax/tree/master/org-show)

Files can be exported to many other formats: C-c C-e

e.g. LaTeX -> PDF C-c C-e l p

Can be used as alternative to writing raw LaTeX.


## More information

- <http://doc.norang.ca/org-mode.html>
- <http://cachestocaches.com/2016/9/my-workflow-org-agenda/>



[orgfile]: /slides/2019-02-18-org-mode.org
