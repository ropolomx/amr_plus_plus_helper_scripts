#!/usr/bin/env python3

import pandas as pd
import argparse
import os

# Function to define the arguments of the script

def arguments():

    parser = argparse.ArgumentParser(description='Program to parse AmrPlusPlus Gene Ids/Headers into AMR Class, Mechanism and Group')

    parser.add_argument('amrtable', help = 'Output tab file from AmrPlusPlus pipeline')

    return parser.parse_args()


def sample_name(amr_tabular):

    """ Extracts the name of the sample from the filename

    Returns string with sample name

    """

    sample = os.path.splitext(os.path.basename(amr_tabular))[0]

    return sample

def read_data(amr_tabular):

    """ Reads tabular AMRPlusPlus output files from as Pandas dataframe.

    Returns pandas dataframe with the name of the Gene Id column changed to Header. 
    """
    sample = sample_name(amr_tabular)
    
    amr_results = pd.read_table(os.path.join(sample+'.tabular'))

    amr_results = amr_results.rename(columns={'Gene Id': 'Header'})

    return amr_results

def parse_and_split(amr_df):

    """Function for splitting the AMRPlusPlus headers by the pipe character

    Returns a pandas dataframe with the Class, Mechanism and Group columns

    extracted from the Header column"""

    amr_df['Class'] = amr_df['Header'].str.split('|').str[-3]

    amr_df['Mechanism'] = amr_df['Header'].str.split('|').str[-2]

    amr_df['Group'] = amr_df['Header'].str.split('|').str[-1]

    return amr_df

def save_to_file(amr_tabular, new_categories):

    sample = sample_name(amr_tabular)

    df_header = ['Level', 'Iteration', 'Header', 'Class', 'Mechanism', 'Group', 'Gene Fraction', 'Hits']

    new_categories.to_csv(str(sample+"_parsed"+".tab"), sep="\t", columns=df_header, index=False)

def main():

    args = arguments()

    sample_name(args.amrtable)

    read_results = read_data(args.amrtable)

    splitting_headers = parse_and_split(read_results)

    save_to_file(args.amrtable,splitting_headers)

if __name__ == '__main__':
    main()
