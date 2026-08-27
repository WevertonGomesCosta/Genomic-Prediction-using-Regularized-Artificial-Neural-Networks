find_project_root <- function(start = getwd()) {
  path <- normalizePath(start, winslash = "/", mustWork = TRUE)

  repeat {
    if (file.exists(file.path(path, "_workflowr.yml"))) {
      return(path)
    }

    parent <- dirname(path)

    if (identical(parent, path)) {
      stop("Could not locate workflowr project root.")
    }

    path <- parent
  }
}

PROJECT_ROOT <- find_project_root()

project_path <- function(...) {
  file.path(PROJECT_ROOT, ...)
}

gr <- readRDS(project_path("output", "simulated", "gblup", "simulated_gblup_ade_results.rds"))
ar <- readRDS(project_path("output", "simulated", "ann", "final", "simulated_ann_results.rds"))

metrics <- c(
  "Genetic_Correlation",
  "Genetic_RMSE",
  "Genetic_MAE",
  "Genetic_Bias",
  "Genetic_Slope",
  "Genetic_R2",
  "Phenotype_Correlation",
  "Phenotype_RMSE",
  "Phenotype_MAE",
  "Phenotype_Bias",
  "Phenotype_Slope",
  "Phenotype_R2"
)

higher_better <- c(
  "Genetic_Correlation",
  "Genetic_R2",
  "Phenotype_Correlation",
  "Phenotype_R2"
)

lower_better <- c(
  "Genetic_RMSE",
  "Genetic_MAE",
  "Phenotype_RMSE",
  "Phenotype_MAE"
)

zero_target <- c("Genetic_Bias", "Phenotype_Bias")
one_target <- c("Genetic_Slope", "Phenotype_Slope")

required_cols <- c(
  "Scenario", "Repetition", "Fold", "TaskID", "Model", metrics
)

missing_gr <- setdiff(required_cols, names(gr))
missing_ar <- setdiff(required_cols, names(ar))

if (length(missing_gr)) {
  stop("Missing GBLUP columns: ", paste(missing_gr, collapse = ", "))
}
if (length(missing_ar)) {
  stop("Missing ANN columns: ", paste(missing_ar, collapse = ", "))
}

all_results <- rbind(
  gr[, required_cols],
  ar[, required_cols]
)

overall <- aggregate(
  all_results[, metrics],
  by = list(Model = all_results$Model),
  FUN = mean
)

scenario_summary <- aggregate(
  all_results[, metrics],
  by = list(
    Scenario = all_results$Scenario,
    Model = all_results$Model
  ),
  FUN = mean
)

performance_advantage <- function(metric, ann_value, gblup_value) {
  if (metric %in% higher_better) {
    return(ann_value - gblup_value)
  }
  if (metric %in% lower_better) {
    return(gblup_value - ann_value)
  }
  if (metric %in% zero_target) {
    return(abs(gblup_value) - abs(ann_value))
  }
  if (metric %in% one_target) {
    return(abs(gblup_value - 1) - abs(ann_value - 1))
  }
  stop("Unclassified metric: ", metric)
}

g <- gr[, c("TaskID", metrics)]
names(g)[-1] <- paste0(names(g)[-1], "_GBLUP")

paired <- list()

for (model in sort(unique(ar$Model))) {
  a <- ar[
    ar$Model == model,
    c("TaskID", "Scenario", metrics)
  ]

  z <- merge(a, g, by = "TaskID", all = FALSE)

  if (nrow(z) != 150L) {
    stop(model, ": expected 150 paired tasks, got ", nrow(z))
  }

  for (metric in metrics) {
    ann_value <- z[[metric]]
    gblup_value <- z[[paste0(metric, "_GBLUP")]]

    raw_difference <- ann_value - gblup_value
    advantage <- performance_advantage(
      metric, ann_value, gblup_value
    )

    paired[[length(paired) + 1L]] <- data.frame(
      Model = model,
      Metric = metric,
      N = length(raw_difference),
      Mean_ANN = mean(ann_value),
      Mean_GBLUP = mean(gblup_value),
      Mean_raw_difference = mean(raw_difference),
      Median_raw_difference = median(raw_difference),
      Mean_performance_advantage = mean(advantage),
      Median_performance_advantage = median(advantage),
      ANN_better = sum(advantage > 0),
      Equal = sum(advantage == 0),
      GBLUP_better = sum(advantage < 0),
      stringsAsFactors = FALSE
    )
  }
}

