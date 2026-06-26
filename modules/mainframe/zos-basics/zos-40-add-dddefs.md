# Lab z/OS 40: Add DDDEFs to Target and Distribution zones      

## Overview

Continuing to prepare the product for distribution.

## Part 3: Prepare the product for distribution 

Now it's time to set things up so that SMP/E can create a SYSMOD for the product. This work is still on the development side of things. When you're working as a z/OS system programmer, IBM or another company has already done this to prepare the SYSMODs you install.

### Part 3.1: Decide which elements you want to distribute to customers

Some elements of the product exist for development purposes only, and aren't part of the shipped package. These are things like program source, JCL to run compilers or assemblers, and so forth. Let's clarify which bits and pieces of CHUMP we want to distribute to customers.

| Library | Member | Purpose | Distribute? |
| ------- | ------ | ------- | ----------- |
| JCLLIB | MAKELIBS | Alloc dev libs | No |
| JCLLIB | YYZBDJCL | Build product | No |
| PROCLIB | MAKELIB | Alloc source lib | No |
| PROCLIB | MAKEPLIB | Alloc program lib | No |
| PROCLIB | YYZBUILD | Build product | No |
| SAMPLIB | $INFO | Product doc | Yes |
| SAMPLIB | DMOGREET | Demo JCL YYZGREET | Yes |
| SAMPLIB | DMOSETCC | Demo JCL YYZSETCC | Yes |
| SRCLIB | YYZGREET | Source code | No |
| SRCLIB | YYZSETCC | Source code | No |
| PROGLIB | YYZGREET | Executable | Yes |
| PROGLIB | YYZSETCC | Executable | Yes |

So, we want to distribute the executables for the utilities which we built in Part 2 of this lab, and the samples and documentation we created during development. (Well, we're pretending we created them; they were given, in this case.)

### Part 3.2: Create SMP/E-controlled libraries for product elements

SMP/E needs libraries separate from our local development libraries to contain the elements of products to be packages.

These are (or can be) specific to a product, so we can include the product name in the data set names. We need a library of each type in both the Target Zone and the Distribution Zone.

\<userid\>.CHUMP.TGTPROG      <= DSNTYPE=LIBRARY
\<userid\>.CHUMP.TGTSAMP

\<userid\>.CHUMP.DLIBPROG     <= DSNTYPE=LIBRARY
\<userid\>.CHUMP.DLIBSAMP

Allocate these libraries and copy the relevant members to them from the development libraries.

### Part 3.3: Define DDDEFs in CSI

In Part 3.2 of this lab you allocated libraries that are to be "SMP/E-controlled." You let SMP/E control them by defining DDDEFs in the CSI. 

The DDDEFs (DD definitions) enable SMP/E to allocate the datasets to the job step dynamically. 

GIMSMP uses SVC 99 system calls to do that, in case you're interested. That's also how JES2, TSO, CICS, and other MVS facilities do it, when they don't have JCL DD statements. A program needs to know the DDNAME, DSNAME, and DISP, and it can allocate the data set dynamically. The advantage is you don't have to hand-code DD statements for all the data sets the program references.

Here's how you provide the DDNAME, DSNAME, and DISP for the SMP/E-controlled libraries you created: 

```shell
SET BDY(TARGET).

UCLIN.

REP DDDEF(YYZTPROG)
  DA(PLAT01.CHUMP.TGTPROG)
  SHR.

REP DDDEF(YYZTSAMP)
  DA(PLAT01.CHUMP.TGTSAMP)
  SHR.

ENDUCL.

SET BDY(DLIB).

UCLIN.

REP DDDEF(YYZDPROG)
  DA(PLAT01.CHUMP.DLIBPROG)
  SHR.

REP DDDEF(YYZDSAMP)
  DA(PLAT01.CHUMP.DLIBSAMP)
  SHR.

ENDUCL.
```

The documentation and examples you might find will tell you to use ADD DDDEF. That's correct, but if you need to re-run because one or two of the definitions failed, the re-run will fail because of the commands that worked the first time. If you use REP (replace) instead of ADD, SMP/E will be tolerant of entries that already exist.

Set up and run a GIMSMP job to do this.

After the job runs successfully, check that the DDDEFs are defined in the Target and Distribution Zones. Use the LIST DDDEF command in a GIMSMP batch job for this. 
