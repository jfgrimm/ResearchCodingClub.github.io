---
title: Getting started with version control
subtitle: git revisited
author: Peter Hill
classoption: aspectratio=169
theme: York169dark
---

Does this seem familiar: "report.doc", "report_2.doc",
"report_final_2_for_real.doc"? If so, congratulations! You've been
using version control! But there has to be a better way, right?

This week, we revisited `git`, learning how to using version control
in a slightly more sustainable manner.

# Outline

- What is version control/git?
- Why is version control important?
- Basic git usage
- Working with others

# What is version control?

## Version Control System  (VCS)
* Version control systems record changes to a file/set of files over time
    * Not just software! This talk is under git
    * Allows you revert files back to a previous state, compare
      changes over time, see who last modified something, etc.

## Local VCS
* Naive versioning: separate file/folder for each version
* Slightly better: local database of changes

# Why is version control important?

* Tracking versions
    - Roll back to previous versions
    - See history of project/file/line
    - Find out when bugs were introduced
    - Maintain/compare different versions
* Coordination between developers
    - Easier to work on separate features
    - Easier to merge distinct changes from separate developers
    - Easier to resolve conflicts on same features
    - Tracking who made what changes

If it's not under version control, it doesn't exist!

# Centralised vs Distributed VCS

* Centralised VCSs: CVS, Subversion
    * Have a single server than contains all the versioned files
    * Can see what other people are working on
    * Easier to administer a centralised VCS than local databases on
      each client
    * If server goes down, can lose access to project history, etc.
    * If central database is lost, everything not backed-up is lost
* Distributed VCSs: git, mercurial
    * Clients don't just checkout latest snapshot of files, repository
      is fully mirrored
    * If server goes down, any client repo can be copied back to
      server to restore it
    * Multiple remote repos work pretty well

# How does git work?

## The Three States

* Important to understand correctly
* Three main states that files can be in:
    1. Committed: data stored in repo
    2. Modified: file is changed but not committed
    3. Staged: modified file marked to go into next commit

![areas](/img/areas.png)

# Basic commands

## Get started

```bash
# Initialise a bare repo
$ git init
# Add a new file
$ git add newfile
$ git commit -m "Initial commit"
# Make some changes
$ git status
$ git diff newfile
$ git add newfile
$ git commit -m "Add extra text"
```

# Branching

* Branching is the "killer feature" of git
* Very lightweight, easy to make new branch and throw away if not needed
* Need to know how commits are stored

## How does git store commits?

![commits-and-parents](/img/commits-and-parents.png)

## A branch is just a pointer to a particular commit

* HEAD is a special pointer to the current branch

![branch-and-history](/img/branch-and-history.png)

## A new branch is just a new pointer

* Changing the branch just means changing what HEAD points to

![head-to-master](/img/head-to-master.png)

## A new branch is just a new pointer

* Changing the branch just means changing what HEAD points to

![head-to-testing](/img/head-to-testing.png)

## Branches can diverge

* New commits can be made to separate branches independently

![advance-master](/img/advance-master.png)

# More basic commands

## Next steps

```bash
# Make a new branch
$ git branch branchname
# Switch to branch
$ git checkout branchname
# View history
$ git log
$ git log --oneline --graph --all
# Merge branches
$ git merge branchname
```

# Working with others

## Sharing repos

- Various third party websites to host repos:
    - GitHub
    - GitLab
    - Bitbucket
- University have command line-only service
- Shared network drive

```bash
# Get someone else's repo
$ git clone https://github.com/Username/some_repo.git
$ git remote add reponame /path/to/reponame
# Update your repo from a remote
$ git pull remotename branchname
# Update a remote from your repo
$ git push remotename branchname
# Get help
$ git help add
$ git add --help
```

## Centralised workflow

- Central "one true" repo
- Single master branch
- Useful for individual developers or small teams

## Feature branch workflow

- Central "one true" repo
- New features developed in separate branches
- Create "pull request" to request changes be merged into master
  branch

## Forking workflow

- Each developer has their own fork of the repo
- Otherwise same as Feature branch workflow
- Developers push to their own forks, then submit pull requests from there

## Gitflow workflow

- Central "one true" repo
- New features developed in separate branches
- Strict model for how branches are laid out
    - master branch
    - feature branches
    - development branch
    - "next version" branch
- Only the "next version" branch can be merged into master
- Features get merged into development branch
- "Next version" gets branched off development branch and features are frozen


# Resources

- Git book: **https://git-scm.com/book**
- Atlassian tutorial: **https://www.atlassian.com/git/tutorials**
- Codecademy: **https://www.codecademy.com/learn/learn-git**

# Acknowledgments

Some material from *Pro Git*, Second Edition written by Scott Chacon and Ben Straub and published by Apress.
Available here: **https://git-scm.com/book**


Licensed under Creative Commons Attribution Non-Commercial Share Alike 3.0 Licence.
