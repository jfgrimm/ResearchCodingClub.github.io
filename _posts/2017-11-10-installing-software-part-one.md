---
title: Installing Software on Linux
subtitle: Part One
author: Peter Hill
---

Whatever you're doing in your research, it won't be long before you
find yourself needing some piece of software that you don't currently
have. Installing software can sometimes seem a little like black
magic, with cryptic commands that need to be run and arcane rituals
that have to be performed before the thing just works and you can get
on with using it.

This week we started with the absolute basics of installing software
on Linux, covering how to use the package manager, up to how to
install basic software from source without needed special admin
rights.

Next week we'll be covering more advanced topics, including what to
do if (when...) things go wrong!

# Outline

- What is a Linux distribution?
- Package managers
- Installing from source
- Best practices

# What is a Linux distribution?

- Set of software all compiled with the same compiler and compatible
  settings
- Provide a set of "repositories" for pre-compiled software that you
  can download and unpack into the correct locations
    - Official set of "repos" *is* the distribution
    - But you can add additional repos to expand list of software that
      can be installed
- Provide a package manager that provides interface for searching and
  installing software from the distribution's repositories
    - Ubuntu uses `apt`, Fedora uses `dnf` or `yum`, OpenSUSE uses `zypper`

# Package managers

- Package manager takes care of things like dependencies
    - e.g. NetCDF requires libnetcdf which requires libhdf5;
      installing NetCDF will automatically install both libnetcdf and
      libhdf5
- Whole "package" is usually in a compressed format such as ".deb"
  (Ubuntu/Debian) or ".rpm" (Fedora/OpenSUSE)
    - Package file contains the compiled software, plus any scripts or
      data, and usually a recipe for installing everything
   - Package manager will run included post-install scripts
     (e.g. setting up system accounts and configuration files)
- Package manager normally the "pretty face" for a workhorse backend
    - `dpkg` for .deb, `rpm` for .rpm
    - Sometimes also a GUI version, an "even prettier face"

# Conventional Linux system layout

- Packages are pre-compiled software that just gets extracted -- but
  where to?
- The relevant parts of the conventional Linux (more generally "*nix")
  system layout\*:
- `/` -- the `root` of the whole filesystem, i.e. the top-level
    - `/etc/` -- system-wide configuration files ("`et cetera`")
    - `/usr/` -- `user` utilities and programs
        - `/usr/bin/` -- executables ("binaries")
        - `/usr/include/` -- standard include files (headers, etc.)
        - `/usr/lib/` -- libraries
        - `/usr/share/` -- data
        - `/usr/local/` -- locally installed non-system software
    - `/opt/` -- third-party non-system packages

\* Filesystem Hierarchy Standard

# Installing software with a package manager

- You need to have some kind of admin privileges to use the package
  manager, so this is (typically) only useful on computers you own
  yourself
- First, find the package you want:
    - `apt search <package>`
    - `dnf search <package>`
    - `zypper search <package>` (or just `zypper se <package>`)
- Then, install:
    - `sudo apt install <package>`
    - `sudo dnf install <package>`
    - `sudo zypper install <package>` (or just `zypper in <package>`)
    - We have to use `sudo` here because we'll be changing the system
      for everyone!
    - Normally get presented with a summary of what's going to happen,
      e.g. additional packages that need to be installed, incompatible
      packages that have to be removed, etc.
    - Normally require confirmation, `Are you sure? [Y/n]` -- here,
      the capital "Y" means this is the default choice if you just hit
      `enter`

# Removing software

- As easy as installing:
    - `sudo apt remove <package>`
    - `sudo dnf remove <package>`
    - `sudo zypper remove <package>` (or just `sudo zypper rm <package>`)
- Sometimes the package manager might not remove all the extra
  packages it installed in the first place
- In that case:
    - `sudo apt autoremove`
    - `sudo dnf autoremove`
    - `sudo zypper remove --clean-deps <package>` to remove everything
      in the first place
        - `zypper packages --unneeded` to list unneeded packages which
          can then be removed

# Adding extra repositories

- Easiest method: use the GUI to add more repos
- Several distributions have collections of extra repositories
    - PPAs for Ubuntu, Open Build Service for OpenSUSE
- Command-line methods:
    - `sudo add-apt-repository ppa:<ppa name>`
    - `sudo dnf config-manager --add-repo <repo url>`
    - `sudo zypper addrepo <repo url>`
- Usually need to update/refresh list of packages before you can
  search and install from a new repo

# Installing software outside of repositories

- Some software just provides .deb or .rpm file to download and
  install
- Just use your package manager to install the file (or url)
- Sometimes then adds an extra repo automatically for updates
- Uses the usual mechanisms to install dependencies

# Help, it's all gone wrong!

- What issues can arise with the package manager?
    - corrupt database
    - lack of disk space
    - incompatible packages
    - locked database
    - package removed manually rather than with package manager
    - interrupted update

# Specific fixes

- Locked database:
    - Cause: two things trying to install something at the same
      time. Normally due to background update when you try and install
    - Fix: wait! If that's not working, kill package manager
      processes, clean up database, try again
