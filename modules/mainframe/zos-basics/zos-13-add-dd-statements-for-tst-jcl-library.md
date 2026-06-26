# Lab z/OS 13: Add DD statements for the TST JCL library

## Overview

This is the third in a series of small Lab exercises with the end goal of having a single batch job that can provision all the libraries needed by a hypothetical software developer in our hypothetical company.

## Goals

- Build on the source library allocation job to create both the DEV and TEST JCL libraries.

## Part 1: Allocate the TST JCL library

Modify your library allocation job from Lab 12 to create the TST JCL library. Add a DD statement under the CLEANUP step and another under the ALLOC step to delete and allocate <userid>.TST.JCL.

## Part 2: Verify that the job works when the target data sets already exist

Ensure the data set exists, run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.

## Part 3: Verify that the job works when one or both the target data sets do not exist 

Use ISPF Option 3.2 to delete one or both of the target data sets. Run the job, check the spooler output for success and for messages indicating the data set was created, and verify both data sets were created. Test different scenarios; e.g., TST library exists, DEV library exists, both exist, neither exists.
