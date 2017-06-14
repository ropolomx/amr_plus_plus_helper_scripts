#!/usr/bin/env python3

import pandas as pd
import argparse
import os
import glob
from collections import defaultdict

# Function to define the arguments of the script

def arguments():

    parser = argparse.ArgumentParser(description='Program to parse AmrPlusPlus Gene Ids/Headers into AMR Class, Mechanism and Group')

    parser.add_argument('amrdir', default-"./", help = 'Directory with output tab file from the AmrPlusPlus pipeline')

    return parser.parse_args()


def sample_names(amr_directory):

    """ Extracts the filenames of the samples 

    """

    samples = glob.glob(amr_directory+'*.tab*')

    sample_names = [os.path.splitext(os.path.basename(s))[0] for s in samples]    

    return samples, sample_names

def read_data(amr_tabular):

    """ Reads tabular AMRPlusPlus output files from specified directory as Pandas dataframe.

    Returns pandas dataframe with the name of the Gene Id column changed to Header. 
    """

    sample_files = sample_names(amr_directory)[0]

    amr_results = defaultdict(pd.DataFrame)

    for s in sample_files:

        amr_results[s] = pd.read_table(s)

    for v in amr_results.values():

        v = v.rename(columns={'Gene Id': 'Header'})

    return amr_results

def parse_and_split(amr_results):

    """Function for splitting the AMRPlusPlus headers by the pipe character

    Returns a pandas dataframe with the Class, Mechanism and Group columns

    extracted from the Header column"""

    for v in amr_results.values():
    
        v['Class'] = v['Header'].str.split('|').str[-3]

        v['Mechanism'] = v['Header'].str.split('|').str[-2]

        v['Group'] = v['Header'].str.split('|').str[-1]

    return amr_df

def save_to_file(amr_tabular, new_categories):

    samples = sample_names(amr_tabular)[1]

    df_header = ['Level', 'Iteration', 'Header', 'Class', 'Mechanism', 'Group', 'Gene Fraction', 'Hits']

    for s in samples:

        new_categories.to_csv(str(s+"_parsed"+".tab"), 
                                  sep="\t", 
                                  columns=df_header, 
                                  index=False)

def main():

    args = arguments()

    sample_names(args.amrdir)

    read_results = read_data(args.amrdir)

    splitting_headers = parse_and_split(read_results)

    save_to_file(args.amrtable,splitting_headers)

if __name__ == '__main__':
    main()
