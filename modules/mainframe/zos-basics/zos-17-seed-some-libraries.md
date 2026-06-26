# Lab z/OS 17: Seed some libraries

## Overview

This is the seventh in a series of small Lab exercises with the end goal of having a single batch job that can provision all the libraries needed by a hypothetical software developer in our hypothetical company.

## Goals

- Add job steps in appropriate jobs in your provisioning job stream that copy default members to selected developer libraries after the libraries have been allocated.

## Part 1: Define "seed" libraries and populate them with default members

Allocate source libraries to be used as the "source" to copy default members into the DEV libraries you have created for a newly-hired application developer. At your discretion, allocate one or more libraries to contain sample members. If you want to create sample members yourself, that is fine. 

As a Platform Engineer, you aren't expected to get into great depth with these tools, so you can use the sample members provided in the course repository in directory /zos/samples/seeds. There is no need to flesh out a complete set of default members for every possible DEV library. The point is to learn _how_ to do this. You can upload the provided samples _via_ your 3270 emulator.

## Part 2: Write JCL to execute IEBCOPY to populate DEV libraries with default members

Write JCL similar to the example given in the presentation. Use the IBM documentation, online examples, LLM queries, and/or the error messages you get to help you with syntax. Also help each other. This is not a contest.

Place IEBCOPY steps at appropriate points in your provisining job stream. Run the job stream until it seems to be working. 

## Part 3: Verify that the default members were copied as expected

Check the DEV libraries where you intended to put default members and verify the members you expected to be copied are there, and others are not there. 

