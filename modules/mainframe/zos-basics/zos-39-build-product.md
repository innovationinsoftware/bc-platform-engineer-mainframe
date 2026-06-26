# Lab z/OS 39: Build your product and package it for distribution

## Overview

Now you're acting as the software developer/vendor who has a product to distribute to customers via SMP/E. You've created a separate SMP/E environment for packaging the product, and SMP/E created a number of data sets for its own use. But it doesn't know about your product or which files you intend to distribute to customers. 

## Goals

- Create development libraries for building your product and populate them with initial members.
- Tell SMP/E how you want to distribute the product.

## Part 1: Allocate development libraries 

Using JCL similar to your "developer provisioning" job from an earlier lab, allocate the source and program libraries for the CHUMP product.

Be sure and create a _program library_ rather than a _load library_ for the executables. That's DSNTYPE=LIBRARY on the DD statement. This makes a difference in how you specify the product elements in the SMP/E CSI.

Create a source library for "seed" members. Upload the files from zos/chump to the "seed" library. 

Add an IEBCOPY step to your provisioning job that copies the members from the "seed" library into the appropriate development libraries:

- zos/chump/DEV.JCLLIB-MAKELIBS => \<userid\>.CHUMP.DEV.JCLLIB(MAKELIBS)
- zos/chump/DEV.JCLLIB-YYZBDJCL => \<userid\>.CHUMP.DEV.JCLLIB(YYZBDJCL)
- zos/chump/DEV.PROCLIB-MAKELIB => \<userid\>.CHUMP.DEV.PROCLIB(MAKELIB)
- zos/chump/DEV.PROCLIB-MAKEPLIB => \<userid\>.CHUMP.DEV.PROCLIB(MAKEPLIB)
- zos/chump/DEV.PROCLIB-YYZBUILD => \<userid\>.CHUMP.DEV.PROCLIB(YYZBUILD)
- zos/chump/DEV.SAMPLIB-$INFO => \<userid>.CHUMP.DEV.SAMPLIB($INFO)
- zos/chump/DEV.SAMPLIB-DMOGREET => \<userid\>.CHUMP.DEV.SAMPLIB(DMOGREET)
- zos/chump/DEV.SAMPLIB-DMOSETCC => \<userid\>.CHUMP.DEV.SAMPLIB(DMOSETCC)
- zos/chump/DEV.SRCLIB-YYZGREET => \<userid\>.CHUMP.DEV.SRCLIB(YYZGREET)
- zos/chump/DEV.SRCLIB-YYZSETCC => \<userid\>.CHUMP.DEV.SRCLIB(YYZSETCC)

You _could_ do all those things one by one, manually, but part of the purpose of lab practice is to cultivate the habit of automating things. Do the allocations and the seeding of the libraries in a single batch job.

What you have done up to this point is to set up some data sets in a way that a development team might do, and populated them with members such as a development team might have. You haven't touched on SMP/E functionality yet. 

## Part 2: Build the product 

The JCLLIB member YYZBDJCL will assemble and bind all the utility programs in the Chindogu Utility Mega-Pack, calling PROCLIB member YYZBUILD for each one. The resulting executables will be members of your PROGLIB. 

