# Lab z/OS 31: Remove values from a user profile

## Overview

The new user profile contains setting for which the user isn't authorized.

## Goals

- Use the AlTUSER command to remove or negate values in a user profile.

## Part 1: Add TSO access

While signed on as yourself, at the TSO READY prompt (not inside ISPF), enter the command ALTUSER <userid> with the appropriate parameters to negate the ACCTNUM and PROC settings.

## Part 2: Attempt to sign on to TSO as the newly-defined user  

Sign off TSO and sign on again as the user you just defined. See what happens.