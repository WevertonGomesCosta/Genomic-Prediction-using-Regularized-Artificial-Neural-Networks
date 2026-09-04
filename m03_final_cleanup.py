from pathlib import Path

path = Path("analysis/simulated_data_gblup.Rmd")
text = path.read_text(encoding="utf-8")


def replace_once(old, new):
    global text
    if old not in text:
        raise SystemExit(f"Expected text not found:\n{old}")
    text = text.replace(old, new, 1)


replace_once(
    "- **True genetic value is an evaluation target:** it is accessed only after the\n  held-out predictions have been generated.",
    "- **True genetic value is an evaluation target:** it does not participate in\n  partition generation, kernel construction, model fitting, or prediction; it is\n  subset only in the held-out evaluation block."
)

replace_once(
    "The crucial separation is by information type, not by availability of genotype.\nThe 200 outer-assessment individuals retain their marker profiles but their\nphenotypes are hidden before model fitting, and their true genetic values are\nnot read for evaluation until predictions already exist.",
    "The crucial separation is by information type, not by availability of genotype.\nThe 200 outer-assessment individuals retain their marker profiles, but their\nphenotypes are hidden before model fitting. True genetic values never enter\npartition generation, kernel construction, fitting, or prediction and are\nsubset only after held-out predictions have been produced."
)

replace_once(
    '    "sommer::E.mat()"',
    '    "sommer::E.mat(type = \\"A#A\\")"'
)
replace_once(
    '    "Epistatic genomic covariance used by this benchmark."',
    '    "Second-order additive x additive genomic covariance."'
)

replace_once(
    "These matrices describe genomic covariance among individuals. They do not use\nphenotype or true genetic value, and they are built once and reused across all\n150 fits.",
    "These matrices describe genomic covariance among individuals. They do not use\nphenotype or true genetic value, and they are built once and reused across all\n150 fits. In this benchmark, the epistatic matrix is the second-order additive x\nadditive kernel (`type = \"A#A\"`), matching the interaction component represented\nby E rather than an unspecified generic epistasis kernel."
)

replace_once(
    "Thus the output preserves both the total prediction and the additive,\ndominance, epistatic, and summed genomic components for every held-out\nindividual.",
    "Thus the output preserves both the total prediction and the additive,\ndominance, epistatic, and summed genomic components for every held-out\nindividual. The historical output field `GEBV` is retained for compatibility;\nin this ADE model it stores the summed additive, dominance, and epistatic\nprediction and is interpreted here as the **total predicted genetic component**,\nnot as a breeding value in the strict additive-only sense."
)

old_metrics = '''```{r gblup-metrics}
safe_cor <- function(pred, obs) {
  cor(pred, obs)
}

safe_rmse <- function(pred, obs) {
  sqrt(
    mean(
      (pred - obs)^2
    )
  )
}

safe_mae <- function(pred, obs) {
  mean(
    abs(
      pred - obs
    )
  )
}

safe_bias <- function(pred, obs) {
  mean(
    pred - obs
  )
}

safe_slope <- function(pred, obs) {
  as.numeric(
    coef(
      lm(
        obs ~ pred
      )
    )[2]
  )
}

safe_r2 <- function(pred, obs) {
  total_variation <- sum(
    (
      obs -
      mean(obs)
    )^2
  )

  1 -
    sum(
      (
        obs -
        pred
      )^2
    ) /
    total_variation
}

metrics <- function(
  pred,
  obs,
  prefix
) {
  values <- c(
    safe_cor(pred, obs),
    safe_rmse(pred, obs),
    safe_mae(pred, obs),
    safe_bias(pred, obs),
    safe_slope(pred, obs),
    safe_r2(pred, obs)
  )

  names(values) <- paste0(
    prefix,
    c(
      "_Correlation",
      "_RMSE",
      "_MAE",
      "_Bias",
      "_Slope",
      "_R2"
    )
  )

  values
}
```
'''
replace_once(old_metrics, "")

replace_once(
    "For each target, the stored metrics are correlation, RMSE, MAE, bias,\ncalibration slope, and \\(R^2\\). Bias is defined as\n`mean(predicted - observed)`, so positive values indicate overprediction. The\ncalibration slope is estimated from `observed ~ predicted`, and\n\\(R^2=1-SSE/SST\\).",
    "For each target, the stored metrics are **Pearson correlation**, RMSE, MAE,\nbias, calibration slope, and \\(R^2\\). Bias is defined as\n`mean(predicted - observed)`, so positive values indicate overprediction. The\ncalibration slope is estimated from `observed ~ predicted`, and\n\\(R^2=1-SSE/SST\\). These formulas are calculated directly in the fitting loop\ninstead of being hidden behind local metric wrappers."
)

