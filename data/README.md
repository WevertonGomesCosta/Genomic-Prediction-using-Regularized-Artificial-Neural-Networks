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
used by [R02 — Data preparation](../analysis/real_data_audit.Rmd).
See the scientific references and access instructions below to obtain
the original genotype data.

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
Use this object to start the downstream genomic analyses directly.

### Scientific references and data access

Sousa, T. V., et al. (2019). Early selection enabled by the implementation
of genomic selection in *Coffea arabica* breeding. *Frontiers in Plant Science*,
9, 1934. <https://doi.org/10.3389/fpls.2018.01934>.

Sousa, T. V., et al. (2017). Population structure and genetic diversity of
coffee progenies derived from Catuaí and Híbrido de Timor revealed by
genome-wide SNP marker. *Tree Genetics & Genomes*, 13, 124.
[Article record — Embrapa](https://www.alice.cnptia.embrapa.br/alice/handle/doc/1081931).

Suela, M. M., et al. (2025). Structural Equation Modeling and Genome-Wide
Selection for Multiple Traits to Enhance Arabica Coffee Breeding Programs.
*Agronomy*, 15(7), 1686. <https://doi.org/10.3390/agronomy15071686>.

For access to the original genotype data, consult these publications
describing the population and marker data. The data availability
statement in Suela et al. (2025), which analyzes the same population
of 195 plants, directs data requests to coauthor Eveline Teixeira
Caixeta. Request the original marker matrix with individual identifiers
and prepare the RDS input in the format read by R02 at
`data/dados_reais/geno_real.rds`.

## Data availability and reproduction

| Input or product | Source or location |
|:--|:--|
| Six simulated source files | `data/dados_simulados/` |
| Real phenotypic source file | `data/dados_reais/coffee_phenotypes.txt` |
| Original real genotype data | Scientific references and access guidance above |
| Prepared simulated and real datasets | Versioned under `output/` |
| Rendered tutorial | Versioned under `docs/` |

Use the original data for the preparation modules or the saved prepared
datasets to start the downstream analyses. Cite the source publications
and consult the applicable data-use terms in [`LICENSE.md`](../LICENSE.md).

### Canonical file identities (SHA-256)

The following SHA-256 values describe the exact Git blob contents (not the
Git object identifiers) at commit
[`9576541`](https://github.com/WevertonGomesCosta/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/commit/9576541d37a77100eb77fc43bc73d48c6deac0ac),
the completed analytical version. Paths are relative to `data/`.

| Canonical file | Bytes in Git | SHA-256 of Git content |
|:--|--:|:--|
| `dados_simulados/DG#gen_F2_Vfen.txt` | 54123 | `07cbb8b2904a8033f49df0d2b066464187dd93f150d2431704ec2d8d11d0b587` |
| `dados_simulados/DG#gen_F2_Vgen.dat` | 54138 | `7a173cb2e691cd8edfa35cff0f2ac14f134d750401f358d3c9879d7e36e16cc7` |
| `dados_simulados/genoma_mapa.txt` | 12034010 | `ba8ec419b2fbcfa4b36bf5513f580537cf09a29fc28d74e8f4ce57d288101ea8` |
| `dados_simulados/genoma.txt` | 251965 | `fc1789b0efc22e8acbdfa9078a3f4eb6dca0f643733b2f1fb062e4ffc2ff1bfe` |
| `dados_simulados/controlegenetico#1.dat` | 5360 | `7240975f8a5176b1d11aaca081001d5758181a7439ee7fee70d954a205a002d2` |
| `dados_simulados/genoma_pais.txt` | 16401 | `43d46c2fabbf6ee56a33b249fdcf02c1b2e6d2c90c7dd9f7ddf5a7b368821c74` |
| `dados_reais/coffee_phenotypes.txt` | 24171 | `e6e966a663a120641a6030d62e514135ac74ce84dc7319abeed899ca503573f8` |

The seven local text files were checked on 2026-11-26. All matched their
reference Git objects after application of Git clean filters. Their raw
local byte counts and hashes differed, consistently with Windows CRLF
line endings. To verify a versioned file against the table, hash the
Git content rather than the working-tree bytes. For example, from the
repository root in Git Bash or a compatible shell:

```bash
git show '9576541:data/dados_simulados/DG#gen_F2_Vfen.txt' | sha256sum
git hash-object --path='data/dados_simulados/DG#gen_F2_Vfen.txt' 'data/dados_simulados/DG#gen_F2_Vfen.txt'
git rev-parse '9576541:data/dados_simulados/DG#gen_F2_Vfen.txt'
```

The first command checks the recorded SHA-256; the last two should
return the same Git object identifier for a matching local copy.
Apply the same procedure to the other versioned canonical files.

### Local real genotype input

Place the obtained RDS input at `data/dados_reais/geno_real.rds` for
R02. The following record identifies the local reference copy:

| Local file checked on 2026-11-26 | Bytes | SHA-256 of local content |
|:--|--:|:--|
| `dados_reais/geno_real.rds` | 974922 | `a8effc492ec01ea4f5fe68b1aefb052c6216cb79f1fa280645277dddba4034de` |

Compare the SHA-256 of the RDS with the recorded reference copy using:

```bash
sha256sum data/dados_reais/geno_real.rds
```

### Additional versioned files

`dados_simulados/genoma_mapa_tr.txt` and `dados_simulados/map.rds` are
also tracked in Git. Neither is referenced by the current M01 source;
they are not required canonical inputs for the documented reconstruction.

## Data and analysis directories

- `data/` — canonical source data;
- `analysis/` — scientific analysis definitions;
- `output/` — derived analytical objects and scientific results;
- `docs/` — rendered analytical website.

See the [repository README](../README.md) for the analytical sequence and
reproducibility overview, and the [output documentation](../output/README.md)
for the organization and interpretation of persisted results.
