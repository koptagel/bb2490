# BB2490 - Analysis of Data from High-throughput Molecular Biology Experiments
G1 - Phosphoproteome Project

## Project Description
You are to reanalyze a data set from the phosphoproteome study of HeLa cells, presented in Panniza et al. The data stems from cell cultures, that were lysed and fractionated using iso-electric focusing experiments.

For the project, primarily the phosphoproteomics runs are of interest.

1. To analyze the data, you should first convert your data from raw data to searchable data format like .mgf or .ms2 using msconvert (Proteowizard).
2. Search the data using crux/percolator or ms-gf+/percolator. In your searches use fix-modifications for carbamidomethylation on cysteine and TMT 10-plex on lysine and N-terminus, and use open modifications for phosphorylations.
3. Extract TMT quantities with compomics/reporter. 

* First, try to see how many phospho-sites you can localize.
* Second, see if you can cluster your data across conditions. Do your treatment groups cluster?

## Useful Links

### Dataset
http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD005410

### Paper & Supplementary Information
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5495806/
