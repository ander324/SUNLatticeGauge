#!/bin/bash


for target in $@ ; do
    grep $target meas.* > $target
    /home/ander324/SUNLatticeGauge/scripts/analyze.awk $target
done
