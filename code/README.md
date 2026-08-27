# Code

Shared functions and command-line utilities that support multiple analysis
modules may be stored here when they are genuinely reusable.

Scientific stages that generate or interpret reported results belong in the
corresponding workflowr source page under `analysis/`. The canonical simulated
GBLUP-ADE versus ANN comparison is therefore implemented in
`analysis/simulated_data_comparison.Rmd`, not as a standalone script.

## Local legacy scripts

Historical exploratory scripts may be retained locally under `code/legacy/`.

This directory is ignored by Git and is not part of the canonical scientific
workflow.

The currently preserved local legacy files are:

- `Redes_nao_regularizadas.txt`
- `Redes_neuralnet.txt`
- `Redes_regularizadas.txt`

These files represent earlier ANN experiments, including obsolete local file
paths, packages, datasets, validation strategies, and modeling protocols. They
must not be used as a source of canonical results or as an implementation
reference for the current ANN workflow.

Their Git history remains available from the earlier versions in which they
were stored under `data/`.
