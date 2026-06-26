# Lab z/OS 10: Make the Job Idempotent

## Overview

Enhance the data set creation job to be idempotent.

## Goals

- Enhance your data set creation job so that it results in the same outcome no matter how many times it is executed, and whether the data set already exists or not. 

## Part 1: Modify the JCL to make the job idempotent

Make the changes necessary to your data set create job (JCL in member CRQSAM) so that the job is idempotent.

## Part 2: Verify that the job works when the target data set already exists

Ensure the data set exists, run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.

## Part 3: Verify that the job works when the target data set does not exist 

Use ISPF Option 3.2 to delete the target data set. Run the job, check the spooler output for success and for messages indicating the data set was created, and verify it was created.
