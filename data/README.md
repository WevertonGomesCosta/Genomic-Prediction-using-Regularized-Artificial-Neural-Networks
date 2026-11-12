# Data

This directory contains the source data used by the project.

Derived analytical objects, fitted-model results, predictions, diagnostics,
tables, and figures belong under `output/`.

## Simulated data

The simulated-data workflow reads its canonical inputs from
`data/dados_simulados/`.

The source files provide simulated phenotypes, true genetic values, genotype
representations, genetic-map information, parental information, and
simulation-scenario metadata.

`analysis/simulated_data_audit.Rmd` prepares these sources and creates the
common simulated-data object consumed by the validation and model-fitting
modules.

## Real Coffea arabica data

The real-data workflow uses two distinct source components.

### Longitudinal phenotypic data

The complete repeated field observations are the input to
`analysis/real_data_phenotype.Rmd`.

The phenotypic module uses all observations required by the experimental
mixed-model analysis before any integration with genomic marker data.

It produces individual genotypic BLUPs for the target traits. These BLUPs are
derived analytical objects and are stored under `output/real/phenotype/`.

### Genomic marker data

`geno_real.rds` is the canonical genotype object for the real-data genomic
workflow.

The genotype object is introduced only in `analysis/real_data_audit.Rmd`,
after the phenotypic mixed-model stage is complete.

That module aligns the genotyped individuals with the phenotypic BLUPs,
performs the defined marker quality control, and creates the common real-data
object used by validation, GBLUP-ADE, ANN, and model-comparison modules.

## Directory contract

- `data/` — canonical source data;
- `analysis/` — scientific analysis definitions;
- `code/` — reusable analytical functions and utilities;
- `output/` — derived analytical objects and scientific results;
- `docs/` — rendered analytical website;
- `.local/` — machine-local runtime files that are not part of the scientific
  output contract.

Source data are not modified in place by downstream analysis modules.
