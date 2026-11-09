# R07 — Real-data regularized ANN audit

Date: 2026-11-06
Branch context: `real-data-workflow`
Module: `analysis/real_data_ann.Rmd`

## Scope

This record freezes the computational, provenance, and scientific audit of the
real-data regularized ANN workflow before the terminal GBLUP-ADE versus ANN
comparison. No hyperparameter grid, validation split, model architecture, or
held-out result was changed after inspection of outer-assessment performance.

## Computational integrity

| Check | Status | Observed |
|---|---|---|
| Tuning task checkpoints | PASS | 75 / 75 |
| Final-fit task checkpoints | PASS | 75 / 75 |
| Selected configurations | PASS | 300 / 300 |
| Candidate summaries | PASS | 5,250 / 5,250 |
| Inner candidate-fold fits | PASS | 21,000 / 21,000 |
| Unique tuning tasks | PASS | 75 / 75 |
| Final model-task results | PASS | 300 / 300 |
| Held-out predictions | PASS | 11,700 / 11,700 |
| Epoch-selection rows | PASS | 300 / 300 |
| Unique final tasks | PASS | 75 / 75 |
| Successful final results | PASS | 300 `ok` |
| Finite held-out predictions | PASS | 11,700 / 11,700 |
| Model balance | PASS | 75 results for each ANN variant |
| Trait balance | PASS | 100 results for each trait |

The 75 outer tasks are the frozen `3 traits × 5 repetitions × 5 folds`. Each
task evaluates 70 tuning candidates over 4 inner folds, giving 21,000 inner
training fits in total. Each final model predicts the same 39 held-out
individuals, giving `75 × 4 × 39 = 11,700` ANN prediction rows.

## Provenance and canonical reconstruction

The canonical final result file is:

`output/real/ann/final/real_ann_results.rds`

MD5:

`8f1aee04001d43829d0f0d810b0dbdd3`

All 75 final checkpoints belong to one coherent execution contract:

- `dataset = real`
- `analysis = real_ann_final_task`
- `device = cuda`
- `torch_version = 0.16.3`
- one unique `config_id`
- one unique `tuning_config_id`
- `task_index` exactly covers `1:75`

The canonical objects were reconstructed directly from the 75 checkpoint RDS
files and compared after deterministic sorting.

| Object | Rebuilt rows | Canonical rows | Maximum numeric difference | Non-numeric columns | `all.equal` |
|---|---:|---:|---:|---|---|
| Results | 300 | 300 | 0 | identical | TRUE |
| Predictions | 11,700 | 11,700 | 0 | identical | TRUE |
| Epoch selection | 300 | 300 | 0 | identical | TRUE |

The current R07 state is therefore exactly reproducible from its final
checkpoints. A small discrepancy observed during an earlier interactive audit
belongs to a prior non-preserved snapshot and is not present in the canonical
checkpoint-derived state documented here.

## Parallel execution note

The completed run used internal `future::multisession` parallelism with
Torch/CUDA. The machine exposed one NVIDIA GeForce RTX 4060 Laptop GPU and 22
logical CPU cores. An initial 22-worker CUDA run saturated approximately 97% of
VRAM and produced poor throughput. The completed final run used two CUDA
workers, preserving task-level checkpoints. This is an operational decision
only; it does not alter the scientific model, folds, seeds, hyperparameter grid,
or held-out evaluation contract.

## Tuning behavior

Architecture and learning rate are selected with `ANN_0` and shared across the
four ANN variants within each outer task, by design.

Selected learning rates across 75 tasks:

- `0.000125`: 54 tasks (72.0%)
- `0.00025`: 10 tasks
- `0.0005`: 7 tasks
- `0.001`: 4 tasks

Regularization frequently reached the upper boundary of the prespecified grid:

- `ANN_L1`: `L1 = 0.1` in 49/75 tasks (65.3%)
- `ANN_L1_L2`: `L1 = 0.1` in 47/75 tasks (62.7%)
- `ANN_L2`: `L2 = 0.01` in 32/75 tasks (42.7%)
- `ANN_L1_L2`: `L2 = 0.01` in 30/75 tasks (40.0%)

This boundary behavior is recorded as a scientific warning. The grid is not
expanded post hoc after inspection of held-out performance.

