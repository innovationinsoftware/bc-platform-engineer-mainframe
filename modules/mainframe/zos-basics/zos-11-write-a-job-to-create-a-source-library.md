# Lab z/OS 11: Write a job to create a source library

## Overview

This is the first in a series of small Lab exercises with the end goal of having a single batch job that can provision all the libraries needed by a hypothetical software developer in our hypothetical company.

## Goals

- Allocate a Library with attributes suitable for storing JCL members.

## Part 1: Set up JCL for a job to create a JCL Library

Copy and modify your data set creation JCL so that it allocates a Library (PDSE) with attributes suitable for storing members that contain 80-column card-image records, such as JCL, program source statements, scripts, or configuration files.

Name the library according to the data set naming conventions defined for these lab exercises. Name it appropriately for a "dev" JCL Library. Use your own z/OS userid as the high-level qualifier (HLQ) for the data set name. Use DEV as the mid-level qualifier.

Don't get fancy...yet.

## Part 2: Verify that the job works when the target data set already exists

Ensure the data set exists, run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.

## Part 3: Verify that the job works when the target data set does not exist 

Use ISPF Option 3.2 to delete the target data set. Run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.
