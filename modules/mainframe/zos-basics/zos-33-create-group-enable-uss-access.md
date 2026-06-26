# Lab z/OS 33: Create a RACF group; enable USS access for RACF user
## Overview

The new user would like to work with USS.

## Goals

- Use RACF commands to create a group, add a user to it, make the group the user's default group, and enable USS access for the user

## Part 1: Create RACF group for developers

While signed on as yourself, at the TSO READY prompt (not inside ISPF), enter the appropriate RACF commands to create a group named DEV, connect your new user to that group, make DEV the user's default group. Then use ALTUSER to add an OMVS segment to the user's RACF profile so they can make use of USS on the system.

## Part 2: Attempt to sign on to USS as the newly-defined user  

Sign off TSO and sign on again as the user you just defined. Navigate to TSO Option 6 and enter **omvs** to start the USS command shell.