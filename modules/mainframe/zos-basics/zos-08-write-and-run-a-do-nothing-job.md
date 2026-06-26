# Lab z/OS 8: Write and Run a Do-Nothing Job

## Overview

We want to see how to write JCL for the simplest possible job. 

## Goals

- Write JCL that will run successfully, but do nothing.

## Prerequisites

1. Your local system is connected to the Internet

## Part 1: Use ISPF option 2 to create a member in your JCL library

Navigate to ISPF option 2 (Edit) and use the ISPF editor to enter JCL statements for a job that will run successfully, but that does nothing (that is, it doesn't create or delete or modify any data sets or display anything).

## Part 2: Submit the job 

From within the ISPF Editor, submit the JCL you wrote in Part 1.

## Part 3: Examine the spooler output from the job 

In ISPF, navigate to SDSF and locate your job output. Examine each of the three default datasets produced by JES. Ensure your minimal job actually executes and gets condition code zero. 