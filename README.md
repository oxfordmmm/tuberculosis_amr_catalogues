# tuberculosis_amr_catalogues
A collection of genetic catalogues for AMR prediction of M. tuberculosis. 

The idea is that the GitHub repository becomes the master version of existing and new MBTC AMR catalogues.

## File format

Each catalogue must conform to the following.

```
Field name          Description
CATALOGUE_NAME      The unique name of the catalogue e.g. LID2015A
GENBANK_REFERENCE   The identifier of the reference, including version, that this catalogue is with respect to e.g. NC_000962.2
DRUG                Which drug? e.g. RIF
GENE                The gene (must match a GENE or LOCUS entry in the relevant Genbank file)
MUTATION            The mutation formed as per the NOMENCLATURE
POSITION            The position (amino acid residue if appropriate, otherwise nucleotide relative to the start codon)
GENE_TYPE           One of GENE, RNA or LOCUS depending on the description in the relevant Genbank file
VARIANT_AFFECTS     One of CDS, RNA or PROM. RNA only applies for RNA encoding genes, like rrs 
VARIANT_TYPE        One of SNP or INDEL
INDEL_1             The first layer below the top foo_indel layer e.g. foo_ins
INDEL_2             The next layer of a deeper description e.g. foo_ins_2
INDEL_3             The final layer e.g. foo_ins_at (note not defined for deletions since one does not know what was deleted)
SOURCE              Some indication of how this row arose
PREDICTION          The prediction. One of R, S, U and sometimes also F.
```

## Available catalogues

w.r.t version 2 of the NC_000962 / H37rV GenBank reference genome
```
NC_000962/version2/NC_000962.2_LID2015A_RUS_catalogue_v1.0
NC_000962/version2/NC_000962.2_LID2015B_RUS_catalogue_v1.0
NC_000962/version2/NC_000962.2_NEJM2018_RUS_catalogue_v1.0
```

w.r.t version 3 of the NC_000962 / H37rV GenBank reference genome
```
NC_000962/version3/NC_000962.3_NEJM2018_RUS_catalogue_v1.0
NC_000962/version3/NC_000962.3_CRyPTICv1.0_RUS_catalogue_v1.0
NC_000962/version3/NC_000962.3_CRyPTICv1.1_RUS_catalogue_v1.0
NC_000962/version3/NC_000962.3_CRyPTICv1.2_RUS_catalogue_v1.0
```
Note that there are small but significant differences between version2 and version3 of the NC_000962/H37rV reference so e.g. the two versions of the NEJM2018 catalogues are different!


