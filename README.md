# BB2490 - Analysis of Data from High-throughput Molecular Biology Experiments
G1 - Phosphoproteome Project

## Project Description
You are to reanalyze a data set from the phosphoproteome study of HeLa cells, presented in Panniza et al. The data stems from cell cultures, that were lysed and fractionated using iso-electric focusing experiments.

For the project, primarily the phosphoproteomics runs are of interest.

1. To analyze the data, you should first convert your data from raw data to searchable data format like .mgf or .ms2 using msconvert (Proteowizard).
2. Search the data using crux/percolator or ms-gf+/percolator. In your searches use fix-modifications for carbamidomethylation on cysteine and TMT 10-plex on lysine and N-terminus, and use variable modifications of S, T or Y for phosphorylations.
3. Extract TMT quantities with compomics/reporter. 

* First, try to see how many phospho-sites you can localize.
* Second, see if you can cluster your data across conditions. Do your treatment groups cluster?

## Useful Links

### Dataset
http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD005410

### Paper & Supplementary Information
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5495806/

### .ms2 Dataset
https://drive.google.com/drive/u/0/folders/19nV1IcLbF2HDbYcscpVA_p7V801NOyup

### Crux 
#### Installation
http://crux.ms/tutorials/install.html
#### How to run?
http://crux.ms/tutorials/search.html
#### Label information (TMT 6-plex, TMT 10-plex)
http://crux.ms/faq.html

https://assets.thermofisher.com/TFS-Assets/LSG/manuals/MAN0015866_2162600_TMT_MassTagging_UG.pdf (TMT 10-plex, page 6)

http://www.biotech.cornell.edu/sites/default/files/uploads/Documents/Proteomics_protocols/Protocol%2017_TMT%20labeling.pdf (TMT 6-plex, page 9)
#### S,T,Y variable modifications
http://crux.ms/commands/tide-index.html (crux/tide-index --mods-spec)

### Dropbox 
https://www.dropbox.com/sh/oqhsahyz1dxt01j/AAA7ThJDdPXEQUT4CXVYYgEza?dl=0 
