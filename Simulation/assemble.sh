#!/bin/bash
# Usage: ./assemble.sh <SVGen dir>
SVGEN_BASE=$1
SARG=''
for f in sample*_SV.fa
do
  SARG='$SARG -s $f'
done
twopaco -o sim.bin -t 32 -f 24 -k 25 $SVGEN_BASE/reference/hg38.chromFa/chr22.fa sample*_SV.fa
graphdump sim.bin --gfa -k 25 -s $SVGEN_BASE/reference/hg38.chromFa/chr22.fa $SARG > sim.gfa
gfa2json sim.gfa > sim.json
