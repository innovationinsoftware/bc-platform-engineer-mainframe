# Lab z/OS 20: Write a REXX script

## Overview

REXX is frequently used in z/OS processes that install, configure, and customize software; manage the creation, movement, archiving, and renaming of data sets; and other functions applicable to system programming work. 

## Goals

- Write a REXX script and execute it from the TSO READY prompt.

## Part 1: Ensure you have a place to store REXX scripts

If you haven't already done so, allocate a source library where you will keep your REXX scripts. The library should have the same data set attributes as your other source libraries. Typical names for REXX libraries include <userid>.<something>.REXX, <userid>.<something>.EXEC, and <userid>.<something>.CLIST. 

## Part 2: Write the REXX script

Write a script that displays the time and date in the form, "It's hh:mm:ss on dd Mon yyyy". For example, "It's 17:24:24 on 13 Jun 2026". 

The IBM documentation for REXX under TSO is here: [REXX doc](https://www.ibm.com/docs/en/zos/2.1.0?topic=tsoe-zos-rexx-users-guide). 

## Part 3: Run the script at the TSO READY prompt  

Exit from ISPF but stay in TSO. At the READY prompt, run your script with the command 

ex 'hlq.mlq.libname(script)'

For example, 

ex 'IBMUSER.LAB.REXX(DATETIME)'
