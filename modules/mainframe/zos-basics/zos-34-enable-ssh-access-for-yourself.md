# Lab z/OS 34: Enable ssh access for yourself
## Overview

You want to connect to the z/OS system using your lab userid.

## Goals

- Given a working TCP/IP configuration on the z/OS system, you copy an authorized_keys file from a userid that is already set up and enable ssh access for your own userid.

## Part 1: Copy files and set ownership and permissions

Sign on as yourself and navigate to ISPF Option 6. Enter **omvs** to start the USS command shell.

In your home directory (e.g., /u/plat14) create directory .ssh. Copy an authorized_keys file from a user directory that's already set up correctly to your new .ssh directory. Example:

```shell
cd 
mkdir .ssh
cd .ssh
cp /u/plat01/.ssh/authorized_keys . 
``` 

Make yourself the owner of your home directory, the .ssh directory, and the authorized_keys files. 

```shell 
cd
chown plat14 /u/plat14
chown plat14 .ssh
chown plat14 .ssh/authorized_keys 
``` 

Set minimal permissions for the .ssh directory and authorized_keys file.

```shell 
cd
chmod 700 /u/plat14 
chmod 700 .ssh
chmod 600 .ssh/authorized_keys
```

## Part 2: Attempt to sign on to USS via ssh  

Sign off the z/OS system and attempt to connect via ssh. Example:

```shell
ssh plat14@173.45.66.189
```