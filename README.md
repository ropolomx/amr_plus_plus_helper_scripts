# Scripts for helping with AmrPlusPlus data analysis

This repository contains scripts for helping with data cleaning, processing and analysis of results generated with the AmrPlusPlus pipeline.

### `parse_amr_output.py`

__Purpose__: This script parses the Gene Ids (or headers) from the AmrPlusPlus database present in the results from Resistome Analyzer. The script divides those headers into AMR Class, Mechanism and group. The script will read all the Gene output files generated with Resistome Analyzer (*gene.tabular) that present in an user-provided directory, and will extract the Class, Mechanism and Group information from the Gene names. The output of the script is parsed CSV files. Those would have similar names as the input files, but with the word "parsed" in the filename. For example, if your input file is called `sample1_gene.tabular`, the output file will be called `sample1_gene_parsed.tabular`

__Usage__:

``parse_amr_output.py [name of directory]``

_Examples_

For present directory:

``parse_amr_output.py .``

For sub-directory:
``parse_amr_output.py ./resistome_results``



__Software Requirements__:

Python 3 (tested with Python 3.6.3). The `pandas` Python library (tested with version 22) is required as well.

### `buildingMegabio.py`

__Purpose__: This script builds a nucleotide MegaBio database (biocides and biometals) from aminoacid accession numbers from a database curated by CSU.

### `megabio_annotation.R`

__Purpose__: This script parses old annotation file, and filters it and generates a new annotation file with new FASTA headers from `edirect` search.
