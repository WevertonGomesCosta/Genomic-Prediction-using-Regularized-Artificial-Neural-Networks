from pathlib import Path

path = Path("analysis/simulated_data_audit.Rmd")
text = path.read_text(encoding="utf-8")


def replace_once(old, new, label):
    global text
    if text.count(old) != 1:
        raise SystemExit(f"Expected one {label} anchor; found {text.count(old)}")
    text = text.replace(old, new, 1)


# Remove the paragraph left over from the former combined-QTL subsection.
replace_once(
    """The number of simulated QTL increases from 8 in C1 to 480 in C6, while the
specified heritability changes from 0.7 in C1-C2 to 0.5 in C3-C4 and 0.3 in
C5-C6. The remaining settings shown in the table are constant across scenarios.
The scenarios therefore become genetically more polygenic as the number of QTL
increases, while the specified heritability decreases across the same sequence.

""",
    "",
    "redundant scenario paragraph",
)

# Replace terse post-chunk statements with compact, descriptive reading points.
replace_once(
    """The file contains `r nrow(phenotype)` individuals and
`r ncol(phenotype)` scenarios. These are the responses that become available to
the model only when an individual belongs to the corresponding analysis set in
the validation design.
""",
    """The phenotype object now establishes two facts used later:

- **Dimensions:** `r nrow(phenotype)` individuals are represented in each of
  `r ncol(phenotype)` scenarios.
- **Use in prediction:** phenotype is the response available to a model only for
  individuals belonging to the corresponding analysis set defined by the
  validation design.
""",
    "phenotype interpretation",
)

replace_once(
    """The matrix contains the same `r nrow(true_genetic_value)` individuals and six
scenarios as the phenotype matrix, preserving row-by-row correspondence between
the observed response and the known simulated genetic component.
""",
    """This second response-related object has three properties to retain:

- **Same dimensions:** `r nrow(true_genetic_value)` individuals x six scenarios.
- **Same row order:** every row remains paired with the corresponding phenotype
  row.
- **Different analytical role:** the values are reserved for held-out evaluation
  rather than model fitting.
""",
    "true genetic value interpretation",
)

replace_once(
    """The complete matrix contains `r nrow(geno_012)` individuals and
`r ncol(geno_012)` markers. The observed states are
`r paste(sort(unique(as.vector(geno_012))), collapse = ", ")`, which correspond
to the three genotype classes generated for the F2 population.
""",
    """The displayed sample makes the structure of the complete genotype object
explicit:

- **Dimensions:** `r nrow(geno_012)` individuals x `r ncol(geno_012)` markers.
- **Observed states:** `r paste(sort(unique(as.vector(geno_012))), collapse = ", ")`.
- **Interpretation:** these three discrete states are the genotype classes
  generated for the simulated F2 population.
""",
    "genotype interpretation",
)

replace_once(
    """Thus, `0 -> -1`, `1 -> 0`, and `2 -> 1`. The transformation changes the
numerical scale only.
""",
    """After recoding, the prediction matrix preserves the data structure:

- the same 1,000 individuals remain in the same row order;
- the same 4,010 markers remain in the same column order;
- only the numerical coding changes from `0/1/2` to `-1/0/1`.
""",
    "genotype coding conclusion",
)

replace_once(
    """The map now establishes the marker framework by itself. QTL are introduced only
once, in Section 6, where their distribution is compared across the six
simulation scenarios.
""",
    """The separation between Sections 5 and 6 is intentional:

- **Section 5** establishes only the marker framework and linkage-group
  structure;
- **Section 6** adds QTL once, using the scenario-specific figure to compare
  their positions and density across C1-C6.

This avoids presenting the same QTL information in both a combined map and a
scenario map.
""",
    "map-QTL separation",
)