Median epoch behavior:

| Model | Median best epoch | Median last epoch |
|---|---:|---:|
| ANN_0 | 2 | 27 |
| ANN_L1 | 27 | 52 |
| ANN_L1_L2 | 26 | 51 |
| ANN_L2 | 2 | 27 |

The `ANN_0` and `ANN_L2` pattern is consistent with very early best validation
performance followed by the fixed patience window.

## Canonical held-out performance

Mean performance across the 25 outer splits for each trait:

| Trait | Model | Correlation | RMSE | MAE | Bias | R2 |
|---|---|---:|---:|---:|---:|---:|
| BM | ANN_0 | -0.0929 | 0.5398 | 0.4425 | 0.0341 | -0.1204 |
| BM | ANN_L1 | -0.0405 | 0.5257 | 0.4257 | 0.0116 | -0.0631 |
| BM | ANN_L1_L2 | -0.0685 | 0.5272 | 0.4278 | 0.0252 | -0.0681 |
| BM | ANN_L2 | -0.0957 | 0.5406 | 0.4438 | 0.0369 | -0.1244 |
| Cer | ANN_0 | -0.0382 | 0.6011 | 0.4890 | 0.0301 | -0.1529 |
| Cer | ANN_L1 | -0.0157 | 0.5814 | 0.4774 | 0.0312 | -0.0692 |
| Cer | ANN_L1_L2 | -0.0185 | 0.5819 | 0.4766 | 0.0246 | -0.0710 |
| Cer | ANN_L2 | -0.0482 | 0.6019 | 0.4896 | 0.0315 | -0.1543 |
| Prod.Cor | ANN_0 | 0.0099 | 3.1289 | 2.4318 | 0.0126 | -0.1276 |
| Prod.Cor | ANN_L1 | -0.0248 | 3.0620 | 2.3903 | 0.0775 | -0.0789 |
| Prod.Cor | ANN_L1_L2 | -0.0262 | 3.0662 | 2.3938 | 0.0982 | -0.0831 |
| Prod.Cor | ANN_L2 | 0.0117 | 3.1258 | 2.4349 | 0.0486 | -0.1268 |

All four ANN variants show held-out Pearson correlations close to zero or
negative. L1-based regularization reduces RMSE and MAE relative to ANN_0, but
does not produce useful held-out ranking.

## Prediction-dispersion diagnosis

Median within-fold `SD(prediction) / SD(observed)`:

| Trait | ANN_0 | ANN_L1 | ANN_L1_L2 | ANN_L2 |
|---|---:|---:|---:|---:|
| BM | 0.139 | 0.059 | 0.059 | 0.137 |
| Cer | 0.152 | 0.029 | 0.047 | 0.196 |
| Prod.Cor | 0.191 | 0.052 | 0.052 | 0.191 |

Number of outer folds with `SD(prediction) / SD(observed) < 0.10`:

| Trait | ANN_0 | ANN_L1 | ANN_L1_L2 | ANN_L2 |
|---|---:|---:|---:|---:|
| BM | 8/25 | 23/25 | 23/25 | 8/25 |
| Cer | 6/25 | 23/25 | 21/25 | 5/25 |
| Prod.Cor | 5/25 | 19/25 | 19/25 | 5/25 |

Median within-fold correlations remain approximately zero or negative for every
variant. The regularized networks, especially those containing L1, therefore
show strong regression toward the fold mean. In some folds the prediction
variance is effectively zero, explaining unstable calibration slopes.

## Frozen interpretation

**Methodological/computational status: PASS.**
**Provenance/reconstruction status: PASS.**
**Scientific predictive signal: WARN / not useful under this design.**

The nested validation design, task completeness, finite predictions, checkpoint
structure, and checkpoint-to-canonical reconstruction are intact. No evident
leakage was detected. The ANN branch does not demonstrate a predictive advantage
in the real data under the prespecified search space. L1 regularization reduces
squared/absolute error mainly through stronger shrinkage toward the mean rather
than improved individual discrimination.

The terminal R08 comparison must use exactly these frozen checkpoint-derived
ANN outputs together with the frozen GBLUP-ADE outputs. No model refitting or
post-hoc hyperparameter modification is permitted.
