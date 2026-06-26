# Lab z/OS 14: Refactor your provisioning job

## Overview

This is the fourth in a series of small Lab exercises with the end goal of having a single batch job that can provision all the libraries needed by a hypothetical software developer in our hypothetical company.

## Goals

- Refactor the provisioning job to make it shorter, cleaner, and easier to live with.

## Part 1: Apply step-by-step refactorings

Modify your library allocation job from Lab 13 along the lines that were demonstrated in the presentation. Create a PROCLIB if you don't already have one (don't use your existing JCL library for PROCS). Place the PROC you ultimately develop in the PROCLIB and refer to it in your provisioning job.

## Part 2: Verify that the job works when the target data sets already exist

Ensure the data set exists, run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.

## Part 3: Verify that the job works when one or both the target data sets do not exist 

Use ISPF Option 3.2 to delete one or both of the target data sets. Run the job, check the spooler output for success and for messages indicating the data set was created, and verify both data sets were created. Test different scenarios; e.g., TST library exists, DEV library exists, both exist, neither exists.

## Part 4: Add steps in the provisioning job to allocate the remaining developer source libraries

Refer to the list of developer source libraries in the course materials and add steps to provision all of them. Use your own userid as the high-level qualifier for these data sets.

Remember that the *.*.PROGLIB libraries are for executables, not source. They will have different attributes. That will be the next lab exercise.