- Lack of disk space:
    - Cause: old kernels piling up
    - Fix: `sudo apt autoremove`
- Incompatible packages:
    - Cause: usually due to additional repos
    - Fix: remove all problem packages, update whole system, try
      reinstalling packages
        - May also need to change which repo you get the package from

# General fixes

- Something has gone badly wrong, and the package manager is refusing
  to either remove, uninstall or update anything!
- Possible causes:
    - interrupted update, file corruption, mutually dependent but
      incompatible packages
- Possible fixes:
    - **Read the error message!** Sometimes tells you exactly how to
      fix the problem, usually gives you a lead
    - Clear the package cache (previously downloaded packages)
        - `sudo apt autoclean`, `sudo zypper clean`, `sudo dnf clean`
    - Run the low-level package manager "configure" option
        - `sudo dpkg --configure -a`, `sudo rpmdb --rebuilddb`
        - This re-runs any setup or tidying that needs to be done
    - Refresh/update package list and try again
    - On Ubuntu: `sudo apt install -f` fixes most problems

# General fixes

- I can't even log in!
    - Use a virtual terminal - `Ctrl + Alt + F1`
        - Text-only interface
    - Try updating, might just work, might give you a clue
- All else fails: ask the internet!

# Python

- Nice tool for python: `pip`
    - You may need to install the system package first, normally
      called "python3-pip"
- Find python package:
    - `pip3 search <package>`
- Install:
    - `pip3 install --user <package>`
    - `--user` is important! This installs it just for you
    - **Never** use `sudo` with pip -- this is asking for a bad time
- If it's not on PyPi.org:
    - `pip3 install --user /path/to/project` -- install a local
      project
        - Add `--editable` to just make links -- useful for something
          you're developing yourself!
    - `pip3 install --user <url>` -- install from the web

# Installing software from source

- Not unusual to have to install software from source
- For C/C++/Fortran, etc., three main methods for installing:
    - The GNU/Autotools way -- probably the most common method
    - CMake -- most popular for software that can be installed on
      Windows as well
    - "no method" -- typical for smaller/really old projects

# Common steps -- downloading

- Software website *should* have installation instructions, but
  generally follow this pattern:
- Download a "tarball": `<package name>.tar`
    - Just an "archive", bunch of files wrapped up in container file
    - Might be compressed, e.g. `<package>.tar.gz`
- Unpack archive:
    - `tar --list f <file>` to check where files will be unpacked to
        - The majority of *sensible* software has a top-level directory in
          the archive (i.e. it extracts everything into a single
          folder)
    - `tar xvf <package>.tar`
        - "e**X**tract **V**erbosely **F**ile"
        - Modern `tar` can handle compressed tarballs without
          problems, older systems might need a `z` flag too
        - If it's not using a top-level directory, you'll need to
          `mkdir <package dir>` and use `tar xvf <package>.tar -C <package dir>`


# Common steps -- directory layout

- Software source directories generally look *something* like this at the top-level:

```
$ ls package/
configure  include/  INSTALL Makefile.am  README  src/
```
or this:

```
$ ls package/
cmake/ CMakeLists.txt  include/  INSTALL  README  src/
```

- The first is GNU or Autotools, second is CMake
- Read the "README" first (with e.g. `less`), followed by "INSTALL"
- One of these files should tell you if you need to install anything
  else first

# Installing dependencies

- If you have to install any dependencies, first check system package
  manager!
- Two types of dependencies:
    - Runtime, i.e. library files
    - Compile-time, i.e. header files
- Runtime dependencies are the usual ones your package manager
  installs
- Compile-time dependencies you typically need to explicitly install
  yourself
- Usually named either `package-dev` or `package-devel`
- If your system doesn't provide some/all the dependencies (or the
  correct versions), you'll have to compile them yourself
- Very important to be consistent if you have to do this!
    - Use same compiler, versions of libraries, etc. for everything

# The GNU way

- Traditional three steps:
    - `./configure`
    - `make`
    - `sudo make install`
- But what if I don't have `sudo` access?
    - `./configure --prefix=/path/to/install`
    - `make`
    - `make install`

## Tips
- Use `make -j` to compile in parallel
- Use `./configure --help` to see configuration options
- Use out-of-source build if you can (though this might not
  always work)
- Run `make check` (or `tests`) to verify the build works

# Out-of-source builds

## What?

Build the software in a separate directory to the source, e.g.:

```bash
$ mkdir build; cd build
$ ../configure --prefix=/path/to/install
$ make -j && make install
```

## Why?

1. Keeps the source tree clean
2. Makes it easy to start again -- just delete the build directory
3. Makes it possible to keep multiple different builds (e.g. debug and
   production)


# Resources

- Apt docs: https://help.ubuntu.com/lts/serverguide/apt.html
- CMake docs: https://cmake.org/
- Arch Linux wiki: https://wiki.archlinux.org
- FHS: https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard
- FHS: http://www.tldp.org/LDP/Linux-Filesystem-Hierarchy/html/c23.html
