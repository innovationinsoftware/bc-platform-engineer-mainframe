# Lab z/OS 29: Create a new user profile

## Overview

As a Platform Engineer, your RACF userid should be set up with the authority to create new users.

## Goals

- Use the ADDUSER command to create a new user profile. 

## Part 1: Create a user profile for a (hypothetical) software developer

While signed on as yourself, at the TSO READY prompt (not inside ISPF), enter the command ADDUSER <userid> with the appropriate parameters to make the owner "ibmuser" and the default password "newpass". The userid should be "dev" plus the number at the end of your userid plus another two-digit number. As this is the first developer you're defining, make it "01." So, if your userid is plat12, the new userid will be dev1201.

## Part 2: Attempt to sign on to TSO as the newly-defined user  

Sign off TSO and sign on again as the user you just defined. See what happens.