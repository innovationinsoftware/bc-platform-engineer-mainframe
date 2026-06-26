# Lab z/OS 30: Add TSO access for the new user

## Overview

The user profile you created in the previous lab needs access to TSO.

## Goals

- Use the AlTUSER command to add a TSO segment to the user profile. 

## Part 1: Add TSO access

While signed on as yourself, at the TSO READY prompt (not inside ISPF), enter the command ALTUSER <userid> with the appropriate parameters to enable the user to access TSO. 

## Part 2: Attempt to sign on to TSO as the newly-defined user  

Sign off TSO and sign on again as the user you just defined. See what happens.