paired <- do.call(rbind, paired)
rownames(paired) <- NULL

paired_scenario <- list()

for (model in sort(unique(ar$Model))) {
  a <- ar[
    ar$Model == model,
    c("TaskID", "Scenario", metrics)
  ]

  z <- merge(a, g, by = "TaskID", all = FALSE)

  for (scenario in sort(unique(z$Scenario))) {
    zs <- z[z$Scenario == scenario, , drop = FALSE]

    if (nrow(zs) != 25L) {
      stop(
        model, " / ", scenario,
        ": expected 25 paired tasks, got ", nrow(zs)
      )
    }

    for (metric in metrics) {
      ann_value <- zs[[metric]]
      gblup_value <- zs[[paste0(metric, "_GBLUP")]]

      advantage <- performance_advantage(
        metric, ann_value, gblup_value
      )

      paired_scenario[[length(paired_scenario) + 1L]] <- data.frame(
        Scenario = scenario,
        Model = model,
        Metric = metric,
        N = nrow(zs),
        Mean_advantage = mean(advantage),
        Median_advantage = median(advantage),
        ANN_better = sum(advantage > 0),
        Equal = sum(advantage == 0),
        GBLUP_better = sum(advantage < 0),
        stringsAsFactors = FALSE
      )
    }
  }
}

paired_scenario <- do.call(rbind, paired_scenario)
rownames(paired_scenario) <- NULL

checks <- data.frame(
  Check = c(
    "5 models overall",
    "30 scenario-model rows",
    "48 paired model-metric rows",
    "288 paired scenario-model-metric rows",
    "150 paired tasks per ANN model/metric",
    "25 paired tasks per scenario/model/metric",
    "all paired summary values finite",
    "all scenario summary values finite"
  ),
  PASS = c(
    nrow(overall) == 5L,
    nrow(scenario_summary) == 30L,
    nrow(paired) == 48L,
    nrow(paired_scenario) == 288L,
    all(paired$N == 150L),
    all(paired_scenario$N == 25L),
    all(vapply(
      paired[, vapply(paired, is.numeric, logical(1)), drop = FALSE],
      function(x) all(is.finite(x)),
      logical(1)
    )),
    all(vapply(
      scenario_summary[, metrics, drop = FALSE],
      function(x) all(is.finite(x)),
      logical(1)
    ))
  ),
  stringsAsFactors = FALSE
)

checks$Status <- ifelse(checks$PASS, "PASS", "BLOCKED")

cat("\n============================================================\n")
cat(" OVERALL MODEL PERFORMANCE\n")
cat("============================================================\n")
print(overall)

cat("\n============================================================\n")
cat(" PAIRED ANN VS GBLUP SUMMARY\n")
cat(" Positive performance advantage = ANN better\n")
cat("============================================================\n")
print(paired)

cat("\n============================================================\n")
cat(" PAIRED BY SCENARIO\n")
cat("============================================================\n")
print(paired_scenario)

cat("\n============================================================\n")
cat(" INTEGRITY CHECKS\n")
cat("============================================================\n")
print(checks[, c("Check", "Status")], row.names = FALSE)

cat("\nTOTAL:", sum(checks$PASS), "/", nrow(checks), "PASS\n")

if (any(!checks$PASS)) {
  stop("Canonical comparison integrity checks failed.")
}

dir.create(
  project_path("output", "simulated", "comparison"),
  recursive = TRUE,
  showWarnings = FALSE
)

write.csv(
  overall,
  project_path("output", "simulated", "comparison", "simulated_model_overall_summary.csv"),
  row.names = FALSE
)

write.csv(
  scenario_summary,
  project_path("output", "simulated", "comparison", "simulated_model_scenario_summary.csv"),
  row.names = FALSE
)

write.csv(
  paired,
  project_path("output", "simulated", "comparison", "simulated_ann_vs_gblup_paired_summary.csv"),
  row.names = FALSE
)

write.csv(
  paired_scenario,
  project_path("output", "simulated", "comparison", "simulated_ann_vs_gblup_paired_by_scenario.csv"),
  row.names = FALSE
)

cat("\nSaved 4 canonical comparison files:\n")
cat("  output/simulated/comparison/simulated_model_overall_summary.csv\n")
cat("  output/simulated/comparison/simulated_model_scenario_summary.csv\n")
cat("  output/simulated/comparison/simulated_ann_vs_gblup_paired_summary.csv\n")
cat("  output/simulated/comparison/simulated_ann_vs_gblup_paired_by_scenario.csv\n")