replace_once(
    """The phenotype-true-genetic-value correlation ranges from
`r sprintf("%.3f", min(scenario_summary$Cor_P_G))` to
`r sprintf("%.3f", max(scenario_summary$Cor_P_G))`. This variation shows that
the six scenarios do not contain the same amount of recoverable genetic signal,
which is important context for the model comparisons made later.
""",
    """Two points from this table are especially important for later prediction:

- **Genetic signal differs among scenarios:** phenotype-true-genetic-value
  correlation ranges from
  `r sprintf("%.3f", min(scenario_summary$Cor_P_G))` to
  `r sprintf("%.3f", max(scenario_summary$Cor_P_G))`.
- **Comparison context:** model performance should therefore be interpreted
  alongside scenario difficulty rather than assuming that C1-C6 contain the
  same amount of recoverable genetic signal.
""",
    "signal interpretation",
)

replace_once(
    """The absolute differences for C1-C6 are
`r paste(sprintf("%.4f", abs(h2_difference)), collapse = ", ")`. The largest
difference occurs in
`r scenario_summary$Scenario[which.max(abs(h2_difference))]`, with an absolute
difference of `r sprintf("%.4f", max(abs(h2_difference)))`.
""",
    """The comparison can be read directly from two quantities:

- **Absolute differences for C1-C6:**
  `r paste(sprintf("%.4f", abs(h2_difference)), collapse = ", ")`.
- **Largest difference:**
  `r scenario_summary$Scenario[which.max(abs(h2_difference))]`, with
  `r sprintf("%.4f", max(abs(h2_difference)))`.

These are realized properties of the generated population and do not change the
heritability values specified when the scenarios were simulated.
""",
    "heritability interpretation",
)

replace_once(
    """The empirical phenotype CV values are
`r paste(sprintf("%.2f", scenario_summary$CV_empirical_pct), collapse = ", ")`%.
Their differences from the GENES setting are
`r paste(sprintf("%.2f", cv_difference), collapse = ", ")` percentage points.
The two quantities are therefore retained and interpreted separately.
""",
    """The distinction is visible numerically:

- **Empirical phenotype CV for C1-C6:**
  `r paste(sprintf("%.2f", scenario_summary$CV_empirical_pct), collapse = ", ")`%.
- **Difference from the GENES setting:**
  `r paste(sprintf("%.2f", cv_difference), collapse = ", ")` percentage points.

The GENES setting and the empirical phenotype CV are therefore retained as
separate quantities with separate interpretations.
""",
    "CV interpretation",
)

replace_once(
    """The observed proportions can be compared directly with the expected F2
proportions. This verifies that the genotype matrix has the segregation pattern
expected from the simulated cross before the markers enter prediction models.
""",
    """The segregation figure is used for two related checks:

- **Observed pattern:** genotype classes 0, 1, and 2 occur close to the expected
  F2 proportions 0.25, 0.50, and 0.25.
- **Purpose:** the comparison confirms that the complete marker matrix reflects
  the segregation pattern expected from the simulated cross before it enters
  the prediction models.
""",
    "F2 interpretation",
)

replace_once(
    """The complete genotype matrix is retained for downstream prediction with the same
individuals and markers described above.
""",
    """These summaries are descriptive rather than filtering rules. Consequently:

- no marker is removed because of these summaries in this module;
- the complete genotype matrix is passed downstream with the same individuals
  and markers described above.
""",
    "marker properties conclusion",
)

replace_once(
    """Both parents occur in all 10 linkage groups. Parent 1 is fixed for marker state
1 and parent 2 for marker state 0, providing the contrasting homozygous states
from which the F2 genotypes were generated.
""",
    """The parental summary establishes the simulated cross directly:

- **Coverage:** both parents are represented in all 10 linkage groups.
- **Parent 1:** fixed for marker state 1.
- **Parent 2:** fixed for marker state 0.
- **Implication:** these contrasting homozygous parental states generate the
  three genotype classes observed in the F2 population.
""",
    "parent interpretation",
)

# Guard the structural requests from this pass.
for forbidden in [
    "### 6.3",
    "### 6.4",
    "genetic-map-qtl",
    "genetic_map_with_qtl.tiff",
    "The number of simulated QTL increases from 8 in C1 to 480 in C6",
]:
    if forbidden in text:
        raise SystemExit(f"Redundant content remains: {forbidden}")

path.write_text(text, encoding="utf-8", newline="\n")
print("OK - M01 reader-polish pass 2 applied")
print("Residual Section 6 redundancy removed")
print("Terse conclusions expanded into compact reading points")
