# Lab z/OS 20: Write a USS shell script

## Overview

USS is the entry point for external tools used for managing, configuring, monitoring, and automating tasks on z/OS systems. Many configuration scripts and batch jobs include a combination of MVS and USS tools and resources. Basic Unix-style shell scripts are widely used.  

The USS environment that ships with z/OS is basic. The shell is the basic shell, not bash or zsh or anything else. The editor is vi. There's no command history. The shell lives in /bin/sh. The man command is installed. You can find comprehensive IBM documentation about USS online. 

## Goals

- Write a USS shell script and execute it from a USS command line.

## Part 1: Write a shell script

Write a script that displays the time and date in the form, "It's hh:mm:ss on dd Mon yyyy". For example, "It's 17:24:24 on 13 Jun 2026". 

Remember to make the script executable using chmod.

The IBM documentation for USS is here: [USS doc](https://www.ibm.com/docs/en/zos/2.1.0?topic=services-zos-unix-system-users-guide). 

## Part 2: Run the script from a USS command line.  

You can run your script using ishell, omvs, or an ssh connection to z/OS. 

