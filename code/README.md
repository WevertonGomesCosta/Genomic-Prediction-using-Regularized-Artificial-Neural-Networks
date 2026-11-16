# Code

This directory contains reusable functions and analytical utilities shared by multiple modules.

Scientific analyses and their interpretation are presented in the corresponding R Markdown modules under `analysis/`.

The main analyses are implemented in the dataset-specific `workflowr` modules.

Reusable code placed in this directory should:

- define inputs and outputs explicitly;
- avoid machine-specific absolute paths;
- avoid duplicating scientific logic defined in an analysis module;
- be called explicitly by the analysis pages that depend on it;
- preserve deterministic behavior whenever reproducible results require it.

Dataset-specific model fitting, validation, and model comparison remain in
their respective `analysis/*.Rmd` modules.
