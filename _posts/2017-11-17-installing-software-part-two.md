---
title: Installing Software on Linux
subtitle: Part Two
author: Peter Hill
tags: Linux software
---

Last week, we started looking at installing software for
ourselves. We pick it up again this week, taking it a bit further,
looking at common ways things can go south, and some general tips and
methods for solving these problems.

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

# What's going on here?

## `./configure`

- Purpose is to make compilation "portable" -- i.e. work on many
  different systems, abstract over:
    - different compilers
    - different shells
    - different implementations of features
    - different hardware
- Allows user to choose between options
- Tries to find dependencies
    - Different distros might install things in different locations
- Creates `Makefile` from a template, usually with hardcoded paths
  found during running `configure`

# What's going on here?

## `make`

- Compile the software
- There may be additional/optional "targets" you can also build -- see
  the README/INSTALL files for information

## `make install`

- Copy the compiled software to the installation directory (specified
  with `--prefix` to `configure`
    - You can also use `make DESTDIR=/path/to/install install` to
      install in a different place than `prefix`
    - This will actually install it under `/path/to/install/usr/local`
        - Due to hardcoded paths set during configure stage

# The GNU way -- dependencies

- Running just `./configure` normally finds everything that it *needs*
  without any extra input
- Sometimes want optional features
- Sometimes can't find dependencies
- Usually 2-3 ways of tell `configure` to use an optional package or
  where to find a needed dependency:
    - `--with-<package>` -- will try and use some built-in method of finding
      optional `package`
        - Typically looks for standard names under `/usr/` or
          `/usr/local`
        - Might be more clever and use `pkg-config` (see later)
        - Might check environment variables
    - `--with-<package>=/path/to/install` -- use this if it still
      can't find `package`
    - `--with-<package>-libdir=/path/to/lib`
      `--with-<package>-include=/path/to/include` -- use these if
      `configure` is looking for some exact path, but `lib/` and
      `include/` are in different places

# The GNU way -- environment variables

- Running `./configure --help` should also list "Some influential
  environment variables":
    - Which compiler to use: `CC`, `CXX`, `FC`
    - Extra compiler flags: `CFLAGS`, `CXXFLAGS`, `FFLAGS`
    - Extra linking flags: `LDFLAGS`, `LDLIBS`, `LIBS`
    - Preprocessor flags: `CPPFLAGS`
- These allow you to be extra specific about how to compile the
  software

# Oh no, something's gone wrong!

## Find the error first

- `configure` produces `config.log` by default
    - Unfortunately, jumping straight to the end won't show you the
      last error -- it's a bunch of useless output!
    - Instead, `grep -ni error config.log` to find line numbers
      containing the word "error" or "ERROR"
    - Then, `less config.log` followed by `g N` to go to line `N`
- `make` doesn't produce logs by default, so instead do:
    - `make | tee make.log` -- `tee` writes to screen and to file
    - Error should be at bottom

# Typical problems

- Wrong options to `configure` (e.g. wrong `prefix`, missed optional
  feature you wanted)
    - Start again! If out-of-source, you can just `rm -r <build dir>`
      and start again
    - Otherwise, run `make distclean` (if `configure` worked
      successfully) -- this should clean up **everything** created
      during the configure process
    - In general, if you need to change an option to `configure`, you
      need to start completely afresh
- Missing dependency
    - Should be obvious from `configure` output or reading
      `config.log`
    - Bad software will assume a dependency can always be found
    - Solution: install it! Check package manager first before trying
      to do it manually

# Typical problems

- Unsupported version of dependency (i.e. software doesn't work with
  this version)
    - `configure` will hopefully tell you!
    - Otherwise, can be tricky to even diagnose if documentation isn't
      explicit about version numbers
    - Typically, looks like mismatch in function signatures or object
      definitions at compile time -- check output of `make`
    - Solution: install it! Might be more difficult if you first need
      to establish *which version*
        - Probably going to need to compile and install yourself!
- Wrong version of dependency (i.e. not the version *you* wanted to
  use)
    - You make have to be very explicit and use
      `--with-<package>=/path/to/version`
    - Possibly also need to set `CFLAGS`/`CPPFLAGS`, etc.

# Typical problems

- Couldn't find `<file>`
    - Could be either at configure-time or compile-time
    - Might just be in a weird place:
        - `locate <file>` -- uses database to quickly find files
        - Otherwise use `find / -type f -name <file>` -- this will be
          **slow**
        - Then tell `configure` where it is
    - Might be because dependency is the wrong version
        - Or compiled without a feature
    - Might be named differently
        - Symlinking to the rescue!
        - Make a link to the installed version, but with the expected
          name, and then point `configure` at your link
    - If compile-time (`cannot find -l<foo>`), then either:
        - one of the above
        - You need to add actual install path to `LD_LIBRARY_PATH` variable

# CMake

- Traditional four steps:
    - `mkdir build && cd build`
    - `cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/install`
    - `make -j`
    - `make install`

## Tips
- CMake always works with out-of-source builds, so you should *always*
  use them!
- Use `ccmake` or `cmake-gui` to discover configure-time options
- Press `t` in `ccmake` to see advanced options and set paths, etc.
- CMake doesn't make log files by default: use `tee` to record output to a log file
- Typical problems similar to `configure`

# The "no method" method

- Typical for smaller projects
- Read all the documentation provided
- Even in this state, it's probably at least got a Makefile
- Look for `CC`, `CXX`, `FC`, `F77` variables in the Makefile -- these set
  the C, C++ and Fortran compilers
    - You might need to check to see if it's going to parse these
      variables and only work for certain compilers
    - Particularly bad projects will call this something like `COMPILER`
- Look for `CFLAGS`, `CXXFLAGS`, `FFLAGS` variables -- these set compiler options
    - These are where you'll tell the compiler about where
      include files (headers/.mod files) are located
- Look for `LDFLAGS` -- this sets linker options
    - Where library files are located

# How do I know what flags I need to use a dependency?

- Read the README!
- Some software uses `pkg-config`:
    - `pkg-config --list-all | sort` to see alphabetical list of
      packages
    - `pkg-config --libs <package>` for libraries (i.e. `-lpackage`
      flags)
    - `pkg-config --cflags <package>` for include paths and other
      flags
    - If you know a package installs a `<package>.pc` file, then you
      can set `PKG_CONFIG_PATH=/path/to/pkgconfig/dir` (normally found
      under `/path/to/package/lib/pkgconfig`)
- Other software (e.g. NetCDF, HDF5) provide their own config tools
  (e.g. `nc-config`, `h5cc -show`)
- Otherwise, find out what files a package uses:
    - If system package, you can use either `dpkg -L <package>` or
      `rpm -ql <package>` to list files installed by a package


# What to do after installation

- Usual layout of an installation directory:
    - `bin/` -- for executables
    - `include/` -- for headers
    - `lib/` -- for libraries
    - `share/` -- for data/configuration files
- Default install location is `/usr/local`
    - Probably won't need to do very much more if installing here
- Custom install location, you'll then need to tell everything else
  where you've installed it
- Helpful environment variables for runtime:
    - `$PATH` -- location of `bin/`
    - `$LD_LIBRARY_PATH` -- location of `lib/`
- When compiling:
    - `-I/path/to/include/` in `CFLAGS`/`CXXFLAGS`/`FFLAGS`
    - `-L/path/to/lib/` in `LDFLAGS`

# Help! It's installed but won't run!

- Command not found:
    - Check your `$PATH`: is the install location in it?
    - Use `locate <file>` to check install location
- `error while loading shared libraries: lib<foo>... No such file`
    - Use `ldd <executable>` to see what libraries it needs
    - Missing libraries look like `lib<foo> => not found`
    - Check your `$LD_LIBRARY_PATH`: is the install location in it?

# Best practices when installing software

- *Always* use out-of-source builds when you can -- saves many headaches!
- Even if you have `sudo` rights, not always a good idea to install
  stuff centrally on your own machine
    - Might not play well with multiple versions
    - Might hide/shadow important system packages
- Instead, install in e.g. `~/Tools` or `~/local`
- Name things like: `package-version-compiler-version`
    - e.g. flat: `netcdf-4.4.1-gcc-5.4`
    - or nested: `netcdf-4.4.1/gcc-5.4`
- Then you can change your `PATH` and `LD_LIBRARY_PATH` to point to
  the correct version
- Expert level: set up an "environment module" system to manage
  multiple versions for you


# Thanks!

- Resources:
    - Apt docs: https://help.ubuntu.com/lts/serverguide/apt.html
    - CMake docs: https://cmake.org/
    - Arch Linux wiki: https://wiki.archlinux.org
    - FHS: https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard
    - FHS: http://www.tldp.org/LDP/Linux-Filesystem-Hierarchy/html/c23.html
