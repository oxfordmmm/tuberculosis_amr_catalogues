# tuberculosis_amr_catalogues


A collection of published genetic catalogues for AMR prediction of *M. tuberculosis*. These can then be compared, or used for testing. To ensure this each conforms to a specific file format with a naming convention. These catalogues can then be used as inputs to [piezo](https://github.com/oxfordmmm/piezo), a Python module that parses the catalogue and makes resistance predictions for supplied genetic mutations.

## File format

Each catalogue must contain the following.

```
Field name          Description
GENBANK_REFERENCE   The identifier of the reference, including version, that this catalogue is with respect to e.g. NC_000962.2
CATALOGUE_NAME      The unique name of the catalogue e.g. LID2015A
CATALOGUE_VERSION   To allow development of catalogues e.g. v1.0
CATALOGUE_GRAMMAR   The grammar used to describe the genetic variation. The first use GM1, which is a protein-centric view and is described more below.
PREDICTION_VALUES   For qualitative catalogues only: the classifications used, in descending order of priority, in the catalogue. Many catalogues will be RUS, but RFUS is also a possibility to allow for differential treatment of HET calls, depending on where they occur.
DRUG                The drug identified using a 3 letter code e.g. RIF.
MUTATION            According to the specified grammar, a description of the genetic variant.
SOURCE              JSON to allow multiple entries detailing if this mutation has been included in multiple published catalogues, or is mentioned in a number of scientific papers. 
EVIDENCE            JSON to allow a flexible reporting of the evidence used to justify inclusion in this catalogue. Could include the number of resistant and sample samples containing this mutation, along with some estimate of its confidence.
OTHER               JSON to allow for inclusion for other useful information e.g. is this a lineage-defining mutation? 
```

## Available grammars

If the catalogue is to be interpreted by piezo, that code must understand the grammar being used. At present, piezo only knows about one grammar, called `GARC1`, which is described [here](http://fowlerlab.org/2018/11/25/goarc-a-general-ontology-for-antimicrobial-resistance-catalogues/) and also briefly in the README of the piezo module. In brief this is a protein-centric view of genetic variation, so where possible, variants are described according to their effect on the amino acids in the coding sequence of a gene (e.g. `rpoB@S450L`). If a variant occurs upstream of a coding region, it is assumed to be in the promoter of that gene and instead the base change is described relative to the start code of the coding sequence (e.g. `fabG1@c-15t`). Whilst convenient, this potentially makes describing variation a long way from a coding region difficult, however, at present, no such variants are know to confer resistance in TB. It also describes in the same way a potentially large number of different codons. For example, the apparent synymous mutation `fabG1@L203L` is known to confer resistance to `INH`, which at first examination does not make sense, however, this is really a promoter mutation for the upstream gene that happens to lie in the coding region of the downstream gene and since we are taking a protein-centric view, that is how the variant is described. Addition grammars can be added to piezo.

## Available catalogues

w.r.t version 2 of the NC_000962 / H37rV GenBank reference genome
```
$ ls catalogues/NC_000962.2/
NC_000962.2.gbk                         NC_000962.2_LID2015B_v1.0_GARC1_RUS.pkl
NC_000962.2_LID2015A_v1.0_GARC1_RUS.csv NC_000962.2_NEJM2018_v1.0_GARC1_RUS.csv
NC_000962.2_LID2015A_v1.0_GARC1_RUS.pkl NC_000962.2_NEJM2018_v1.0_GARC1_RUS.pkl
NC_000962.2_LID2015B_v1.0_GARC1_RUS.csv```
```

w.r.t version 3 of the NC_000962 / H37rV GenBank reference genome
```
$ ls catalogues/NC_000962.3/
NC_000962.3.gbk                          NC_000962.3_LID2015A_v1.1_GARC1_RUS.csv
NC_000962.3_CRyPTIC_v1.2_GARC1_RUS.csv   NC_000962.3_LID2015A_v1.1_GARC1_RUS.pkl
NC_000962.3_CRyPTIC_v1.2_GARC1_RUS.pkl   NC_000962.3_LID2015B_v1.1_GARC1_RUS.csv
NC_000962.3_CRyPTIC_v1.311_GARC1_RUS.csv NC_000962.3_LID2015B_v1.1_GARC1_RUS.pkl
NC_000962.3_CRyPTIC_v1.311_GARC1_RUS.pkl NC_000962.3_NEJM2018_v1.0_GARC1_RUS.csv
NC_000962.3_ERJ2017_v1.1_GARC1_RUS.csv   NC_000962.3_NEJM2018_v1.0_GARC1_RUS.pkl
NC_000962.3_ERJ2017_v1.1_GARC1_RUS.pkl
```

Note that there are small but significant differences between version2 and version3 of the NC_000962/H37rV reference so e.g. the two versions of the NEJM2018 catalogues are slightly different!

## Description 


| Name |   Version |      Description |
| ---- | ---- |--|
| LID2015A   | v1.1  | published via reference 1 below |
| LID2015B   | v1.1  | published via reference 1 below |
| ERJ2017    | v1.1   | published via reference 3 below |
| NEJM2018   |  v1.0 | published via reference 2 below |
| CRyPTIC  | v1.2 | unpublished; simple amalgam of NEJM2018 (INH,RIF,PZA,EMB) and ERJ2017 (other drugs) with some phyloSNPs also added |
| CRyPTIC  | v1.311 | published via reference 4 below | 


## Citations

If you use these catalogues, please cite

1. Walker TM, Kohl TA, Omar S V, Hedge J, Del Ojo Elias C, Bradley P, Iqbal Z, Feuerriegel S, Niehaus KE, Wilson DJ, Clifton DA, Kapatai G, Ip CLC, Bowden R, Drobniewski FA, Allix-Béguec C, Gaudin C, Parkhill J, Diel R, Supply P, Crook DW, Smith EG, Walker AS, Ismail N, Niemann S, Peto TEA, Modernizing Medical Microbiology (MMM) Informatics Group. 2015. Whole-genome sequencing for prediction of Mycobacterium tuberculosis drug susceptibility and resistance: a retrospective cohort study. Lancet Infec Dis 15:1193–202. [doi:10.1016/S1473-3099(15)00062-6](https://doi.org/10.1016/S1473-3099(15)00062-6)

2. The CRyPTIC Consortium, 100000 Genomes Project. 2018. Prediction of Susceptibility to First-Line Tuberculosis Drugs by DNA Sequencing. New Eng J Med 379:1403–1415. [doi:10.1056/NEJMoa1800474](https://doi.org/10.1056/NEJMoa1800474)

3. Miotto P, et al. (2017) A standardised method for interpreting the association between mutations and phenotypic drug resistance in Mycobacterium tuberculosis. Eur Respir J 50(6):1701354 [doi:10.1183/13993003.01354-2017](http://doi.org/10.1183/13993003.01354-2017)

4. The CRyPTIC Consortium (2021) Epidemiological cutoffs for a 96-well broth microtitre plate for high-throughput research antibiotic susceptibility testing of M . tuberculosis. medRxiv [doi:101101/2021022421252386](https://doi.org/10.1101/2021.02.24.21252386)



