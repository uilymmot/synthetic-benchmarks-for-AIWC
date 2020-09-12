#!/usr/bin/env python3

"""
    Extract the kernel source from the tensorflow generated .pbtxt file.
    If one argument is provided the source will be printed to the output (perhaps to be piped to some other place?), but if two arguments are given the kernel source will both be printed to standard output an written to the file -- this is specified by the kernel_filepath argument.
    Usage:
        ./pbtxt2kernel <pbtxt_filepath> <kernel_filepath>(optional)

    Example:
        ./pbtxt2kernel.py  ../synthetic_sample.pbtxt out.cl

"""

import sys

assert len(sys.argv) == 2 or 3

pbtxt_filepath = sys.argv[1]

kernel_source = ""
with open(pbtxt_filepath, 'r') as infile:
    for line in infile:
        if line.startswith("text: "):
            kernel_source = line

kernel_source = kernel_source.replace("text: \"",'')
kernel_source = kernel_source[:-2]
print(kernel_source)

if len(sys.argv) == 3:
    kernel_filepath = sys.argv[2]
    with open(kernel_filepath, 'w') as outfile:
        outfile.write(kernel_source)

