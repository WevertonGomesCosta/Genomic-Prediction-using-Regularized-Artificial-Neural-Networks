# Data

This directory contains the source data used by the project. Derived analytical
objects, model results, predictions, tables, and figures are organized under
[`output/`](../output/README.md). Source data are not modified in place by
downstream analysis modules.

The project combines a controlled simulated genomic population and real
phenotypic and genomic data from *Coffea arabica*. The two datasets support
complementary assessments of genomic prediction.

## Simulated genomic data

### Canonical source files

The simulated-data workflow reads the following files from
`data/dados_simulados/`. All six files are versioned in Git.

| File | Content |
|:--|:--|
| `DG#gen_F2_Vfen.txt` | Simulated phenotypic values for the six genetic scenarios |
| `DG#gen_F2_Vgen.dat` | Known true genetic values for the six scenarios |
| `genoma_mapa.txt` | Marker genotype matrix |
| `genoma.txt` | Genetic-map information |
| `controlegenetico#1.dat` | Simulation settings and QTL information |
| `genoma_pais.txt` | Parental genotypes |

### Population and marker structure

The data were generated using GENES. The F2 population contains 1,000
individuals and 4,010 markers distributed across ten linkage groups, with
401 markers per group and 0.5 cM between consecutive markers. The six genetic
scenarios (C1–C6) differ in QTL number and nominal heritability; they are not
six independent measured traits.

The marker genotypes are read in their original 0/1/2 representation and
reoriented to individuals by markers. The prediction modules use the
corresponding -1/0/1 marker coding. Phenotypes, true genetic values and
genotypes retain the same individual order.

### Prediction targets and prepared data

Simulated phenotypes are the response for model fitting. Known true genetic
values are reserved for predictive assessment and do not participate in model
fitting, hyperparameter selection or training-duration selection. Evaluation
against simulated phenotypes complements the primary assessment against true
genetic values.

[M01 — Data preparation](../analysis/simulated_data_audit.Rmd) reads the source
files and creates `output/simulated/audit/preprocessed_simulated_common.rds`,
the shared input to the validation and model-fitting modules. The scenario
settings, genetic map, QTL distribution and genotype coding are explained in
M01. [M05 — Model comparison](../analysis/simulated_data_comparison.Rmd)
presents the results separately by scenario and evaluation target.

### Scientific references

- Cruz, C. D. (2013). GENES — a software package for analysis in experimental
  statistics and quantitative genetics. *Acta Scientiarum*, 35(3), 271–276.
- Cruz, C. D. (2016). Genes Software — extended and integrated with the R,
  Matlab and Selegen. *Acta Scientiarum*, 38(4), 547–552.

## Real Coffea arabica data

### Phenotypic data and experimental population

The canonical phenotypic input,
`data/dados_reais/coffee_phenotypes.txt`, is versioned in Git and is read by
[R01 — Phenotypes](../analysis/real_data_phenotype.Rmd).

| Feature | Description |
|:--|:--|
| Field observations | 684 |
| Permanent plant identifiers | 228 |
| Evaluation years | 2014–2016 |
| Experimental progenies | 13 (progenies 1–13) |
| Checks | 2 (progenies 14–15) |
| Target genomic-prediction population | 195 individuals |

The three analyzed traits are:

| Code | Description |
|:--|:--|
| Cer | Cercosporiosis score |
| BM | Leaf-miner incidence score |
| LP | Production-related phenotype |

The two checks remain in the phenotypic mixed-model analysis. Seven
zero-coded non-observations for LP are excluded from its mixed-model fit.
The individual BLUPs for the 195 target plants are estimated from the
available field observations before integration with genomic markers.
Genomic information is not used in this phenotypic adjustment.

The BLUPs are derived analytical objects, stored under
`output/real/phenotype/`. They are the response and assessment reference
for the real-data genomic models, not known true genetic values.

### Genomic marker data and quality control

`data/dados_reais/geno_real.rds` is the canonical local genotype input
required by [R02 — Data preparation](../analysis/real_data_audit.Rmd).
This raw genotype file is not available in the versioned repository at
that path.

The population comprises 195 individuals from 13 progenies. Capture-Seq
genotyping produced the original panel of 21,620 SNPs. The common
marker quality-control procedure retains 20,887 SNPs with -1/0/1 genotype
coding.

| Criterion | Retention rule |
|:--|:--|
| Call rate | At least 90% |
| Minor allele frequency (MAF) | At least 0.05 |
| Observed heterozygosity | Less than 100% |

R02 aligns individual identifiers between the genotype matrix and the
phenotypic BLUPs and applies the same marker quality control to the common
panel. All seven genomic prediction methods use the same aligned individuals,
marker panel and prediction targets.

The resulting prepared object,
`output/real/audit/preprocessed_real_common.rds`, is versioned in Git.
It contains the retained genotypes and aligned prediction targets and is
the input to the downstream genomic validation and model-fitting stages.
It is a derived analytical object, not a replacement for the original
genotype file when reconstructing R02 from raw inputs.

### Scientific reference

Sousa, T. V., et al. (2019). Early selection enabled by the implementation
of genomic selection in *Coffea arabica* breeding. *Frontiers in Plant Science*,
9, 1934. <https://doi.org/10.3389/fpls.2018.01934>.

## Data availability and reproducibility

| Input or product | Availability |
|:--|:--|
| Six simulated source files | Versioned in Git |
| Real phenotypic source file | Versioned in Git |
| Raw real genotype file (`geno_real.rds`) | Required locally; not available at the canonical repository path |
| Prepared simulated and real datasets | Versioned under `output/` |
| Rendered tutorial | Versioned under `docs/` |

The published tutorial can be inspected without reconstructing the
analyses. The prepared datasets provide inputs for the downstream stages,
subject to the availability of the other required objects and software
dependencies. Full reconstruction from raw inputs additionally requires
access to the canonical real genotype file. A fresh clone alone does not
provide that file.

Source datasets and third-party materials remain subject to their own
licensing, access, citation and provenance conditions, as described in
[`LICENSE.md`](../LICENSE.md).

## Data and analysis directories

- `data/` — canonical source data;
- `analysis/` — scientific analysis definitions;
- `output/` — derived analytical objects and scientific results;
- `docs/` — rendered analytical website.

See the [repository README](../README.md) for the analytical sequence and
reproducibility overview, and the [output documentation](../output/README.md)
for the organization and interpretation of persisted results.
