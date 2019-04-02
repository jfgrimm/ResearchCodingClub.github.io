---
title: How to do everything in Emacs
author: Peter Hill
tags: emacs text-editing practical
---

Something a bit different this week. Working with various different
codes in various different languages, along with writing
presentations, talks and papers, I spend most of my day writing text,
just with different syntaxes. As such, I like to be able to do it all
in the same program -- and that program is Emacs. This week, I led
another hands-on session, giving a shallow dive into the wide, wide
waters of Emacs.

You can get the `.el` files that accompany this seminar [here][git_repo].


# Overview

- Terminology/anatomy
- Basic commands
- Basic customisation
- Multiple cursors
- Flyspell
- Helm
- Projectile
- LaTeX
- C/C++/Fortran (subword mode)
- Python

# Why Emacs?

- It's the best

# Terminology/anatomy

- Emacs development began in 1970s, before Windows/MS Office
- Names of things can be a little different
- Shortcuts for copy, paste, etc. very different
- Helps to see original keyboard:

![Space-cadet](/img/emacs/Space-cadet.jpg)

[By Retro-Computing Society of Rhode Island - Own work, CC BY-SA 3.0](https://commons.wikimedia.org/w/index.php?curid=3388741)

# Terminology/anatomy

- "kill" = "cut"
- "yank" = "paste"

## Windows and frames

![Cpp_in_GNU_emacs](/img/emacs/Cpp_in_GNU_emacs.png)

[By Original uploaded by: Praveep - Transferred from ml.wikipedia to Commons by Sreejithk2000 using CommonsHelper., GPL](https://commons.wikimedia.org/w/index.php?curid=12584006)

# Terminology/anatomy

## Major Modes

- Only one per buffer
- Specialised behaviour for particular file or buffer types
    - e.g. C source code, or compilation buffer

## Minor modes

- Optional features,  can have multiple per buffer
    - e.g. auto-fill mode for automatically inserting line breaks, or flyspell mode for spell-checking
- Some are "buffer-local", i.e. can be turned on/off per buffer
- Some are "global", i.e. turned on/off for all buffers at once

# Vim Users

## Vim-like modal editing and keybindins

- Evil mode (extensible vi layer for Emacs)
- Spacemacs
- Doom

# Basic commands

- `C` means Ctrl, `M` means Alt (Meta)
- In terminals, `C-M-` combos might be hard to type, so you can use `C-[ C-` instead
- Lots of commands can take a "prefix argument": press `C-u` before the rest of the shortcut or command to use optional arguments
    - e.g. `C-u 4 C-b`: move four characters backwards
- Rebinding Caps lock as an extra ctrl can be useful: <https://www.emacswiki.org/emacs/MovingTheCtrlKey>
- Eval any elisp commands anywhere with `C-x C-e`
- `C-g`: general purpose "cancel"

<!-- ## Movement -->

<!-- Forward: -->

<!-- - `C-f` forward-char -->
<!-- - `M-f` forward-word -->
<!-- - `C-M-f` forward-sexp -->

<!-- Backward: -->

<!-- - `C-b` -->
<!-- - `M-b` -->
<!-- - `C-M-b` -->

<!-- Up: -->

<!-- - `C-p` -->

<!-- Down: -->

<!-- - `C-n` -->

<!-- Beginning: -->

<!-- - `C-a` -->
<!-- - `M-a` -->
<!-- - `C-M-a` -->

<!-- End: -->

<!-- - `C-e` -->
<!-- - `M-e` -->
<!-- - `C-M-e` -->

# Movement you might not know

## Lines

- `M-m`: move to first non-whitespace character on line

## Brackets

- `C-M-f`, `C-M-b`: move over balanced brackets
- `C-M-<space>`: selected balanced brackets

## Functions

- `C-M-a`, `C-M-e`: move over functions
- `C-M-h`: select whole function

# Getting help

## Help functions

- `C-h f` help on functions
- `C-h v` help on variables
- `C-h l` key stroke history (possibly with command names!)
- `C-h m` help on current major mode (keybindings and useful functions)

## Outside Emacs:

- <https://emacs.stackexchange.com/> *Q&A site*
- <https://www.emacswiki.org/> *Generally good first stop*
- <https://tuhdo.github.io/> *In-depth tutorial* 

# Beyond the basics

## Macros

- `C-x (` Begin record macro
- `C-x )` End recording
- `C-x e` Run macro
- `C-u <n> C-x e` Run macro `<n>` times
- `M-0 C-x e` Run macro until it stops

# Beyond the basics

## Rectangles

- `C-x r k`: kill rectangle
- `C-x r y`: yank rectangle
- `C-x r t`: replace rectangle with string
- `C-x r N`: insert numbers in front of rectangle

## Capitalisation

- `M-u`: UPPERCASE next word
- `M-l`: lowercase next word
- `M-c`: Capitalise next word

# Beyond the basics

## Working with windows

- `C-x 2`: Split window vertically
- `C-x 3`: Split window horizontally
- `C-x 0`: Close this window
- `C-x 1`: Close everything **but** this window
- `C-x C-b`: List of open buffers
- `C-x 4 b`: Switch to buffer in other window

# Beyond the basics

## Miscellaneous

- `M-q`: "fill" paragraph - insert line breaks at "fill-column"
- `M-<space>`: replace multiple whitespace with single space
- `M-$`: spell-check word
- `M-/`: auto complete

# Beyond the basics

## emacsclient

- In bash, set the environment variable `EDITOR` to `emacsclient`, and
  do `M-x server-start` inside an existing emacs session
- Now when other programs need to open `$EDITOR`, it will open in your
  existing emacs session

## TRAMP

- Open remote files by prepending the path with `/ssh:username@host:`

# Basic customisation

- Emacs core is written in C, but wrapped in elisp (Emacs Lisp)
- All customisation is done through elisp
- Key points about elisp:
    - Functions are written in Polish notation with function name
      first, then arguments: `+ 1 2`
    - Everything is written in a list: `(+ 1 2)`
    - Code and data are treated as equals, which means we often need
      to distinguish between symbols and their values: use `(quote x)`,
      or simply `'x`

# Basic customisation

## [`customisations/0-basic.el`][0-basic]

```lisp
;; Remember minibuffer history across sessions:
(savehist-mode 1)

;; Remember lots of history lines:
(setq history-length 100)

;; No startup screen
(setq inhibit-startup-screen t)

;; Highlight region
(transient-mark-mode 1)
```

# Installing packages

## [`customisations/1-packages.el`][1-packages]

```lisp
;; We need symbols from the "package" package
(require 'package)

;; Use https for packages
(setq package-archives
      '(("gnu" . "https://elpa.gnu.org/packages/")
        ("melpa" . "https://melpa.org/packages/")))
;; Do some basic hardening of the package system
;; See https://glyph.twistedmatrix.com/2015/11/editor-malware.html
```

# Use use-package

<https://github.com/jwiegley/use-package>

## [`customisations/1-packages.el`][1-packages]

```lisp
;; Initialise packages now
(setq package-enable-at-startup nil)
(package-initialize)

;; Make sure we have use-package installed
(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))

(eval-when-compile
  (require 'use-package))
(require 'diminish)
(require 'bind-key)

```

# Magit

<https://magit.vc/>

The *best* git interface

Needs Emacs 24.4+ (not available in Ubuntu 14.04) and git 1.9+

## [`customisations/2-magit.el`][2-magit]

```lisp
(use-package magit
  :ensure t
  :bind
  (("\C-cm" . magit-status)))
```

<!-- - Adding -->
<!-- - Committing -->
<!-- - Merging -->
<!-- - Conflicts -->
<!-- - Remotes -->
<!-- - Logs -->
<!-- - Blame -->

# Multiple cursors

<https://github.com/magnars/multiple-cursors.el>

## [`customisations/multiple-cursors.el`][multiple-cursors]

```lisp
(use-package multiple-cursors
  :bind
  (("C->" . mc/mark-next-like-this)
   ("C-<" . mc/mark-previous-like-this)))
```

# Auctex

<https://www.gnu.org/software/auctex/>

## [`customisations/3-auctex.el`][3-auctex]

```lisp
(use-package tex
  :ensure auctex

  :config
  (setq TeX-auto-save t
        TeX-parse-self t
        TeX-PDF-mode t)
  (setq-default TeX-master nil)
  (add-hook 'LaTeX-mode-hook 'turn-on-reftex))
```

# Auctex

## Basic commands

- `C-c RET`: insert macro
- `C-c C-e`: insert environment
- `C-u C-c C-e`: change environment
- `C-c C-c`: run LaTeX/BibTex/View document

# C/C++/Fortran

## Example C project

- Open `c/main.c`
- `M-x shell` to get an Emacs shell
- `make tags` to run etags and make TAGS file

## xref

- `M-.`: Find definition
- `M-?`: Find reference
- `M-,`: Go back

# C/C++/Fortran

## Compiling

- `M-x compile`: Compile the code
- ``C-x ` ``: Jump to first error

See [`customisations/4-c-like-languages.el`][4-c-like-languages] for some more useful things

## 

# Helm (previously Anything)

<https://github.com/emacs-helm/helm>

## [`customisations/5-helm-projectile.el`][5-helm-projectile]

```lisp
(use-package helm
  :ensure t
  :diminish helm-mode
  :bind
  (("C-x C-f" . helm-find-files)
   ("M-x" . helm-M-x)
   ("M-y" . helm-show-kill-ring)
   ("C-x b" . helm-mini)
   ("C-c h" . helm-command-prefix))

  :config
  (helm-mode 1))
```

# Helm

- Better completion of commands
- <http://tuhdo.github.io/helm-intro.html>

## General use

- Search for candidates by typing parts (or regex) of match:
    - e.g. "li pa" brings up `list-packages`
    - e.g. ".*[ch]xx" brings up all C++ files
- You can run actions on candidates, e.g. bring up the help on a function
- You can mark multiple candidates and run an action on all of them
    - e.g. close multiple buffers
    
# Helm

## Useful actions

- `C-x b` can show recent buffers by pressing $\rightarrow$
- In buffer menu, `M-S-d` (`M-D`) to kill buffer(s)
- In file/buffer menu, `C-o` to open in other window
- In file menu, `C-l` to go up a level
- In function/variable help menu, `<tab>` to display help for
  highlighted function
- In any helm menu, `C-h m` to get more help

# Projectile

<http://batsov.com/projectile/>

## [`customisations/5-helm-projectile.el`][5-helm-projectile]

```lisp
(use-package projectile
  :ensure t
  :init
  (projectile-mode t)
  (use-package helm-projectile)
  (setq projectile-completion-system 'helm)
  (helm-projectile-on))
```

- All-in-one command: `C-c p h`
    - Switch to buffer
    - Find file
    - Switch project

# Back to C project

<https://tuhdo.github.io/helm-projectile.html>

## Projectile commands

- `C-c p a`: Switch to "other" file (`.c <--> .h`)
- `C-c p c`: Run compile command
- `C-c p P`: Run test command
- `C-c p s g`: Run grep on project

# Python

<https://elpy.readthedocs.io/en/latest/>

## [`customisations/6-python.el`][6-python]

```lisp
(use-package elpy
  :config
  (setq elpy-rpc-python-command "python3")
  (setq elpy-test-runner 'elpy-test-pytest-runner)

  (when (require 'flycheck nil t)
    (setq elpy-modules (delq 'elpy-module-flymake elpy-modules))
    (add-hook 'elpy-mode-hook 'flycheck-mode)))
```


[git_repo]: https://github.com/PhysicsCodingClub/EverythingWithEmacs
[0-basic]: https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/0-basic.el
[1-packages]: https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/1-packages.el
[2-magit]: https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/2-magit.el
[3-auctex]: https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/3-auctex.el
[4-c-like-languages]: https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/4-c-like-languages.el
[5-helm-projectile]: https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/5-helm-projectile.el
[6-python]: https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/6-python.el
[multiple-cursors]: https://github.com/PhysicsCodingClub/EverythingWithEmacs/blob/master/customisations/multiple-cursors.el
