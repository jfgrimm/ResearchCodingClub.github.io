---
title: Working with remote computers
subtitle: SSH tips and tricks
author: Peter Hill
---

Often, we need to use computers other than the one currently sat on
our desk, for instance in order to do some really heavy
calculations. To access remote machines, the tool of choice is
`ssh`. This week we take a dive into exploring how `ssh` works, and
some tips and tricks to make using remote machines that bit easier.

# Outline

- How to access remote computers
- SSH config
- Password-less connections
- Graphical connections
- Gateways
- Transferring files
- SSH from Windows

# Accessing remote computers

## Old school: telnet

- Data sent unencrypted, even username/password!
- Trivial to "sniff" credentials
- Zero security

## ssh: Secure SHell

- Data sent encrypted, choice of encryption algorithms
- Very hard to crack

# How does ssh work?

- Diffie-Hellman key exchange to generate a shared secret
    - Uses asymmetric encryption
    - An interesting video on how Diffie-Hellman key exchange works:

<iframe width="420" height="315" src="https://www.youtube.com/embed/YEBfamv-_do" frameborder="0" gesture="media" allowfullscreen></iframe>

- Use shared secret to encrypt rest of session
    - Uses symmetric encryption



- Instead of sending password, can use ssh key pairs
    - Offers much better protection

# Basic connections

    ssh username@remote.computer

- ssh offers some protection for verifying the remote host is what it
  says it is.
- On first time connecting to a computer, ssh prints a message like:

```
$ ssh ph781@research1.york.ac.uk
The authenticity of host 'research1 (144.32.196.129)' can't be established.
ECDSA key fingerprint is SHA256:DS1JXxFzIBORiQjQKsXMuAOJXcY5LJwe+yS7oS6vJh0.
Are you sure you want to continue connecting (yes/no)?
```

- On subsequent connections, ssh can then check if a computer is the
  same as the one you previously connected to
- If it's changed, you'll see something like:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
96:92:62:15:90:ec:40:12:47:08:00:b8:f8:4b:df:5b.
Please contact your system administrator.
Add correct host key in /home/username/.ssh/known_hosts to get rid of this message.
Offending key in /home/username/.ssh/known_hosts:10
RSA host key for arvo.suso.org has changed and you have requested strict
checking.
Host key verification failed.
```

- Important to read these messages!
- Usually a good reason for this: OS has changed, IP address has
  changed, etc.

# SSH Config

- Can be annoying to type long hostnames
- Normally use same username on a given hostname each time
- Easy way to set up custom hosts:

File: `~/.ssh/config`:
```aconf
Host yarcc
     HostName login.yarcc.york.ac.uk
     User ph781
```
- If you don't already have the directory `~/.ssh`, create it and make
  sure only *you* can read it:

```
$ mkdir ~/.ssh
$ chmod 700 ~/.ssh
```

# Password-less connections

    ssh-keygen

- Can choose different types of SSH key pairs to generate
    - Default is RSA, based on difficulty of factoring large primes.
      Most widely supported
    - For stronger encryption, choose ed25519, based on elliptic curve
      logarithms. Less widely supported though

- For RSA, can also specify number of bits (default is 2048) with
  `-b`, e.g. `ssh-keygen -b 4096`
- Add a comment with `-C`, e.g. `ssh-keygen -C my.email@example.com`
- Will ask you for a passphrase -- choose something nice and strong!
    - Easiest way to pick a strong passphrase:
        - 4-5 random words
        - separated by random characters and numbers
        - e.g. `Many$Astronomical89dogs`

# Password-less connections

    ssh-copy-id user@host

- Copies your key onto the remote host
- You can then ssh using your key!
- But wait... we still need to type in the passphrase every time?!
- `ssh-agent` to the rescue! Caches decrypted keys to pass to ssh
  sessions

```
eval $(ssh-agent)
ssh-add
```

- Run once, then add keys to the agent -- remembers the keys for the
  whole of the login session
- Works with both GNOME and KDE wallets:
    - GNOME: https://wiki.archlinux.org/index.php/GNOME/Keyring
    - KDE: https://en.opensuse.org/SDB:Ssh-agent_KDE_Wallet

# Password-less connections with University managed Linux systems

- IT managed Linux uses Kerberos for authentication and to mount
  network drives
- Once authenticated, you get a Kerberos ticket for 10 hours
    - Can be renewed for about a week
- Requires your actual password to have been entered at some point
- Make sure you have `kinit` installed (usually found in `krb5-client`
  or `krb5-user` package)
- To set up on your computer, add the following to SSH config file:

```aconf
Host *.its.york.ac.uk
     GSSAPIAuthentication yes
     GSSAPIDelegateCredentials yes
