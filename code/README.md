# Code

Command-line scripts and shared source code supporting the reproducible
workflow are stored here.

## Canonical simulated-data comparison

`simulated_model_comparison.R` generates the four canonical descriptive
GBLUP-ADE vs ANN comparison tables under `output/simulated/comparison/`.

It consumes already validated canonical model-result objects and does not refit
GBLUP-ADE or ANN models.
