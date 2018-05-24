# Scripts for helping with AmrPlusPlus data analysis

This repository contains scripts for helping with data cleaning, processing and analysis of results generated with the AmrPlusPlus pipeline.

### `parse_amr_output.py`

__Purpose__: This script parses the Gene Ids (or headers) from the AmrPlusPlus database present in the results from CoverageSampler. The script divides those headers into AMR Class, Mechanism and group. The script will read all the *.tab or *tabular files on the same directory.

__Usage__:

``parse_amr_output.py [name of directory]``

__Software Requirements__:

Python 3 (tested with Python 3.6.3)
* `pandas` library

### `buildingMegabio.py`

__Purpose__: This script builds a nucleotide MegaBio database (biocides and biometals) from aminoacid accession numbers from a database curated by CSU.

### `megabio_annotation.R`

__Purpose__: This script parses old annotation file, and filters it and generates a new annotation file with new FASTA headers from `edirect` search.
