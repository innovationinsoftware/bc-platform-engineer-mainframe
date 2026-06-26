# Lab z/OS 7: Create a JCL library using ISPF

## Overview

We want to create a library to store our JCL for course labs. 

## Goals

- Create a Library (PDSE) for our JCL.

## Prerequisites

1. Your local system is connected to the Internet

## Part 1: Use ISPF option 3.2 to allocate a source Library

Navigate to ISPF option 3.2 and allocate a Library with the appropriate attributes to store source members. All sources on z/OS have to contain records that look like 80-column punched cards from the 1960s. Therefore, the logical record length must be 80. For a Library, the data set name type must be "LIBRARY". The record format can be FB, for "fixed, blocked," and the block size must be an even multiple of the logical record length, 80. 