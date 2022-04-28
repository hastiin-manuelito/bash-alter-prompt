#!/bin/env python

# Using this repository to get well acquinted with git
SPAN = 80
VARIABLE = 'O'
MULT = 2
SPACE = ' ' * MULT

def print_pattern(span, variable, space):
    for i in range(40):
        varspan = variable * ((span - 2*len(space)) - i*2)
        space = space
        llateralspan = variable * ((span - (len(varspan) + len(space)))//2)
        rlateralspan = variable * ((span - (len(varspan) + len(space)))//2)
        print(llateralspan + space + varspan + space + rlateralspan)

print_pattern(SPAN, VARIABLE, SPACE)
