# A General Ontology for Antimicrobial Resistance Catalogues (GOARC)

## Assumptions

* Resistance to an antimicrobial can be predicted by genetics i.e. the presence or absence of specific genetic sequences. AMR catalogues therefore need to specify
   * the presence of absence of genes (i.e. coding sequences)
   * changes, insertions or deletions to coding sequences and also to promoter regions
* Any code that parses catalogues should
   * apply general rules first and specific rules last to allow specific entries to override general entries.
   * have unit testing using known, high-confidence mutations to provide confidence that the code is working as intended
* Where possible, catalogues should be complete and computer-readable i.e. no logic should be written in to any computer code and the catalogue should not contain rules written in sentences! For example, catalogues should specify the effect of synonymous mutations in the coding region of genes of interest.
* This ontology is designed with non-additive qualitative AMR catalogues in mind i.e. if both mutations X and Y confer Resistance, then having both mutations present would also lead to a prediction of R. Using the ontology for quantitative, additive catalogues which predict the change in minimum inhibitor concentration (MIC) with respect to an arbitary reference (e.g. the mode MIC for susceptible strains) would be simple. Since each row is a mutation, describing non-linearities is more challenging. This could be achieved by allowing an entry in the catalogue to be a list of mutations (or gene presences) which, being more specific, would then override any more general rules.

## Nomenclature

### Genes

For core chromosomal genes, the name of the gene in the catalogue must match either the gene name or locus tag in the GenBank reference. E.g. *rpoB* in *M. tuberculosis* can also be referred to as *Rv0667*.

```
gene            759807..763325
                     /gene="rpoB"
                     /locus_tag="Rv0667"
```

For genes that are not present in the reference genome for a species, for example plasmid or other mobile genetic elements, ensuring consistency of nomenclature is more difficult. The developer must ensure that the name given to specific genetic elements by the bioinformatics workflow matches the name found in the catalogue, otherwise there will be false negatives leading to very major errors.

### Amino acids and nucleotides

* Amino acids are always given in UPPERCASE. Nucleotides in lowercase. This should be checked by the code and fail if this is not the case ('halt and catch fire').
* Het calls at present are given by the letter z, hence `Z` for an amino acid or `z` for a base.
* Likewise, null calls are given by the letter x, hence `X` for an amino acid or `x` for a base.
* Hence code should insist that

```
aminoacids in ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z','!']

nucleotides in ['a','c','t','g','x','z']
```

### Wildcards and other special characters

This is designed to be general and expandable (especially for indels)

* `*` is reserved to mean any residue (or base, depending on context). Note that `-*` is expanded to mean 'any promoter position'
* `!` is reserved for the STOP codon. This is defined in the private method `_setup_conversion_dicts()` in `cryptic.genetics.gene` (rather than `Stop` or `*` as previously)
* `?` is a wildcard for any non-synonmous mutation (including hets and nulls) and `=` is a wildcard for the synoymous mutation

## Catalogue entries

### Presence or absence of genes

This is the highest level of the hierarchy and these rules are therefore applied first. A gene presence entry is simply

`oxa48`

To avoid confusion with the wildcards, we use `~` to indicate logical NOT hence

`~oxa48`

indicates the absence of gene *oxa48*.

### Genetic mutations

* There are two types of mutations: single nucleotide polymorphisms (SNP) or insertions/deletions (INDEL), each of which can apply to a coding region of a protein (CDS) or the coding region of ribosomal RNA (RNA) or a promoter (PROM). A CDS is always translated into an amino acid sequence and hence the numeric position is the number of the amino acid residue, whereas a gene encoding rRNA needs to be treated as nucleotides, so is not translated.
* In the catalogue these are specified by the TYPE (SNP or INDEL) and AFFECTS (CDS, RNA or PROM). No other values are allowed.

### Single nucleotide polymorphisms (SNPs)

The general format is

`gene_mutation`

Splitting the mutation on underscore (`_`) therefore always gives you 2 strings which is used to identfy this as a SNP. Below are three examples for a CDS, RNA and PROM SNP:

`rpoB_S450L`, `rrs_a1402t` and `fabG1_c-15t`.

