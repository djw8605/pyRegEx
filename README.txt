CSCE 828 Project 1 
Derek Weitzel

src/pyRegEx.py
    This file is the python source of the regular expression parser.
    It takes input from stdin, sending to stdout.
    
tests/*
    This directory contains the tests that where distributed on the class
    website.
    
Building Instructions:
Since the program is written in python, there is no building required.


Execution Instructions:
Run the program by invoking the script with python:
python src/pyRegEx.py < input.txt

The program will read in the regular expression in the first line of stdin.
Each successive line will be treated as input that will be fed into the 
regular expression parser.  


This project uses a primitive parse tree to create a NFA.  Then, the NFA is 
simulated on the input.  No NFA to DFA translation was done since simulating
NFA is simple in python.

