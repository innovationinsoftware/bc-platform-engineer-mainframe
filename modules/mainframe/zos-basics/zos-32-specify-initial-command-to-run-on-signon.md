# Lab z/OS 32: Specify an initial command to run automatically upon sign-on

## Overview

The new user would like ISPF to start automatically when they sign on to TSO.

## Goals

- Use the AlTUSER command to add an initial command to the user profile.

## Part 1: Add TSO initial command

While signed on as yourself, at the TSO READY prompt (not inside ISPF), enter the command ALTUSER <userid> with the appropriate parameters to specify an initial command in the TSO segment of the user profile.

## Part 2: Attempt to sign on to TSO as the newly-defined user  

Sign off TSO and sign on again as the user you just defined. See what happens.