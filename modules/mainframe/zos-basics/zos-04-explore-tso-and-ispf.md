# Lab z/OS 4: Explore TSO and ISPF

## Overview

The standard IBM documentation will be your go-to source of information about z/OS and its facilities and tools. You will find it useful to have a basic understanding of where the documentation is located, what kinds of information it contains, how it's organized, and IBM's style for writing technical documentation.

## Goals

- Get a feel for how TSO behaves when you enter commands at the READY prompt.
- Learn how to cancel the current TSO command when it becomes confused or stuck.
- Learn how to start ISPF from the READY prompt.
- Learn how to change the colors of text for your ISPF session. 

## Prerequisites

1. Your local system is connected to the Internet

## Part 1: Sign on to TSO and exit from ISPF to get to the TSO READY prompt

Your usual sign on procedure takes you into the ISPF environment. To get to the TSO READY prompt, enter an X in the command field of the ISPF Primary Option Menu and press Enter. 

## Part 2: Try some TSO commands

You might have to (a) experiment, (b) find the documentation, or (c) ask an LLM for assistance to identify the correct TSO commands.

1. Display help for TSO commands. 

2. Display the current date and time. 

3. Display your own TSO profile. 

4. List the data set names of all data sets under your TSO ID. 

5. Start ISPF. 

## Part 3: Explore ISPF panels and options 

ISPF Option 6 goes to the ISPF Command Shell panel. There, you can enter TSO commands without having to exit from ISPF. Try a couple of the TSO commands you've learned. 

Use the Help feature to find out how to change the color settings for your ISPF session. Try changing the default colors to different values to see how the display looks. Leave the colors set to values you like. 

When playing with TSO commands, you listed the data sets defined under your userid. Find the ISPF panel under Utilities where you can perform the equivalent action, and list the data sets under your userid. 

If you have just completed the item above, you're currently looking at the Data Set List Utility panel. That's two levels down from the Primary Option Menu. Try shortcut navigation by entering "=3.1" in the Command field and pressing Enter. This should take you to option 1 under option 3, also known as option 3.1, Library Utility. 


