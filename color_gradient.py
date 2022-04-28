#!/bin/env python

import os
import sys
from sys import argv

if len(argv) != 3:
    sys.exit('Need two ints (space separated) from 0 to 7 for term colors.')
else:
    left = int(argv[1])
    right = int(argv[2])
    
# Using wal-generated colors 0-7
with open(os.path.expanduser('~/.cache/wal/colors')) as cf:
        cl = cf.read().strip().split()

# Set the gradient length
gradient_len = 6

def calc_rgb_diff(left_color, right_color):
    # Split up the rgb values into r, g, and b values for interpolation
    rl = int(left_color[0:2],base=16)
    gl = int(left_color[2:4],base=16)
    bl = int(left_color[4:6],base=16)
    rr = int(right_color[0:2],base=16)
    gr = int(right_color[2:4],base=16)
    br = int(right_color[4:6],base=16)
    
    # Calculate the difference between rgbs
    red_diff = rr-rl
    green_diff = gr-gl
    blue_diff = br-bl
    diff_tup = (red_diff, green_diff, blue_diff)
    start_color = (rl, gl, bl)
    
    # values for [d]efault background
    #rd = int(default_c[0:2],base=16)
    #gd = int(default_c[2:4],base=16)
    #bd = int(default_c[4:6],base=16)

    return diff_tup, start_color

# Calculate and build color steps
def populate_steps_dict(diff_tup, gradient_len=5):
    """Calculate the steps of each rgb value where `diff_tup` is the
    is the rgb tuple of left and right ends of the color gradient
    gradient_len: number of steps to take, len-1, default=5

    Returns a dict object with steps for each rgb value."""
    # A dictionary of steps for each rgb value
    steps = dict(red=0, green=0, blue=0)

    for diff, key in zip(diff_tup,steps):
        steps[key] = int(diff/gradient_len)

    return steps
    
# Create the color arrays in another rgb dict
def create_color_arrays(steps: dict, start_color: tuple, gradient_len=5):
    """Calculate the rgb colors in an array.

    steps: dictionary of steps for each rgb value
    gradient_len: The number of steps to take, len-1. default=5)
    (red_left,green_left,blue_left): tuple of split rgb values to calculate
        the colors

    Returns a dict object with list of rgb values:
        {'red': [000000,...,ffffff], 'green': ..., ...}
    """
    
    #Define the dictionary
    grdnt = dict(red=[], green=[], blue=[])

    for key, otherkey, rgb in zip(steps, grdnt, start_color):
        for i in range(gradient_len):
            nxtc = rgb + steps[key]*(i+1)
            to_str = str(nxtc)
            grdnt[otherkey].append(to_str)

    return grdnt
    
# Build the proper bash escape sequence to fill in colors
def build_color_escapes(grdnt: dict):
    """A formatter to change rgb tuple values into a bash escape sequence.

    Returns a string of escape values.
        example: '\[ESC [48:2:<r>:<g>:<b>m]\ ...' """
    cout = []
    esc_strt = r'\033['
    for i in range(gradient_len):
        concat = ''
        for key in grdnt:
            concat = ':'.join([concat,grdnt[key][i]])
        concat = esc_strt + r'48:2' + concat + 'm'
        cout.append(concat)
    
    bash_code = r'\] \['.join(cout)
    bash_code = r'\[' + bash_code + r'\]'
    
    return bash_code

# drop hash
left_c = cl[left].strip('#')
right_c = cl[right].lstrip('#')

diff_tup, start_color = calc_rgb_diff(left_c, right_c)
steps = populate_steps_dict(diff_tup, gradient_len)
grdnt = create_color_arrays(steps, start_color, gradient_len)
bash_code = build_color_escapes(grdnt)

print(bash_code)

