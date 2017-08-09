from Bio import SeqIO
import pandas as pd
import argparse

def arguments():
    parser = argparse.ArgumentParser(description='Program for building the MegaBio database from exisiting aminoacid records')

    parser.add_argument()

    return parser.parse_args()

def current_megabio(megabio):

    """ Read file with MegaBio accessions, and read CDS database extracted with edirect """

    # TODO: Check if data can be downloaded and parsed with BioPython. Consider snakemake.

    # TODO: Double check if this needs to have a closing handle

    megabio_accessions = open('megabio_accessions.txt').read().splitlines()

    megabio_nt = [rec for rec in SeqIO.parse('megabio_database_cds.fasta', 'fasta')]

    return megabio_accessions, megabio_nt

def accession_matches(megabio_accessions, megabio_nt):

    """ Returns list of CDS records matched by the MegaBio aminoacid accessions"""

    matches = []

    for m in megabio_accessions:
        for n in megabio_nt:
            for m in n.description:
                matches.append(n)

    return matches

def unique_matches(matches):
    """ Returns a dictionary with record IDs as keys and records as values """

    matchDict = {}

    for m in matches:
        matchDict[m.id] = m

    return matchDict

def export_matches(matchDict):

    """ Save matched records as FASTA file """

    toSave = [v for v in matchDict.values()]

    SeqIO.write(toSave, 'megabio_AAFC.fasta', 'fasta')

def extract_ProtID_DF():

    megabioSteven = pd.read_csv('megabio_annotationsv0.1.csv')

    megabioSteven['ProtID'] = megabioSteven['Header'].str.split('|').str[2]

    megabioSteven.to_csv('megabio_annotations_CSU.csv', index=False)


def annotation_tuple_DF():


    megabioAAFC = [rec for rec in SeqIO.parse('megabio_AAFC.fasta','fasta')]


    protIDs = []

    descriptions = []

    for rec in megabioAAFC:
        protIDs.append(rec.description.split('protein_id=')[1].split('.')[0])
        descriptions.append(rec.description)

    descTuples = zip(protIDs, descriptions)

    descDF = pd.DataFrame.from_records(descTuples, names = ['ProtID', 'NewHeader'])

    descDF.to_csv('megabio_updated_headers.csv', index=False)

def main():

    args = arguments()

    current_records = current_megabio(megabio)

    matched_by_current = accession_matches(current_records)

    unique_cds = unique_matches(matched_by_current)

    export_matches(unique_matches)

if __name__ == '__main__':
    main()
