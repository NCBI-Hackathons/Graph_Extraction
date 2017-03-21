#!/bin/bash
CHROM=22
CHROM_TRANS=1-21
FASTA=reference/hg38.chromFa/chr22.fa

for i in {1..1}
do
    python simulate_SV_BED.py \
        --dup_lens SV_lengths.txt \
        --del_lens SV_lengths.txt \
        --inv_lens SV_lengths.txt \
        --bal_trans_lens SV_lengths.txt \
        --unb_trans_lens SV_lengths.txt \
        --chroms $CHROM \
        --chroms_trans $CHROM_TRANS \
        --chrom_lens reference/chrom_lengths_hg38.txt \
        --gaps reference/gaps_hg38.txt \
        -o sample${i}_SVs.bed
    python insert_SVs.py \
        -i $FASTA \
        -o sample${i}_SV.fa \
        --chrom_lens reference/chrom_lengths_hg38.txt \
        --chrom $CHROM \
        --bed sample${i}_SVs.bed \
        -v
    python create_reads.py \
        -pe \
        -i sample${i}_SV.fa \
        -o sample${i}_reads.fq \
        --cov 30 \
        --read_len 100 \
        --snp_rate 0.01 \
        --del_rate 0.01 \
        --ins_rate 0.01
done
