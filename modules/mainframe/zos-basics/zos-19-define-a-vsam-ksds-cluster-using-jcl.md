# Lab z/OS 19: Define a VSAM KSDS cluster using JCL

## Overview

VSAM is a sophisticated access method that manages four types of VSAM data sets as well as Generation Data Groups (GDGs). Basic knowledge of VSAM, and basic proficiency using the IDCAMS utility program, are necessary for Platform Engineering work that involves z/OS.

## Goals

- Write a job that uses the IDCAMS utility to define a VSAM KSDS cluster.

## Part 1: Write the JCL

Develop a job stream based on the example shown in the presentation and on information found in IBM documentation and Internet searches. Delete the cluster. If the return code from the Delete is 8, it means the cluster did not exist. You want your job to continue in that case. If the return code from the Delete is 0, it means the Delete operation succeeded. Code the Define command to run if the return code from Delete was less than 9. Run the job.

## Part 2: Verify that the KSDS was catalogued

Use ISPF option 3.4 to locate the catalog entry for the new KSDS and to view catalog information.
