# Lab z/OS 36: Explore USS
## Overview

You want to become more familiar with the USS environment.

## Goals

- Try a few USS commands and see what they do.

## Part 1: Navigate to your USS command line shell

Either via ssh or omvs, get into your USS command line shell.

## Part 2: Get the uname value

```shell
uname -a
``` 

## Part 3: Check the versions of a few packages 

```shell
ssh -V 
python -version
```

## Part 4: Display the contents of an MVS data set 

```shell
cat "//'sys1.parmlib(clock00)'"
```

## Part 5: Display the member list of a PDS

```shell
mls 'ibmuser.lab.jcl'
```

## Part 6: Display values assigned to z/OS system symbols 

```shell 
sysvar SYSNAME
sysvar JESNAME
sysvar DBC1MSTR
sysvar CICSTS61
sysvar TCPHOSTNAME_ 
```

System symbols or variables are defined in SYS1.PARMLIB(IEASYS00).

## Part 7: Display information about aggregates 

Aggregates are the VSM Linear Data Sets that house USS filesystems. 

```shell
zfsadm fsinfo -all
```

## Part 8: Sanity-check the sshd_config file 

```shell
sshd -dt 
```