# Lab z/OS 12: Create a model DSCB for source libraries

## Overview

This is the second in a series of small Lab exercises with the end goal of having a single batch job that can provision all the libraries needed by a hypothetical software developer in our hypothetical company.

## Goals

- Enhance the source library allocation job to use a model DSCB for DCB parameters.

## Part 1: Allocate a model DSCB

Copy and modify your DSCB creation job so that it specifies attributes suitable for a source Library (PDSE).

Modify your library allocation job from Lab 11 to refer to the model DSCB instead of hard-coding the DCB parameters on the DD statements.

## Part 2: Verify that the job works when the target data set already exists

Ensure the data set exists, run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.

## Part 3: Verify that the job works when the target data set does not exist 

Use ISPF Option 3.2 to delete the target data set. Run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.
