#!/bin/bash
# Usage: ./generate_reads.sh <SVGen directory>
SVGEN_BASE=$1
CHROM=22
CHROM_TRANS=1-21
FASTA=$SVGEN_BASE/reference/hg38.chromFa/chr22.fa

for i in {1..1}
do
    simulate_SV_BED.py \
        --dup_lens $SVGEN_BASE/SV_lengths.txt \
        --del_lens $SVGEN_BASE/SV_lengths.txt \
        --inv_lens $SVGEN_BASE/SV_lengths.txt \
        --bal_trans_lens $SVGEN_BASE/SV_lengths.txt \
        --unb_trans_lens $SVGEN_BASE/SV_lengths.txt \
        --chroms $CHROM \
        --chroms_trans $CHROM_TRANS \
        --chrom_lens $SVGEN_BASE/reference/chrom_lengths_hg38.txt \
        --gaps $SVGEN_BASE/reference/gaps_hg38.txt \
        -o sample${i}_SVs.bed
    insert_SVs.py \
        -i $FASTA \
        -o sample${i}_SV.fa \
        --chrom_lens $SVGEN_BASE/reference/chrom_lengths_hg38.txt \
        --chrom $CHROM \
        --bed sample${i}_SVs.bed \
        -v
    create_reads.py \
        -pe \
        -i sample${i}_SV.fa \
        -o sample${i}_reads.fq \
        --cov 30 \
        --read_len 100 \
        --snp_rate 0.01 \
        --del_rate 0.01 \
        --ins_rate 0.01
done
