# Lab z/OS 37: Explore SMP/E in ISPF
## Overview

You want to become more familiar with SMP/E.

## Goals

- Explore the options available for SMP/E under ISPF to learn how things are laid out and named, and what kinds of information each item stores. There's no specific work to do for this lab. It's just to get used to the tools, and start to recognize some of the main bits and pieces of SMP/E.

## Part 1: In ISPF, navigate to the SMP/E ISPF menu

On the SMP/E Primary Option Menu under ISPF, enter option D for "Describe." Browse around the documentation and get a sense of what kinds of information you can find there. There's no need to read it in depth at this time, unless you see something that particularly interests you. Press F3 to return to the menu.

Now enter option T for Tutorial and explore the tutorial content briefly. The goal is to familiarize yourself with the ISPF SMP/E facility and what you can find there. Press F3 to return to the menu.

About halfway down the page there's a field labeled "SMPCSI Data Set". If that field is pre-filled, clear it by typing spaces over the data set name. Then enter option 3, "Query," and press Enter. That takes you to the SMP/E CSI Selection panel.

## Part 2: SMP/E CSI Selection panel

Explore the Describe and Tutorial content accessible from this panel.

A list of SMPCSI Data Set names will be shown at the bottom of the panel. Tab down to that part of the screen and type an "S" next to one of the data set names. You might want to make a note of the data set name you selected, because subsequent panels don't echo the value. 

Press Enter. That takes you to the Query Selection Menu.

## Part 3: Query Selection Menu

This panel also has Describe and Tutorial options. Browse through those. When you're finished, press F3 to return to the menu. 

Enter option 1, CSI Query, and press Enter. That takes you to the CSI Query panel. 

## Part 4: CSI Query panel.

If you didn't make a note of the CSI data set you're querying, you might be starting to regret it just about now. These panels don't remind you which data set you're looking at. 

Clear out Zone Name, Entry Type, and Entry Name by typing spaces over any values they contain. That way, you can see what the dialog displays when you leave the fields blank. 

There aren't multiple options on this panel, so you can just press Enter to continue. It's going to show you lists of Zone Name, Entry Type, and Entry Name to narrow down your query.

## Part 5: Zone Selection

This panel displays a list of the zones defined in the CSI data set you selected. If one of them is labeled Global, type an "S" next to it and press Enter. 

## Part 6: Entry Type Selection 

Now the dialog presents a list of the Entry Types within the selected Zone within the selected CSI data set. Choose several of the Entry Types (one at a time, of course) and choose one or more Entry Names to see what they look like and what they tell you about the entries. 