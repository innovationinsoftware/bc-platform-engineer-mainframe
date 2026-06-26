# Lab z/OS 15: Write a job to create program libraries

## Overview

This is the fifth in a series of small Lab exercises with the end goal of having a single batch job that can provision all the libraries needed by a hypothetical software developer in our hypothetical company.

## Goals

- Create program libraraies <userid>.DEV.PROGLIB and <userid>.TST.PROGLIB

## Part 1: Create a new job

Create a job similar to the one you have for creating source libraries, but for creating program libraries. 

Easy way:

- Use ISPF Editor commands to create a model DSCB allocation job based on the one you have for source libraries.
- Create a PROC based on the one you have for allocating source libraries and modify it to allocate program libraries instead.
- Create a job based on the one you have for allocating source libraries and modify it to call the new PROC instead.

## Part 2: Verify that the job works when the target data sets already exist

Ensure the data set exists, run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.

## Part 3: Verify that the job works when one or both the target data sets do not exist 

Use ISPF Option 3.2 to delete one or both of the target data sets. Run the job, check the spooler output for success and for messages indicating the data set was created, and verify both data sets were created. Test different scenarios; e.g., TST library exists, DEV library exists, both exist, neither exists.