old_extract = '''### 7.1 Recovering the genomic components

`sommer::mmes()` stores the random-effect estimates in `fit$uList`. The helper
below maps a fitted effect back to the 1,000 individual positions through its
incidence matrix.

```{r extract-genomic-component}
extract_u <- function(
  fit,
  dat,
  factor_name,
  effect_name
) {
  random_effect <- as.matrix(
    fit$uList[[effect_name]]
  )

  incidence_matrix <- model.matrix(
    as.formula(
      paste0(
        "~",
        factor_name,
        " - 1"
      )
    ),
    data = dat
  )

  as.numeric(
    incidence_matrix %*%
      random_effect[
        ,
        1L,
        drop = FALSE
      ]
  )
}
```

The fitting loop calls this function for `id/A`, `idd/D`, and `ide/E` to recover
additive, dominance, and epistatic predictions, respectively.

### 7.2 One model call
'''
new_extract = '''### 7.1 One model call

`sommer::mmes()` stores the fitted random effects in `fit$uList`. In the complete
workflow below, each additive, dominance, and epistatic effect is mapped back to
the 1,000 individual positions explicitly with its incidence matrix; no local
helper function hides that transformation.

'''
replace_once(old_extract, new_extract)
replace_once("### 7.3 Complete 150-task workflow", "### 7.2 Complete 150-task workflow")

replace_once(
    "A_matrix <- sommer::A.mat(geno)\nD_matrix <- sommer::D.mat(geno)\nE_matrix <- sommer::E.mat(geno)",
    "A_matrix <- sommer::A.mat(geno)\nD_matrix <- sommer::D.mat(geno)\nE_matrix <- sommer::E.mat(\n  geno,\n  nishio = TRUE,\n  type = \"A#A\",\n  min.MAF = 0.02\n)"
)

replace_once(
    "  phenotype_vector <- phenotype[\n    ,\n    scenario_index\n  ]\n  true_genetic_vector <- true_g[\n    ,\n    scenario_index\n  ]\n",
    "  phenotype_vector <- phenotype[\n    ,\n    scenario_index\n  ]\n"
)

old_effects = '''  # Recover additive, dominance, and epistatic effects for all individuals.
  additive <- extract_u(
    fit,
    dat,
    "id",
    "vsm(ism(id), Gu = A_matrix)"
  )
  dominance <- extract_u(
    fit,
    dat,
    "idd",
    "vsm(ism(idd), Gu = D_matrix)"
  )
  epistatic <- extract_u(
    fit,
    dat,
    "ide",
    "vsm(ism(ide), Gu = E_matrix)"
  )

  gebv <-
    additive +
    dominance +
    epistatic

  intercept <- as.numeric(fit$b)[1L]
  predicted_value <- intercept + gebv
'''
new_effects = '''  # Recover the additive effect for all individuals.
  additive_effect <- as.matrix(
    fit$uList[["vsm(ism(id), Gu = A_matrix)"]]
  )
  additive_incidence <- model.matrix(
    ~ id - 1,
    data = dat
  )
  additive <- as.numeric(
    additive_incidence %*%
      additive_effect[, 1L, drop = FALSE]
  )

  # Recover the dominance effect for all individuals.
  dominance_effect <- as.matrix(
    fit$uList[["vsm(ism(idd), Gu = D_matrix)"]]
  )
  dominance_incidence <- model.matrix(
    ~ idd - 1,
    data = dat
  )
  dominance <- as.numeric(
    dominance_incidence %*%
      dominance_effect[, 1L, drop = FALSE]
  )

  # Recover the additive x additive epistatic effect for all individuals.
  epistatic_effect <- as.matrix(
    fit$uList[["vsm(ism(ide), Gu = E_matrix)"]]
  )
  epistatic_incidence <- model.matrix(
    ~ ide - 1,
    data = dat
  )
  epistatic <- as.numeric(
    epistatic_incidence %*%
      epistatic_effect[, 1L, drop = FALSE]
  )

  genetic_component <-
    additive +
    dominance +
    epistatic

  intercept <- as.numeric(fit$b)[1L]
  predicted_value <- intercept + genetic_component
'''
replace_once(old_effects, new_effects)

old_eval = '''  # Evaluate only the 200 held-out individuals.
  observed_test <- phenotype_vector[
    assessment_index
  ]
  true_g_test <- true_genetic_vector[
    assessment_index
  ]
  predicted_test <- predicted_value[
    assessment_index
  ]
  gebv_test <- gebv[
    assessment_index
  ]

  genetic_metrics <- metrics(
    predicted_test,
    true_g_test,
    "Genetic"
  )
  phenotype_metrics <- metrics(
    predicted_test,
    observed_test,
    "Phenotype"
  )
'''
new_eval = '''  # Evaluate only after held-out predictions have been generated.
  observed_test <- phenotype_vector[
    assessment_index
  ]
  true_g_test <- true_g[
    assessment_index,
    scenario_index
  ]
  predicted_test <- predicted_value[
    assessment_index
  ]
  genetic_component_test <- genetic_component[
    assessment_index
  ]

  # Primary evaluation against the known simulated genetic value.
  genetic_correlation <- cor(
    predicted_test,
    true_g_test
  )
  genetic_rmse <- sqrt(
    mean((predicted_test - true_g_test)^2)
  )
  genetic_mae <- mean(
    abs(predicted_test - true_g_test)
  )
  genetic_bias <- mean(
    predicted_test - true_g_test
  )
  genetic_slope <- as.numeric(
    coef(lm(true_g_test ~ predicted_test))[2]
  )
  genetic_r2 <- 1 -
    sum((true_g_test - predicted_test)^2) /
    sum((true_g_test - mean(true_g_test))^2)

  # Secondary evaluation against the observed phenotype.
  phenotype_correlation <- cor(
    predicted_test,
    observed_test
  )
  phenotype_rmse <- sqrt(
    mean((predicted_test - observed_test)^2)
  )
  phenotype_mae <- mean(
    abs(predicted_test - observed_test)
  )
  phenotype_bias <- mean(
    predicted_test - observed_test
  )
  phenotype_slope <- as.numeric(
    coef(lm(observed_test ~ predicted_test))[2]
  )
  phenotype_r2 <- 1 -
    sum((observed_test - predicted_test)^2) /
    sum((observed_test - mean(observed_test))^2)
'''
replace_once(old_eval, new_eval)

