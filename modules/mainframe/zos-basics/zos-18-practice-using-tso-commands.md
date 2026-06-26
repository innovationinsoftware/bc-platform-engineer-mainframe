# Lab z/OS 18: Practice using TSO commands

## Overview

Using an off-platform system administration tool such as Ansible, you can work with z/OS instances in a number of ways. You can submit JCL such as the JCL you've been writing. You can also run individual TSO commands such as you might enter at the TSO READY prompt (outside of ISPF). The choice depends on which approach makes more sense in a given context.

## Goals

- Get a general sense of how TSO commands look and feel, especially those equivalent to the functions your provisioning job stream performs.

## Part 1: Exit from ISPF but not from TSO

Our lab environment is configured to start ISPF automatically after you've entered your sign on credentials. To get to the bare-bones TSO READY prompt, exit from ISPF by entering "X" in the Command field on the Primary Option Menu. If you're prompted to do something with your ISPF log file, choose "delete" and press Enter.

## Part 2: Play with TSO commands to allocate and free data sets

Explore the TSO commands you would issue to allocate a new source code library (PDSE). This is the same functionality as a JCD DD statement with DISP=(NEW...). The name of the command is ALLOCATE. It can be abbreviated as ALLOC. To get help, enter HELP ALLOC.

To delete the existing library before allocating a new one, use the TSO command DELETE. It can be abbreviated as DEL. To get help, enter HELP DEL.

To copy members from a seed library into target libraries, use the TSO command OCOPY. To get help, enter HELP OCOPY.

You can do an Internet search to find the relevant IBM documentation, community resources such as discussion boards, and social media resources such as Reddit. ChatGPT or Duck.ai or similar LLM-based resources may also be useful, although they are often wrong about mainframe-related topics. 

