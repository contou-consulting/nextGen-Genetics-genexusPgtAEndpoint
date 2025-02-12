#!/usr/bin/python3

import vcf
import pandas as pd
import numpy as np
import argparse #parses command line inputs

def read_cytoband(cytoband_file:str):
    """
    Read cytoband information from the cytoband.txt file and store it in a pandas dataframe.
    Source for the cytoband file: https://software.broadinstitute.org/software/igv/Cytoband

    Args:
        cytoband_file: name of cytoband file

    Returns:
        pandas dataframe containing cytoband information
    """
    with open(cytoband_file, 'r') as file:
        text = file.read()
    text = text.split('\n')
    text = [t.split('\t') for t in text]
    cols = ['chromosome','start','end','band','stain']
    df = pd.DataFrame(text, columns=cols)
    df = df.dropna()
    cols = ['start','end']
    for c in cols:
        df[c] = df[c].astype(int)
    # make sure cytoband file is sorted
    df = df.sort_values(by=['chromosome','start','band'])
    return df

def read_vcf(vcf_file:list):
    '''
    Reads vcf file

    Args:
        vcf_file (list): List of vcf files

    Returns:
        pandas dataframe containing vcf information
    '''
    dfo = []
    for fname in vcf_file:
        with open(fname, 'r') as f:
            vcf_reader = vcf.Reader(f)
            out = []
            for record in vcf_reader:
                chromosome = record.CHROM
                start_position = record.POS
                end_position = record.INFO['END']
                length = end_position - start_position
                ploidy = record.genotype(record.samples[0].sample)['CN']  # Extract ploidy from the first sample
                #print(ploidy)
                out.append([chromosome, start_position, end_position, ploidy])
                #print(out)
        cols = ['chromosome','start','end','ploidy']
        df = pd.DataFrame(out, columns=cols)
        
        df['filename'] = fname
        df['length'] = df['end'] - df['start']
        dfo.append(df)
    df = pd.concat(dfo)
    cols = ['start','end']
    for c in cols:
        df[c] = df[c].astype(int)
    return df

def find_cytoband_range(chr, start, end, df):
    """
    Find the cytoband range for a given chromosome, start, and end positions.

    Args:
        chr (str): Chromosome name (e.g., "chr1").
        start (int): Start position in the chromosome.
        end (int): End position in the chromosome.
        df: pandas dataframe of cytoband information.

    Returns:
        str: Cytoband range (e.g., "p11.32q23").
    """
    c = df['chromosome'] == chr
    # make vcf index same as cytoband index
    start = start - 1
    end = end - 1

    c1 = c & (df['end'] > start)
    c2 = c & (df['start'] < end)

    s1 = df[c1]['band'].values[0]
    s2 = df[c2]['band'].values[-1]
    return ''.join([chr, s1, s2])

def translate_vcf(cytobandFile, inFile):
    # Read cytoband information
    print('Reading cytobands files')
    cyto = read_cytoband(cytobandFile)

    # read vcf file info
    print('Reading vcf files')
    df = read_vcf([inFile])
    #print(df)

    # read vcf information
    out = []
    for chr, start, end in df[['chromosome','start','end']].values:
        out.append(find_cytoband_range(chr, start, end, cyto))
    df['cytoband'] = out
    #print(df)
    #df = df.drop(columns=['filename','start','end'])
    return df;


