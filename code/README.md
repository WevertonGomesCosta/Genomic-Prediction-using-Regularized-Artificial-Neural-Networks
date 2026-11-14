# Code

This directory is reserved for reusable functions and command-line utilities
shared by multiple analysis modules.

Scientific stages that define or interpret results belong in the corresponding
R Markdown source page under `analysis/`.

The main analysis sequence is implemented in the dataset-specific `workflowr`
modules rather than in standalone scripts.

Reusable code placed in this directory should:

- have a clearly defined input and output contract;
- avoid machine-specific absolute paths;
- avoid duplicating scientific logic defined in an analysis module;
- be called explicitly by the analysis pages that depend on it;
- preserve deterministic behavior whenever reproducible results require it.

Dataset-specific model fitting, validation, and model comparison remain in
their respective `analysis/*.Rmd` modules.
