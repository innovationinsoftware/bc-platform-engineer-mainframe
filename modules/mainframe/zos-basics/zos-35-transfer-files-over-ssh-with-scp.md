# Lab z/OS 35: Transfer files over ssh with scp
## Overview

You want to copy files between z/OS USS and your local system.

## Goals

- Create a file on USS and copy it to your local system.
- Create a file on your local system and copy it to USS.

## Part 1: Create a file on USS and copy it to your local system

Either via ssh or omvs, create a trivial file in your USS home directory on z/OS. Example:

```shell
cd 
ssh you@ipaddress
echo "test" > test.txt
exit
``` 

Copy the file to your local system. Example:

```shell
scp you@ipaddress:test.txt . 
``` 

Verify the copied file has the same contents as the original file. Example:

```shell 
cat test.txt
```

## Part 2: Create a file on your local system and copy it to USS 

Follow steps similar to Part 1, but this time the source file is on your local system and the destination file is on USS. 

## Part 3: Copy a PDS member to USS and then to your local system

Sign on to USS. 

Use **cp** to copy a PDS member of your choosing to your USS home directory. 

Use **scp** to copy the same file to your local system. 

Verify the contents are the same as the original. 

## Part 4: Create a file on your local system and copy it to a PDS on your z/OS account

Create a text file on your local system that is suitable for a PDS of your choosing, such as a program source library or JCL library or parmlib. 

Use **scp** to copy the file to your USS home directory. 

Sign on to USS and use **cp** to copy the file to your PDS. 

Verify the PDS member has the same contents as the original file. 
