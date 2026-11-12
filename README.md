# Genomic Prediction using Regularized Artificial Neural Networks

This repository contains a reproducible genomic-prediction study comparing
L1/L2-regularized artificial neural networks with a GBLUP-ADE genomic mixed
model.

The project contains two complementary analytical branches:

- simulated genomic data, for which true genetic values are known;
- real *Coffea arabica* data, for which longitudinal field observations are
  analyzed with mixed models before genomic prediction.

Both branches use modular `workflowr` analyses with separate stages for data
preparation, validation design, model fitting, and model comparison.

## Scientific objective

The primary objective is to evaluate whether neural-network weight
regularization improves predictive performance and generalization in genomic
prediction relative to a GBLUP-ADE benchmark.

Four artificial-neural-network configurations are evaluated:

- **ANN-0** — no L1/L2 weight penalty;
- **ANN-L1** — L1 regularization;
- **ANN-L2** — L2 regularization;
- **ANN-L1+L2** — simultaneous L1 and L2 regularization.

The genomic mixed-model benchmark is **GBLUP-ADE**, including additive,
dominance, and epistatic genomic effects.

## Simulated-data workflow

The simulated-data branch follows five analytical modules:

```text
simulated_data_audit.Rmd
        |
        v
simulated_data_validation.Rmd
        |
        +-------------------+
        |                   |
        v                   v
simulated_data_gblup.Rmd   simulated_data_ann.Rmd
        |                   |
        +---------+---------+
                  |
                  v
      simulated_data_comparison.Rmd
```

The modules have distinct responsibilities:

1. `simulated_data_audit.Rmd` prepares and describes the simulated genotype,
   phenotype, true genetic-value, genetic-map, and simulation-scenario data.
2. `simulated_data_validation.Rmd` defines the common outer and inner
   cross-validation design.
3. `simulated_data_gblup.Rmd` fits and evaluates GBLUP-ADE.
4. `simulated_data_ann.Rmd` fits the four ANN configurations and performs
   training-only hyperparameter and epoch selection.
5. `simulated_data_comparison.Rmd` compares the saved model results under the
   common validation design.

## Real-data workflow

The real-data branch adds an explicit phenotypic-analysis stage before genomic
data are introduced:

```text
real_data_phenotype.Rmd
        |
        v
real_data_audit.Rmd
        |
        v
real_data_validation.Rmd
        |
        +-------------------+
        |                   |
        v                   v
real_data_gblup.Rmd       real_data_ann.Rmd
        |                   |
        +---------+---------+
                  |
                  v
        real_data_comparison.Rmd
```

The six modules have separate responsibilities.

1. **Phenotypic analysis — `real_data_phenotype.Rmd`**

   Uses the complete longitudinal *Coffea arabica* field dataset. The module
   describes and organizes the repeated observations, specifies the phenotypic
   mixed model, estimates variance components by REML with `sommer`, and
   obtains the final individual genotypic BLUPs used as phenotypic targets for
   genomic prediction.

   Genomic marker data are not used in this module.

2. **Data integration and genotype preparation — `real_data_audit.Rmd`**

   Reads the phenotypic BLUPs and `geno_real.rds`, establishes the common set
   and order of individuals, verifies genotype structure, applies the defined
   marker quality-control rules, and creates the common real-data object used
   by all subsequent modules.

3. **Validation design — `real_data_validation.Rmd`**

   Defines the common outer and inner cross-validation partitions used by
   GBLUP-ADE and all ANN configurations.

4. **GBLUP-ADE — `real_data_gblup.Rmd`**

   Fits the genomic mixed model and generates held-out genomic predictions
   under the common validation design.

5. **Regularized ANN — `real_data_ann.Rmd`**

   Fits ANN-0, ANN-L1, ANN-L2, and ANN-L1+L2. Hyperparameter and epoch
   selection are restricted to the corresponding analysis sample.

6. **Model comparison — `real_data_comparison.Rmd`**

   Reads the saved GBLUP-ADE and ANN results and performs the terminal
   task-matched comparison without refitting either model family.

## Validation principles

The model-comparison design follows common rules across methods:

- competing models use the same outer-assessment partitions;
- outer-assessment responses are excluded from model fitting and model
  selection;
- ANN hyperparameter and epoch selection use only the corresponding
  outer-analysis sample;
- preprocessing that depends on the response or training sample is estimated
  without access to the outer-assessment responses;
- model comparisons use matched held-out individuals;
- predictive metrics are calculated under the same task definitions.

For simulated data, known true genetic values provide an independent primary
evaluation target. For real data, the phenotypic mixed-model stage supplies
the individual genotypic BLUPs used as the response for genomic prediction.

## Repository structure

- `analysis/` — `workflowr` source pages defining the analytical modules;
- `data/` — canonical source data and data contracts;
- `code/` — reusable functions and command-line utilities shared across
  modules;
- `output/` — derived analytical objects, model outputs, tables, and figures;
- `docs/` — rendered `workflowr` website;
- `renv.lock` — project dependency lockfile.

Detailed directory contracts are documented in:

- [`data/README.md`](data/README.md);
- [`code/README.md`](code/README.md);
- [`output/README.md`](output/README.md).

## Reproducibility

The project is implemented in R using R Markdown, `workflowr`, and `renv`.

Each analytical stage has a defined input and output contract. Computationally
intensive fitting can be executed deliberately and its derived objects saved
under `output/`, allowing the rendered site to present the complete analytical
procedure without requiring expensive model fitting during every routine
render.

Package versions are recorded in `renv.lock`, source analyses are stored under
`analysis/`, and the rendered website is stored under `docs/`.

## Citation

If you use this repository, please cite it using the metadata provided in
[`CITATION.cff`](CITATION.cff).

## License

Except where otherwise indicated, the original analytical materials in this
repository are licensed under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International license
(CC BY-NC-SA 4.0). See [`LICENSE.md`](LICENSE.md).
