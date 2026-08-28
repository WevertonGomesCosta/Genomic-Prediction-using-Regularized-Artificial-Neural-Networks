# Genomic Prediction using Regularized Artificial Neural Networks

This repository contains a reproducible genomic-prediction study comparing
L1/L2-regularized artificial neural networks with a GBLUP-ADE genomic mixed
model under a common frozen cross-validation design.

The primary objective is to evaluate whether neural-network weight
regularization improves predictive performance and generalization in
high-dimensional genomic prediction problems.

## Scientific scope

The validated public workflow currently covers the **simulated-data branch**,
where true genetic values are known and can be used for independent predictive
assessment.

A real *Coffea arabica* extension is planned under the same validation
principles, but it is not yet part of the canonical public analysis.

## Models

Five models are compared under the same outer validation design:

- **GBLUP-ADE** — additive, dominance, and epistatic genomic effects;
- **ANN-0** — artificial neural network without L1/L2 weight penalties;
- **ANN-L1** — ANN with L1 weight regularization;
- **ANN-L2** — ANN with L2 weight regularization;
- **ANN-L1+L2** — ANN with simultaneous L1 and L2 weight penalties.

## Canonical simulated-data workflow

The public workflow is:

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

The modules have distinct roles:

1. `simulated_data_audit.Rmd` — audits data integrity, provenance, genotype and
   phenotype structure, QTL information, and simulation-scenario properties;
2. `simulated_data_validation.Rmd` — defines the frozen outer and inner
   cross-validation design shared by all competing methods;
3. `simulated_data_gblup.Rmd` — fits and evaluates the GBLUP-ADE branch;
4. `simulated_data_ann.Rmd` — defines the regularized ANN branch, including
   nested hyperparameter selection, epoch selection, final refitting, and
   held-out prediction;
5. `simulated_data_comparison.Rmd` — performs the terminal, task-matched
   comparison of GBLUP-ADE and ANN results under the shared frozen validation
   design.

ANN hyperparameter tuning is part of the ANN analysis itself rather than a
separate public module.

## Validation design

The simulated-data comparison uses the same frozen outer partitions for all
models.

- ANN hyperparameter selection is restricted to the outer-analysis sample.
- Outer-assessment individuals are excluded from ANN hyperparameter and epoch
  selection.
- Preprocessing parameters are estimated from training data only.
- True simulated genetic values are excluded from fitting and selection and are
  used only for final evaluation.
- GBLUP-ADE and all ANN variants are evaluated on the same held-out individuals
  within each task.
- Genetic-value prediction is the primary outcome; phenotype prediction is
  retained as a secondary outcome.
- Correlation, RMSE, MAE, bias, slope, and R-squared are computed under the same
  held-out design.

## Main findings

Within the prespecified canonical model and ANN architecture search space,
**GBLUP-ADE provides the strongest overall predictive performance**. It has the
highest mean genetic correlation and R-squared, and the lowest mean genetic
RMSE, in all six simulated scenarios.

Among the neural networks, **ANN-L1+L2 has the best overall averages by a very
small margin over ANN-L1**. ANN-L2 remains close to the unregularized ANN,
indicating that the observed regularization gain is driven mainly by the L1
component.

These results describe the frozen validation design and bounded model search
evaluated in this project; they do not establish a universal ranking between
genomic mixed models and all possible neural-network architectures.

## Repository structure

- `analysis/` — workflowr source pages for the public analysis;
- `data/` — input-data area and data documentation;
- `code/` — reusable helper code;
- `output/` — validated derived objects and canonical analysis results;
- `docs/` — generated workflowr website;
- `renv.lock` — project dependency lockfile.

More detailed contracts are documented in:

- [`data/README.md`](data/README.md);
- [`code/README.md`](code/README.md);
- [`output/README.md`](output/README.md).

## Reproducibility

The project is implemented in R using R Markdown, `workflowr`, and `renv`.

Routine site rendering uses the validated saved analysis outputs rather than
repeating computationally intensive model fitting. Scientific analysis pages
retain `sessionInfo()` so that the R session used for each render remains
documented, while project-level package versions are recorded in `renv.lock`.

The generated website is stored under `docs/`, and the corresponding source
analyses remain under `analysis/`.

## Citation

If you use this repository, please cite it using the metadata provided in
[`CITATION.cff`](CITATION.cff).

## License

Except where otherwise indicated, the original analytical materials in this
repository are licensed under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International license
(CC BY-NC-SA 4.0). See [`LICENSE.md`](LICENSE.md) for the repository-level
license statement. Source data and third-party materials remain subject to
their own provenance, authorization, and licensing conditions.
