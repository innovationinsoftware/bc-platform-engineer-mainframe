# Lab z/OS 23: Run USS shell script from batch

## Overview

USS shell scripts (and commands and programs) can be run in batch mode by executing program BPXBATCH. The command line or lines can be passed via the STDIN DD statement or via a PARM parameter on the JCL EXEC statement. The latter method is the more common for one-liners. BPXBATCH supports DDNAMES STDIN, STDOUT, and STDERR. They mean what they appear to mean. Direct the output from your script to SYSOUT using the STDOUT DD statement. 

## Goals

- Write a jobstream to execute your time-and-date shell script in batch mode.

## Part 1: Write JCL to run your REXX script in batch mode using BPXBATCH.

Write JCL to execute program BPXBATCH and pass it the same command line you used in Lab 22 to execute your time-and-date shell script. Direct STDOUT to SYSOUT. Examine the output in SDSF. 
