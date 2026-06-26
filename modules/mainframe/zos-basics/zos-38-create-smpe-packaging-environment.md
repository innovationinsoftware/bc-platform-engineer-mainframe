# Lab z/OS 38: Create SMP/E packaging environment

## Overview

In the next few labs, we will act as a software development organization to prepare and package a product for distribution as a SYSMOD, and then as the customer organization to use SMP/E to install and test the product. 

You'll set up two SMP/E environments under your userid - one to package the product for distribution (you're the developer), and the other to receive and install the product (now you're the customer). This lab concerns the packaging environment.

## Goals

- Create a development/packaging SMP/E environment under your own userid.

## Part 1: Decide on a consistent naming convention for your data sets

Your sandbox data sets should be allocated under your userid. The last qualifier should be the expected value for standard SMP/E data sets, like .CSI, .SMPMTS, and so forth. 

The mid-level qualifier can be anything you want. Here are some sample data set names using USER01 (a userid) as the HLQ, the word "SANDBOX" as the MLQ, and the standard (or typical) SMP/E values for the remaining data set name segments. This sort of naming convention makes it clear that these data sets pertain to a test environment and are not used for actual system maintenance.

    \<userid\>.SANDBOX.GLOBAL.CSI
    \<userid\>.SANDBOX.SMPPTS 
    \<userid\>.SANDBOX.TARGET.SMPLOG

## Part 2: Copy and customize the JCL in SYS1.SAMPLIB(GIMSAMPU)

Browse member SYS1.SAMPLIB(GIMSAMPU) and follow the instructions given in the comments near the top of the file.  

The first step is to fix the JOB statement. Details of the JOB statement are installation-specific, so IBM didn't make any assumptions here. Your usual JOB statement will be fine. 

The next three steps are to replace placeholder values in the sample JCL with the actual values you want to apply to your job. The placeholders begin and end with ampersand characters (&), but they are not JCL symbols. The ampersands are just delimiters, to make it easier for you to locate all the places in the file where you need to make changes. 

If you open the file in the ISPF Editor, you can use change commands to replace the placeholders:

    c all &HLQ& USER01
    c all &VOLUME& USRVS1
    c all &UNIT& SYSDA 

If you're using an off-platform text editor or IDE, it will have a feature to find and replace occurrences of strings. For example, for VSCODE you can use Alt+Windows+f or Option+Apple+f or Alt+Meta+f to choose the "replace" function, or you can select it from the Edit menu. 

If you intend to create the data sets under a high-level qualifier _other than your own userid_, then you'll want to handle the &HLQ& placeholder a little differently. You'll want &SYSUID to be your userid so you can find the spooler output from the job. You'll want to set the HLQ of the SMP/E data sets to a different value.

Review the slides for information on how to use symbols in inline data. You can adjust the HLQs in the job by adding statements like these after the JOB statement:

    // EXPORT SYMLIST=(HLQ)
    // SET HLQ=USER01.SANDBOX

You'll also want to change the &HLQ& placeholder value (with "change all" or "replace all") from "&HLQ&" to "&HLQ.". That will cause the placeholders in inline data sets in the job to change from this:

    &HLQ&.blah 

to this:

    &HLQ..blah

and then at runtime symbol replacement will convert this

    &HLQ..blah 
    
to this SOMETHING.CHUMP.blah.

One more thing to do: You must tell JES2 that you want it to process symbols that are part of inline data sets. Otherwise it will treat the symbols as plain data. You do that with the SYMBOLS= parameter on the DD statement. 

    //SYSIN  DD  *,SYMBOLS=JCLONLY
     DEFINE CLUSTER(
        NAME(&HLQ..GLOBAL.CSI      
    . . . 

That will replace "&HLQ..GLOBAL.CSI" with "<userid>.SANDBOX.GLOBAL.CSI".

Remember that z/OS doesn't assume anything about the "meaning" of data set name qualifiers. It doesn't automatically associate the HLQ with a userid. If you choose to set up your sandbox this way, you need to use RACF to create user a userid with appropriate attributes. 

## Part 3: Run the setup job and review results

The sample job is written as if it will succeed on the first try. That's always nice. But just in case it doesn't, you'll have to do various things to re-try it. 

Step DEFZONES runs IDCAMS to define and initialize CSI data sets. If that step fails early and no data sets are defined, you can re-run the job from the top after fixing whatever it's complaining about. 

Otherwise, you'll have to delete whatever VSAM objects were catalogued prior to the failure before you can re-run the job. If you expect to re-initialize your sandbox SMP/E data sets repeatedly, you might consider adding DELETE steps to the IDCAMS control statements. 

The second step, ALLOCDS, runs IEFBR14 to allocate a bunch of data sets SMP/E uses. If DEFZONES completes normally and the job fails in step ALLOCDS, you needn't re-run the job from the top. You can add a RESTART=ALLOCDS parameter to the JOB statement to begin the re-run in step ALLOCDS. 

If ALLOCDS allocates one or more data sets before it fails, you'll have to delete them before re-running. If you expect to do this repeatedly, you might consider adding another IEFBR14 step ahead of ALLOCDS to delete the data sets with DISP=(MOD,DELETE,DELETE). 

The third step, UPDZONES, runs GIMSMP (the SMP/E batch program) and uses its own command language to configure the CSIs. If the job fails during this step, you'll need to check the output to see whether anything was done before the failure, and reverse it before re-running. An alterntive is to delete the VSAM objects and the sequential data sets and start over. 

If you can re-run starting with step UPDZONES, add the parameter RESTART=UPDZONES to the Job statement and re-run. 

Once you have a clean run, check the results either by querying vis the ISPF panels or by running GIMSMP with commands to list what's in the three Zones. 
product. 