# Lab z/OS 2: Access the z/OS lab environment

## Overview

Historically, the only ways to access an IBM mainframe system were to load punched cards into a card reader or to connect to VTAM using an IBM 3270 or compatible terminal. Today, the mainframe still expects those forms of connection, although they are virtualized. The mainframe can also expose API endpoints and TCP/IP ports to enable access.

z/OS contains "legacy" functionality (often called MVS, or Multiple Virtual Systems, the name of an ancestor of z/OS) as well as POSIX functionality (called USS, or Unix System Services). We can use telnet to connect to USS on z/OS. 

Over the telnet connection we can then (a) call APIs exposed by z/OS and (b) use 3270 terminal emulation to access MVS tools and resources. In this lab we will use 3270 terminal emulation to access z/OS.

## Goals

- Install and set up a 3270 emulator on your local system.
- Connect to the z/OS instance we will use in lab activities.
- Log on to TSO and ISPF using your z/OS credentials.
- Change your initial default z/OS password. 
- Exit from ISPF, then from TSO, then from the terminal emulator session.

## Prerequisites

1. You have your z/OS user id and the IP address and port number to connect to
2. You are authorized to install a terminal emulator on your local system
3. Your local system is connected to the Internet

## Part 1: Install a 3270 terminal emulator

You can use any 3270 terminal emulator you wish. They all support the same protocols. The course instructor uses an open source product called x3270. Information is provided in the course slides. 

## Part 2: Connect to the lab z/OS instance via the terminal emulator 

Every terminal emulator product supports at least one, and probably several ways to establish a connection with a remote system - command line, script, profile, GUI interface, etc. Using the IP address and port number that were provided to you, set up your terminal emulator to connect to the lab z/OS instance. 

## Part 3: Log on and off TSO and ISPF on the lab z/OS instance 

Once you have established a connection, you will be able to log on to TSO and ISPF as shown in the course slides. Then follow the steps described in the slides to log off and end your terminal emulator session. 