for old, new in {
    '      genetic_metrics["Genetic_Correlation"]': '      genetic_correlation',
    '      genetic_metrics["Genetic_RMSE"]': '      genetic_rmse',
    '      genetic_metrics["Genetic_MAE"]': '      genetic_mae',
    '      genetic_metrics["Genetic_Bias"]': '      genetic_bias',
    '      genetic_metrics["Genetic_Slope"]': '      genetic_slope',
    '      genetic_metrics["Genetic_R2"]': '      genetic_r2',
    '      safe_cor(gebv_test, true_g_test)': '      cor(genetic_component_test, true_g_test)',
    '      phenotype_metrics["Phenotype_Correlation"]': '      phenotype_correlation',
    '      phenotype_metrics["Phenotype_RMSE"]': '      phenotype_rmse',
    '      phenotype_metrics["Phenotype_MAE"]': '      phenotype_mae',
    '      phenotype_metrics["Phenotype_Bias"]': '      phenotype_bias',
    '      phenotype_metrics["Phenotype_Slope"]': '      phenotype_slope',
    '      phenotype_metrics["Phenotype_R2"]': '      phenotype_r2',
    '    GEBV = gebv_test,': '    GEBV = genetic_component_test,',
}.items():
    replace_once(old, new)

replace_once(
    "The stored benchmark contains one task-level result row for each of the 150\nscenario-by-split fits and 200 held-out predictions per task.",
    "The stored benchmark contains one task-level result row for each of the 150\nscenario-by-split fits and 200 held-out predictions per task. The historical\n`Status = \"ok\"` field indicates that a fit returned and produced stored\npredictions; it is not interpreted here as independent evidence that numerical\nconvergence was formally diagnosed for all 150 fits."
)

replace_once(
    "  geom_jitter(\n    width = 0.10,\n    height = 0,\n    alpha = 0.45,\n    size = 1.8\n  ) +",
    "  geom_point(\n    position = position_jitter(\n      width = 0.10,\n      height = 0,\n      seed = SEED_GLOBAL + 301L\n    ),\n    alpha = 0.45,\n    size = 1.8\n  ) +"
)
replace_once(
    "  geom_jitter(\n    width = 0.10,\n    height = 0,\n    alpha = 0.45,\n    size = 1.8\n  ) +",
    "  geom_point(\n    position = position_jitter(\n      width = 0.10,\n      height = 0,\n      seed = SEED_GLOBAL + 302L\n    ),\n    alpha = 0.45,\n    size = 1.8\n  ) +"
)

replace_once(
    "- **correlation:** larger values indicate stronger agreement in ranking and\n  linear association with the known genetic signal;",
    "- **Pearson correlation:** larger values indicate stronger linear association\n  with the known genetic signal;"
)

replace_once(
    "The spread within each scenario records sensitivity to the outer assessment\nsample rather than a new source of model tuning.",
    "The spread within each scenario records sensitivity to the outer assessment\nsample rather than a new source of model tuning. These split-level distributions\nare descriptive summaries of held-out-sample sensitivity; the 25 values are not\ntreated as statistically independent replicates or as inferential uncertainty."
)

replace_once(
    "Reporting the mean, standard deviation, minimum, and maximum correlation prevents\none favorable or unfavorable split from determining the interpretation of a\nscenario.",
    "Reporting the mean, standard deviation, minimum, and maximum correlation prevents\none favorable or unfavorable split from determining the interpretation of a\nscenario. These quantities remain descriptive because repeated cross-validation\nreuses individuals across outer analysis and assessment sets."
)

replace_once(
    "Because A, D, and E are built once and reused, their construction time should\nnot be interpreted as a cost incurred separately for every outer split.",
    "Because A, D, and E are built once and reused, their construction time should\nnot be interpreted as a cost incurred separately for every outer split. The\nreported times describe the completed run recorded in the saved outputs and\nshould not be interpreted as hardware-independent constants of GBLUP-ADE."
)

if "<- function" in text:
    raise SystemExit("Named local helper function remains in M03")

path.write_text(text, encoding="utf-8")
