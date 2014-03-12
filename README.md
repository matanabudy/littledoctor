littledoctor
============

Optimization program for CoreWars8086 survivors

Requires:
---------
* Python 2.6
* fasm
* DOSBoxPortable
* special8086

Installation:
-------------
Before you run the little doctor, you should make sure all the required programs are in the same directory as the littledoctor python file.

Usage:
------
littledoctor.py [survivor_name] [start_value] [end_value] [step]

survivor_name: enter with no number, assumes there are two survivors.

Example usage:
I have a survivor named LOUREED in fasm directory. In each LOUREED I have a constant defined:
X equ 0h
Now I want to optimize it with values from 1 to 10 (hex), with a step of 3, so I run the littledoctor from command line:
littledoctor.py LOUREED 1 10 3
When I'm asked to enter a pattern, I enter:
'equ 0h' (and not 'X equ 0h'!)
