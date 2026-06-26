# Lab z/OS 16: Set up a one-shot provisioning job

## Overview

This is the sixth in a series of small Lab exercises with the end goal of having a single batch job that can provision all the libraries needed by a hypothetical software developer in our hypothetical company.

## Goals

- Set up a single job that allocates all the libraries needed in a standard application developer environment in our hypothetical company. Setting up the provisioning job in this way facilitates automation of the process using on-platform or off-platform automation tooling.

## Part 1: Set up the provisioning job stream

Create a new member in your JCL library and use ISPF Editor commands to copy in the JCL from your source library and program library allocation jobs. Break up the source library allocation jobs into multiple pieces (each a copy of the same JCL) that allocate some reasonable (in your opinion) number of libraries each, so that some of the processing can be concurrent.  

## Part 2: Spot-check some of the libraries to see that they were allocated with the right attributes

You're assembling pieces of JCL that you've already verified works, so there's no need for extensive testing here.

