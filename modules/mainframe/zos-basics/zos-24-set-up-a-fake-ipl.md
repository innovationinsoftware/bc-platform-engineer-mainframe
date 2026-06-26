# Lab z/OS 24: Set up a fake IPL

## Overview

We can't IPL our lab system because we don't own it, and we aren't allowed to blow it away and start it up again. But we _can_ tie together a few data sets in the same way as they are tied together to do an IPL. The "system" that we "IPL" will be a REXX script that says it was IPLed at a certain date and time. We also won't do an actual operator START command. We'll simulate that by running a REXX script. The point is to see the way the various data sets are related.

In the presentation, you saw the steps of the z/OS IPL process at a high level. The "fake IPL" setup mimics the main steps of that process and requires coding a few of the data sets that contain configuration and startup information. 

## Goals

- Set up a bare-bones fake IPL to see how the various data sets are related.

## Part 1: Configure a fake z/OS system and IPL it

What's provided: 

FAKE.CLISTLIB(FAKEIPL) - a REXX script that stands in for the HMC. Executing the script is conceptually equivalent to selecting the LOAD option on the HMC. It initiates the IPL process. To run it, you specify a two-character identifier for your "system". The lab system is set up with the identifier "K2". You can view the data sets on the lab system to see how they're written and how they're related. 

FAKE.CLISTLIB(MSTSCHED) - a REXX script that stands in for the Master Scheduler. It does far less than the real Master Scheduler. It will look at the configuration data sets you've set up and check them for validity (not very strenuously). If you've set things up reasonbly correctly, the script will launch a batch job that simulates the next step in the IPL process. 

FAKE.JCL(IPLFAKE) - a JCL stream containing one job with one step. It stands in for the MSTJCL00 job in a real IPL process. It executes a JCL Procedure to simulate system startup.

FAKE.PROCLIB(IPLPROC) - the JCL Procedure that is executed by job IPLFAKE. It contains one step. That step runs the TSO batch processor, IKJEFT01, to execute another REXX script. 

FAKE.CLISTLIB(IPLGO) - a REXX script that stands in for a z/OS system that would have been IPLed had we been doing this for real. It displays a message stating the date and time of the IPL. 

If all we wanted to do was display the date and time, we could certainly do it more easily than this. The idea is that this simulation uses some of the same configuration data sets as a real IPL process, and its various bits and pieces are connected to each other in roughly the same way as the main pieces of a real IPL process. (Much simpler, actually.) 

What you must develop: 

1. You will create a member in library FAKE.IPLPARM named LOADxx, where xx stands for the two-character identifier for your "system." This has to contain realistic entries or script FAKEIPL will complain and die. FAKE.IPLPARM is the fake version of SYS0.IPLPARM.  

2. You will create a member in a PARMLIB of your choosing/making named IEASYMxx, where xx stands for you-know-what. Look at real IEASYMxx members in libraries like K2.PARMLIB and SYS1.PARMLIB to see what kinds of entries they contain. For the simluation, you only have to make sure you have a SYSDEF entry that specifies a system name. 

3. You will create a member in a PARMLIB of your choosing/making named IEASYSxx, where xx...well, you know. This member contains most of the configuration settings for the z/OS system. Script MSTSCHED looks for several of the most common entries and if you don't provide them, it will complain and die. 

The configuration settings that you code won't do anything because we aren't starting a real z/OS system; but you can get a feel for what the settings are and where they are defined. 

You can execute script FAKEIPL to test your setup. It and MSTSCHED will emit helpful error messages that may offer guidance to complete the configuration. 

At the TSO READY prompt or on ISPF Option 6, run the script with:

EX 'FAKE.CLISTLIB(FAKEIPL)' 'xx'

## Part 2: Walkthrough and discussion 

We'll walk through several solutions as a group. There's more than one way to code these data sets, and it may be interesting to see how different people did it. 

We'll also walk through the instructor's sample solution and see if he did anything differently.