Note that position is context dependent! Hence for the CDS mutation it is amino acid number, whilst for the RNA and PROM mutation it is nucleotide number! Since the reference amino acid or base is recorded in all cases, this is always checked against the supplied (H37rV) Genbank file and a warning is logged if it is different - this likely indicates a different reference was used to define the mutation. The catalogue has, however, been checked for consistency against the catalogue using [gemucator](https://github.com/philipwfowler/gemucator) so any warnings generate merit investigation.

Any non-synonymous mutation can be encoded as

`rpoB_S450?`, `rrs_a1402?` and `fabG1_c-15?`

Any non-synonymous (which is has to be) mutation to the stop codon only makes sense for CDS mutations i.e.

`rpoB_!1172?`

The synonymous mutations are obviously

`rpoB_S450S`, `rrs_a1402a`, `fabG1_c-15c`

Allowing `*` to mean 'any position' then we can start to create more complex rules.

For example, any non-synonymous mutation at any amino acid in the coding sequences of these genes

`rpoB_*?`, `rrs_*?`, `fabG1_*?`

Whilst any non-synonymous mutation in the promoter of these genes is

`rpoB_-*?`, `rrs-*?`, `fabG1_-*?`

Note that the reference amino acid or base cannot, and therefore is not, specified. Likewise, all synonymous mutations in the coding sequences are

`rpoB_*=`, `rrs_*=`, `fabG1_*=`

Lastly, these rules have to be applied in a descending hierarchy which is based on the assumption that more specfic rules should override more general rules. This is a made up example.
```
rpoB_*= S
rpoB_*?  U
rpoB_S450? R
rpoB_S450T S
```
The first two rules say that synonymous mutations in the coding region of rpoB have no effect but any non-synonymous mutation has an unknown effect (U). The third second rule overrides this at position 450 so adds "except at position 450 where any non-synonymous mutation is classified R", then the final rule adds a final exception "except if the alt/target amino acid is Threonine, in which case it is classified S.

An important implication of this is that the rules can INTERACT and these needs to be born in mind (but this was always true..)

### Mixed calls (HETs)

Consider a complex example where one may wish to differentiate the prediction for a mixed (i.e. HET) call depending on whether the site is associated with resistance or not. Specifically, if we see a mixed call in a gene associated with resistance but there are is no evidence of resistance (i.e. rows in the catalogue predicting R) at this site then we might wish to classify these mixed calls as susceptible, S. But if we see a mixed call at a site that is associated with resistance we may wish to classify this as a fail, F, (or perhaps resistant, R). Rather than include complex logic into the code itself, we can do this with the appropriate rule set. To adopt this behavior for `rpoB_S450Z` we need to insert an additional rule.

```
rpoB_*= S
rpoB_*?  U
rpoB_S450? R
rpoB_S450Z F
rpoB_S450T S
```

### Insertions or deletions of nucleotides (INDELs)

INDELs require a more complex hierarchy, although only the top level is used for the time being. The top level is

`gene_position_indel`

e.g. `rpoB_1300_indel`

which means any insertion or deletion of any length at this position. If position is positive it is the nucleotide number within the coding sequence. If negative, it is within the promoter.

This can be overridden with more specific rules, the first of which is

`gene_position_fs`

e.g. `rpoB_1300_fs`

which means any frame-shifting mutation at the position. In other words the length of the insertion or deletion is not divisible by three. Then we have a more specific format

`gene_position_type_length`

where the length is specified e.g.

`rpoB_1300_ins_2`

means any insertion of two bases at position 1300 in rpoB. Logically, the numbering is again nucleotide (not amino acid residue). Finally, and not implemented yet, the specific bases inserted can be specific

`rpoB_1300_ins_ca`

Note that the deepest rule for deletions is the layer above i.e. `rpoB_1300_del_2` since we cannot specific which bases were deleted! Hence we end up with this descending hierarchy

```
rpoB_*_indel                        any insertion or deletion in the CDS of rpoB
rpoB_*_ins, rpoB_*_del              any insertion (or deletion) in the CDS
rpoB_*_ins_2, rpoB_*_del_2          any insertion of 2 bases (or deletion of 2 bases) in the CDS
rpoB_*_fs                           any frameshifting insertion or deletion in the CDS (notice that this is rpoB_*_ins_1 + rpoB_*_ins_2 + rpoB_*_ins_4 + rpoB_*_ins_5 +... and the same for deletions)
rpoB_1300_indel                     any insertion or deletion at nucleotide 1300 in the CDS
rpoB_1300_ins, rpoB_1300_del        any insertion (or deletion) at nucleotide 1300 in the CDS
rpoB_1300_ins_2, rpoB_1300_del_2    any insertion of length 2 (or deletion of length 2) in the CDS
rpoB_1300_ins_ca                    insertion of bases ca at position 1300 in the CDS (does not make sense for deletions)
```

Hence to specify any insertion that doesn't frame shift is susceptible, but any frame shifting insertions (i.e. introduces whole numbers of amino acids) confer resistance, whilst not enough deletions have been observed to classify. In addition insertions at position 1300 are classified as conferring resistance.

```
rpoB_*_ins    S
rpoB_*_del    U
rpoB_*_fs     R
rpoB_1300_ins R
```

Here the hierarchy ensures that the susceptible insertions (or unknown deletions) that are actually frame shifts can overriden with an R.

For promoters the picture is a bit more straightforward since there is no concept of a frame shift.

```
fabG1_-*_indel                      any insertion or deletion in the promoter of fabG1
fabG1_-*_ins, fabG1_-*_del          any insertion (or deletion) in the promoter
fabG1_-15_indel                     any insertion or deletion at nucleotide -15 in the promoter
fabG1_-15_ins_2, fabG1_-15_del_2    any insertion of length 2 (or deletion of length 2) in the promoter
fabG1_-15_ins_ca                    insertion of bases ca at position -15 in the promoter
```
