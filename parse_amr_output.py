#! /usr/bin/python3

import pandas as pd
import argparse

# Function to define the arguments of the script

def arguments():

    parser = argparse.ArgumentParser(description='Program to parse AmrPlusPlus Gene Ids/Headers into AMR Class, Mechanism and Group')

    parser.add_argument('--output', default='./parsed_amr_results', help = 'Tab-delimited file that is the output of this script. It includes columns for AMR Class, Mechanism and Group')

    parser.add_argument('amrtable', help = 'Output tab file from AmrPlusPlus pipeline')

    return parser.parse_args()


def read_data(amr_tab_file):

    """ Reads tabular AMRPlusPlus output file as Pandas dataframe.

    Returns pandas dataframe with the name of the Gene Id column changed to Header. 
    """

    amr_results = pd.read_table(amr_tab_file)

    amr_results = amr_results.rename(columns={'Gene Id': 'Header'})

    return amr_results

def parse_and_split(amr_table):

    """Function for splitting the AMRPlusPlus headers by the pipe character

    Returns a pandas dataframe with the Class, Mechanism and Group columns

    extracted from the Header column"""

    amr_table['Class'] = amr_table['Header'].str.split('|').str[-3]

    amr_table['Mechanism'] = amr_table['Header'].str.split('|').str[-2]

    amr_table['Group'] = amr_table['Header'].str.split('|').str[-1]

    return amr_table

def save_to_file(new_categories, output):

    df_header = ['Level', 'Iteration', 'Header', 'Class', 'Mechanism', 'Group', 'Gene Fraction', 'Hits']

    new_categories.to_csv(str(output+".tab"), sep="\t", columns=df_header, index=False)

def main():

    args = arguments()

    read_results = read_data(args.amrtable)

    splitting_headers = parse_and_split(read_results)

    save_to_file(splitting_headers, args.output)

if __name__ == '__main__':
    main()
