#!/bin/bash

FILES=$1/*
SIZE=$2
PLATFORM=$3
DEVICE=$4
MODE=$5

GOOD_KERNEL_COUNT=0
GOOD_KERNELS=""
ALL_KERNEL_COUNT=0

for f in $FILES
do
    echo "Processing $f..."
    ./pbtxt2kernel.py $f $f.cl
    ./sbd $f.cl $SIZE $PLATFORM $DEVICE $MODE;
    STATUS=$?
    if [ $STATUS -eq 0 ]
    then
        GOOD_KERNEL_COUNT=$((GOOD_KERNEL_COUNT+1))
        GOOD_KERNELS=$f" "$GOOD_KERNELS
    fi
    ALL_KERNEL_COUNT=$((ALL_KERNEL_COUNT+1))
done

echo "There were $GOOD_KERNEL_COUNT good kernel(s) out of $ALL_KERNEL_COUNT in this directory"
