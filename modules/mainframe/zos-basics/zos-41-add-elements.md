# Lab z/OS 39: Build your product and package it for distribution

## Overview

Continuing to prepare the product for distribution.

## Goals

- Add the product elements to the Target and Distribution zones and associate them with the Target and Distribution libraries

### Part 1: Define product elements in CSI

SMP/E needs to know what elements belong to this product and which library each one belongs in. We use ADD commands to define this information. 

```shell
SET BDY(TARGET).

UCLIN.
ADD PROGRAM(YYZGREET)
    DISTLIB(YYZTPROG).

ADD PROGRAM(YYZSETCC)
    DISTLIB(YYZTPROG).

ADD TEXT($INFO)
    DISTLIB(YYZTSAMP).

ADD SRC(DMOGREET)
    DISTLIB(YYZTSAMP).

ADD SRC(DMOSETCC)
    DISTLIB(YYZTSAMP).
ENDUCL.

SET BDY(DLIB).

UCLIN.
ADD PROGRAM(YYZGREET)
    DISTLIB(YYZDPROG).

ADD PROGRAM(YYZSETCC)
    DISTLIB(YYZDPROG).

ADD TEXT($INFO)
    DISTLIB(YYZDSAMP).

ADD SRC(DMOGREET)
    DISTLIB(YYZDSAMP).

ADD SRC(DMOSETCC)
    DISTLIB(YYZDSAMP).
ENDUCL.
```

You can use REP (replace) here, as well. 

Set up and run a GIMSMP job to do this.

After the job runs successfully, check that the elements are defined in the Target and Distribution Zones. Use the LIST elementtype(elementname) command in a GIMSMP batch job for this. 
