# Lab z/OS 21: Run REXX from TSO batch

## Overview

TSO commands can be run in batch mode by executing program IKJEFT01, which emulates a terminal by using data set SYSTSIN to simulate terminal input, and data set SYSTSPRT to receive terminal output. This is how REXX is often executed in the context of jobstreams that perform software installation, update, and configuration tasks. 

## Goals

- Write a jobstream to execute your time-and-date REXX script in batch mode.

## Part 1: Write JCL to run your REXX script in batch mode using IJKEFT01.

Write JCL to execute program IKJEFT01 and pass it the same TSO command you used in Lab 20 to execute your time-and-date REXX script. Examine the output in SDSF. 
