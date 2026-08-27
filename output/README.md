# Output

This directory stores reproducible intermediate objects and results generated
by the canonical workflowr analyses.

Files listed below constitute the current simulated-data output contract.
Legacy development results are not part of the canonical analysis.

## Data audit and preprocessing

- `preprocessed_simulated_common.rds`
- `simulated_audit_summary.csv`
- `simulated_ld_summary.csv`
- `simulated_qtl_map.csv`
- `simulated_scenario_summary.csv`

These files document the validated simulated dataset and the canonical
preprocessed object consumed by downstream analyses.

## Frozen cross-validation design

- `simulated_cv_design.rds`
- `simulated_cv_design_audit.csv`
- `simulated_cv_design_summary.csv`
- `simulated_cv_inner_assignments.csv`
- `simulated_cv_outer_assignments.csv`

The same frozen outer partitions are used by GBLUP-ADE and all ANN variants.

## Canonical GBLUP-ADE

- `simulated_gblup_ade_kernel_summary.csv`
- `simulated_gblup_ade_predictions.csv`
- `simulated_gblup_ade_predictions.rds`
- `simulated_gblup_ade_results.csv`
- `simulated_gblup_ade_results.rds`
- `simulated_gblup_ade_run_metadata.rds`

## Canonical ANN tuning

- `simulated_ann_tuning_manifest.csv`
- `simulated_ann_tuning_manifest.rds`
- `simulated_ann_tuning_fold_results.csv`
- `simulated_ann_tuning_fold_results.rds`
- `simulated_ann_tuning_candidate_summary.csv`
- `simulated_ann_tuning_candidate_summary.rds`
- `simulated_ann_tuning_selected_configurations.csv`
- `simulated_ann_tuning_selected_configurations.rds`
- `simulated_ann_tuning_run_metadata.rds`

The canonical tuning stage uses only outer-analysis data. Outer-assessment
individuals and true simulated genetic values are excluded from candidate
selection.

## Canonical final ANN

- `simulated_ann_epoch_selection.csv`
- `simulated_ann_epoch_selection.rds`
- `simulated_ann_predictions.csv`
- `simulated_ann_predictions.rds`
- `simulated_ann_results.csv`
- `simulated_ann_results.rds`
- `simulated_ann_run_metadata.rds`

The final ANN protocol selects `Best_epoch` inside the outer-analysis sample,
reinitializes the network, refits on the full outer-analysis sample for exactly
that number of epochs, and only then predicts the untouched outer-assessment
sample.

## Canonical model comparison

Files under `comparison/`:

- `simulated_model_overall_summary.csv`
- `simulated_model_scenario_summary.csv`
- `simulated_ann_vs_gblup_paired_summary.csv`
- `simulated_ann_vs_gblup_paired_by_scenario.csv`

The paired comparison uses identical `TaskID`, `SplitID`, and outer-assessment
individuals for GBLUP-ADE and all ANN variants.

## Repository policy

Large temporary model-fitting artifacts, development diagnostics, pilot outputs,
old tuning summaries, sensitivity analyses, convergence diagnostics, and
operational checkpoints are not part of the canonical output contract and
should not be committed unless explicitly required for reproducibility.

Routine website rendering should use the saved canonical outputs above rather
than automatically repeating computationally expensive ANN fitting.
