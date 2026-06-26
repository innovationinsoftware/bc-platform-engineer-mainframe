# Lab z/OS 9: Write and Run a Job that Creates a Sequential Data Set

## Overview

We can create data sets either through ISPF panels or through JCL.

## Goals

- Enhance your do-nothing job so that it allocates a new sequential data set. 

## Part 1: Create a new member in your JCL Library named CRQSAM

Navigate to ISPF option 2 (Edit) and use the ISPF editor to enter JCL statements for a job that will run successfully, but that does nothing (that is, it doesn't create or delete or modify any data sets or display anything)

## Part 2: Add a DD statement to the job step that defines a new sequential data set

Give the data set the following attributes:
- Data Set Organization: Physical Sequential 
- Record Format: Fixed, Blocked
- Logical Record Length: 80 
- Block Size: 16000 
- Space Allocation: 5 tracks primary, 2 tracks secondary

## Part 2: Submit the job 

From within the ISPF Editor, submit the JCL you wrote in Part 2.

## Part 3: Examine the spooler output from the job 

In ISPF, navigate to SDSF and locate your job output. Examine each of the three default datasets produced by JES. Ensure the job completed successfully and allocated the data set.

## Part 4: Double-check the data set attributes 

Use ISPF panels to display the data set information for the new data set. Check that the attributes match what you intended to define in the JCL.