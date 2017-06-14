#!/usr/bin/env python3

import pandas as pd
import argparse
import os
import glob
import re

# Function to define the arguments of the script

def arguments():

    parser = argparse.ArgumentParser(description='Program to parse AmrPlusPlus Gene Ids/Gene Ids into AMR Class, Mechanism and Group')

    parser.add_argument('amrdir', default=os.getcwd(), help = 'Directory with output tab file from the AmrPlusPlus pipeline')

    return parser.parse_args()


def sample_names(amr_directory):

    """ Extracts the filenames of the samples 

    """

    samples = glob.glob(amr_directory+'/'+'*.tab*')

    sample_names = [os.path.splitext(os.path.basename(s))[0] for s in samples]    

    return samples, sample_names

def read_data(amr_directory):

    """ Reads tabular AMRPlusPlus output files from specified directory as Pandas dataframe.

    Returns pandas dataframe with the name of the Gene Id column changed to Gene Id. 
    """

    sample_files = sample_names(amr_directory)[0]

    amr_results = {}

    for s in sample_files:

        amr_results[s] = pd.read_table(s)

    #amr_results = amr_results.popitem()

    return amr_results

def parse_and_split(amr_results):

    """Function for splitting the AMRPlusPlus headers by the pipe character

    Returns a pandas dataframe with the Class, Mechanism and Group columns

    extracted from the Gene Id column"""

    for v in amr_results.values():
    
        v['Class'] = v['Gene Id'].str.split('|').str[-3]

        v['Mechanism'] = v['Gene Id'].str.split('|').str[-2]

        v['Group'] = v['Gene Id'].str.split('|').str[-1]

    return amr_results

def save_to_file(amr_directory,amr_results):

    samples = sample_names(amr_directory)[1]

    df_header = ['Level', 'Iteration', 'Gene Id', 'Class', 'Mechanism', 'Group', 'Gene Fraction', 'Hits']

    for k,v in amr_results.items():

        filename = re.sub(r'\.tab.*','', k)

        v.to_csv(str(k+"_parsed"+".tab"),
                              sep="\t", 
                              columns=df_header, 
                              index=False)

def main():

    args = arguments()

    sample_names(args.amrdir)

    read_results = read_data(args.amrdir)

    splitting_headers = parse_and_split(read_results)

    save_to_file(args.amrdir,splitting_headers)

if __name__ == '__main__':
    main()