```

## `/etc/krb5.conf`

```ini
[libdefaults]
        default_realm = YORK.AC.UK
    forwardable = true

[realms]
    YORK.AC.UK = {
               kdc = auth.york.ac.uk auth0.york.ac.uk \
                     auth1.york.ac.uk auth2.york.ac.uk
      admin_server = authm.york.ac.uk
    }

```

- `kinit -p <username>` to get a kerberos ticket, and then
  password-less access to University machines!
- Only need to enter password once a day... but still need to remember
  to run `kinit`...
- For GNOME: install `krb5-auth-dialog` to handle this automatically
- For KDE: `kerberosKWallet.sh` from https://github.com/rnc/kde-scripts

# Graphical sessions

    ssh -X user@host

- Forward X11 over ssh in order to open graphical programs
- Some security concerns, but generally you will connecting to a
  "secure" machine, so not a problem
- Common error: `Error: no display specified`
- Fix: `export DISPLAY=:0.0` on your local machine
    - Then try `echo $DISPLAY` after ssh, should be
      e.g. `localhost:10.0`
- Can add `ForwardX11 yes` under a `Host` section in `~/.ssh/config`
  to always enable X11 forwarding for a particular (or all) host


- X11 over ssh can be quite slow
- Solution: x2go (https://wiki.x2go.org)
- Directly launches a graphical login session
- (Usually) much faster!
- Works from Windows, Linux, Mac

# Gateways and tunnels

- When connecting from off-campus, need to go through `ssh.york.ac.uk`
  and type the name of the machine you want to connect to
- Can be annoying to connect multiple times
- Luckily, ssh can "tunnel" through gateways:

```
ssh -L 9999:<host>.york.ac.uk:22 <username>@ssh.york.ac.uk
```

- `-L` forwards a local port (9999) to a remote port (22) on `host`
- You can then connect directly to `host` by specifing the port with `-p`:

```
ssh -p 9999 <username>@localhost
```

# Transferring files

## Simple

- `scp [user1@host1:]/path/to/source [user2@host2:]/path/to/dest`
- You can omit either/or `user1@host`/`user2@host2` to mean
  "localhost"

## Mounting with sshfs

- `sshfs user@host:/remote/path /local/path`
- Makes the remote path appear like a local directory
- Unmount with `fusermount -u /local/path`

## Robust backup solution

- `rsync -aAvzP [user1@host1:]/path/to/source
  [user2@host2:]/path/to/dest`
- `rsync` can just copy those files that changed -- save time and
  bandwidth!
- Probably best/easiest tool to keep a backup synced
- Can show progress

# SSH from Windows

- Windows Subsystem for Linux
    - Built-in, basically full-ish Linux system
    - Need to run a separate X server (e.g. Xming) for graphical
      applications
- PuTTY
    - Very basic, but functional
    - Still need a separate X server
    - Painful to make work with Kerberos
- MobaXterm
    - Everything you need in one package
- WinSCP
    - Graphical scp application
- x2go
    - Painless graphical session!

# Resources

- Arch wiki:
    - https://wiki.archlinux.org/index.php/SSH_keys
    - https://wiki.archlinux.org/index.php/Secure_Shell
- http://www.slashroot.in/secure-shell-how-does-ssh-work
- https://wiki.york.ac.uk/display/ISD/Linux+Managed+Desktop+-+User+FAQ
