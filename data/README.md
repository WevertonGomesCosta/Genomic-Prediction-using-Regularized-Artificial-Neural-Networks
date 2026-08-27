# Data

This directory contains input data used by the project. Derived analytical
objects, model outputs, diagnostics, and reported results belong under
`output/`, not under `data/`.

## Simulated data

The canonical public simulated-data workflow reads its source files from
`data/dados_simulados/`.

The eight inputs currently required by
`analysis/simulated_data_audit.Rmd` are:

- `controlegenetico#1.dat`
- `DG#gen_F2_Vfen.txt`
- `DG#gen_F2_Vgen.dat`
- `genoma.txt`
- `genoma_mapa.txt`
- `genoma_mapa_tr.txt`
- `genoma_pais.txt`
- `map.rds`

These files provide the simulated phenotypes, true genetic values, genotype
representations, genetic-map information, parental information, and simulation
metadata required by the canonical simulated-data audit.

The audit generates the validated common analytical object under
`output/simulated/audit/`. Downstream validation and modeling modules consume
that versioned output instead of preprocessing the raw inputs independently.

## Real coffee data

`data/dados_reais/` is reserved for the real *Coffea arabica* branch.

The underlying genotype, phenotype, annotation, and provenance files are
currently maintained locally and are not versioned in the public repository.
Their expected local filenames are documented by
`data/dados_reais/.gitignore`.

The real-data branch is not yet part of the canonical public analysis workflow.
Before genomic prediction results are reported, genotype quality control,
phenotype provenance and adjustment, validation design, and model comparison
must be audited under the same reproducibility principles used for the
simulated-data branch.

## Directory contract

- `data/` — source/input data only;
- `analysis/` — scientific workflowr analyses;
- `code/` — reusable supporting code and local legacy-code documentation;
- `output/` — versioned derived objects and canonical scientific results;
- `.local/` — ignored runtime artifacts such as checkpoints, logs, pilots, and
  diagnostics.

Historical analysis scripts are not treated as input data. Local copies are
preserved under the ignored `code/legacy/` directory for reference only and
are not part of the canonical workflow.
