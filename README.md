# Scripts for helping with AmrPlusPlus data analysis

This repository contains scripts for helping with data cleaning, processing and analysis of results generated with the AmrPlusPlus pipeline.

### `parse_amr_output.py`

__Function__: This script parses the Gene Ids (or headers) from the AmrPlusPlus database present in the results from CoverageSampler. The script divides those headers into AMR Class, Mechanism and group.

__Usage__:

`` $ for i in `ls *.tabular`; do parse_amr_output.py $i; done``
