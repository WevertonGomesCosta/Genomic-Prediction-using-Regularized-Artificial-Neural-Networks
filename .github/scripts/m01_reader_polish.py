from pathlib import Path
import re

path = Path("analysis/simulated_data_audit.Rmd")
text = path.read_text(encoding="utf-8")


def replace_between(start, end, replacement):
    global text
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"Missing start anchor: {start!r}")
    j = text.find(end, i + len(start))
    if j < 0:
        raise SystemExit(f"Missing end anchor: {end!r}")
    text = text[:i] + start + replacement + text[j:]


def regex_replace(pattern, replacement, label):
    global text
    text_new, n = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"Expected one replacement for {label}; found {n}")
    text = text_new


# -----------------------------------------------------------------------------
# 1. Purpose: descriptive but scannable.
# -----------------------------------------------------------------------------
replace_between(
    "## 1. Purpose\n\n",
    "```{r setup, include=FALSE}",
    """This module introduces the simulated genomic population used throughout the
prediction workflow. The data were generated with **GENES**, a software package
for experimental statistics, quantitative genetics, and genetic simulation
(Cruz, 2013, 2016).

The module has four reader-facing goals:

- **Identify the input data:** distinguish phenotype, true genetic value,
  genotype matrix, genetic map, parental genotypes, and simulation settings.
- **Make the data structure explicit:** show how individuals, scenarios,
  markers, linkage groups, and QTL are organized before model fitting.
- **Describe the simulated population:** summarize genetic signal, segregation,
  marker properties, and linkage disequilibrium (LD).
- **Prepare one shared object:** preserve the same individuals, marker coding,
  map, scenarios, and QTL for the validation, GBLUP-ADE, ANN, and comparison
  modules.

No genomic prediction model is fitted here. The purpose is to establish what the
data contain, how the main quantities are represented, and which objects are
passed unchanged to the next stages of the workflow.

""",
)

# -----------------------------------------------------------------------------
# 2. Packages and reproducibility.
# -----------------------------------------------------------------------------
replace_between(
    "### 2.1 Packages\n\n",
    "```{r packages, warning=FALSE, message=FALSE}",
    """Three packages support different parts of the reader-facing analysis:

- **`knitr`** converts R objects into formatted HTML tables, allowing dimensions,
  simulation settings, genotype summaries, and LD values to be inspected
  directly in the page.
- **`ggplot2`** constructs every statistical and genomic figure, including the
  phenotype distributions, chromosome-like linkage-group map, QTL distribution,
  F2 segregation, and LD curve.
- **`ggthemes`** provides `theme_gdocs()` and the matching Google Docs color
  scales so all figures share the same visual language.

The comments in the code provide a short reminder of these roles when the reader
executes the chunk independently.

""",
)

replace_between(
    "```\n\nEvery figure displayed in the page uses `theme_gdocs()`",
    "### 2.2 Random seed",
    """```\n\nFor figure output, two rules are applied consistently:

- figures shown in the HTML use `theme_gdocs()` and Google Docs color/fill
  scales whenever categories are distinguished by color;
- publication-quality TIFF copies are written to
  `output/simulated/m01/figures/`, while the `ggsave()` commands remain in
  `include=FALSE` chunks so file-export instructions do not interrupt the
  analytical code shown to the reader.

""",
)

replace_between(
    "### 2.2 Random seed\n\n",
    "```{r random-seed}",
    """Most quantities in this module are fixed because they are read directly from
the GENES simulation files. The random seed is needed for only one operation:

- **Fixed inputs:** phenotype, true genetic values, genotypes, genetic map,
  parental genotypes, and scenario definitions do not change with the seed.
- **Random operation:** 5,000 marker pairs from different linkage groups are
  sampled in Section 10 to obtain a reproducible background LD reference.

Setting the seed here therefore reproduces the LD reference without modifying
any of the simulated data.

""",
)

# -----------------------------------------------------------------------------
# 3. Phenotype and true genetic value.
# -----------------------------------------------------------------------------
replace_between(
    "## 3. Phenotypic and true genetic values\n\n",
    "### 3.1 Phenotypic values",
    """The first two GENES files describe complementary quantities for the same
1,000 individuals and six scenarios:

- **Phenotype:** the observed response that may be used for model fitting when an
  individual belongs to an analysis set.
- **True genetic value:** the known simulated genetic component, reserved for
  evaluating predictions rather than fitting or partition construction.
- **Alignment:** row `i` in both matrices refers to the same simulated
  individual, so row order must remain unchanged throughout the workflow.

""",
)

replace_between(
    "### 3.1 Phenotypic values\n\n",
    "```{r phenotype,",
    """The phenotypic file is read before any transformation so the reader can see
how the response is organized. The chunk performs three steps:

- read the matrix with individuals in rows and scenarios in columns;
- label the six scenario columns as C1-C6;
- reshape only a plotting copy and use boxplots to compare center, dispersion,
  and extreme values across scenarios.

The original phenotype matrix remains unchanged for all later calculations.

""",
)

replace_between(
    "### 3.2 True genetic values\n\n",
    "```{r true-genetic-values,",
    """Because the population is simulated, the genetic value underlying each
individual is known. Its role differs from the phenotype:

- it is **not** used to create validation partitions;
- it is **not** used to tune or fit the prediction models;
- it is retained as the external target used to evaluate predictions for
  held-out individuals.

The chunk reads the matrix with the same C1-C6 structure and creates a plotting
copy. Comparing its distributions with the phenotype figure separates variation
in the known genetic component from variation in the observed response.

""",
)

# -----------------------------------------------------------------------------
# 4. Genotypes.
# -----------------------------------------------------------------------------
replace_between(
    "### 4.1 Genotype matrix\n\n",
    "```{r genotype-sample}",
    """The GENES genotype file must first be oriented in the same direction as the
response matrices. The reader should note four points:

- **Source orientation:** markers are stored in rows and individuals in columns.
- **Analysis orientation:** the matrix is transposed once, producing individuals
  in rows and markers in columns.
- **Observed coding:** the original genotype states are `0`, `1`, and `2`.
- **Displayed sample:** ten individuals and twelve markers spread across all
  4,010 marker columns are printed so the discrete matrix structure can be seen
  directly; a boxplot would not convey that structure.

The complete matrix, not the displayed sample, is retained for every subsequent
calculation.

""",
)

replace_between(
    "### 4.2 Genotype coding used in the prediction models\n\n",
    "```{r genotype-coding}",
    """The prediction models use the same genotype calls centered on zero. The
recoding is deliberately simple:

- `0 -> -1`;
- `1 -> 0`;
- `2 -> 1`.

Only the numerical scale changes. No individual or marker is removed, and the
underlying genotype class is preserved. The table below makes the transformation
explicit before the recoded matrix is saved for downstream analyses.

""",
)

# -----------------------------------------------------------------------------
# 5. Genetic map: move the chromosome-like map here and keep QTL only in 6.2.
# -----------------------------------------------------------------------------
replace_between(
    "## 5. Genetic map\n\n",
    "```{r genetic-map-data}",
    """The genetic map supplies the genomic organization needed to interpret marker
positions, QTL locations, and LD. The GENES text file is read in two conceptual
parts:

- the first 12 lines describe the map globally;
- marker-level records start on line 13 and provide linkage group, marker order,
  marker name, and position in centimorgans (cM).

For later matching, a global marker index from 1 to 4,010 is added. This index is
the bridge between the QTL numbers stored in the scenario file and their
positions on the genetic map.

""",
)

regex_replace(
    r"```\n\nThe map contains 10 linkage groups, each with 401 markers spanning 0-200 cM at\n0\.5-cM intervals\..*?\n\n## 6\. Simulation settings and QTL architecture",
    """```

The numerical map can be summarized before QTL are introduced:

- **10 linkage groups (LG1-LG10);**
- **401 markers per linkage group;**
- **0-200 cM** covered by each group;
- **0.5 cM** between consecutive markers;
- **4,010 markers** in the complete map.

A chromosome-like representation is used below to make this organization easier
to read. Each colored body represents one linkage group and the short white
ticks show every tenth marker. Displaying a regular subset of marker ticks keeps
the 0.5-cM structure visible without drawing 401 overlapping marks on each
linkage group.

```{r genetic-map-figure, fig.cap="Chromosome-like representation of the ten linkage groups in the simulated genetic map. Colors identify linkage groups and white ticks show every tenth marker position."}
# Create one chromosome-like body for each linkage group.
chromosome_map <- data.frame(
  LG = 1:10,
  LG_label = factor(
    paste0("LG", 1:10),
    levels = paste0("LG", 1:10)
  ),
  Start_cM = 0,
  End_cM = 200
)

# Show a regular subset of marker positions to keep the map legible.
marker_ticks <- genetic_map[
  genetic_map$Marker_within_LG %% 10 == 1,
  c("LG", "LG_label", "Position_cM")
]

p_genetic_map <- ggplot() +
  geom_segment(
    data = chromosome_map,
    aes(
      x = LG_label,
      xend = LG_label,
      y = Start_cM,
      yend = End_cM,
      color = LG_label
    ),
    linewidth = 12,
    lineend = "round",
    show.legend = FALSE
  ) +
  geom_point(
    data = marker_ticks,
    aes(
      x = LG_label,
      y = Position_cM
    ),
    shape = 95,
    size = 4.2,
    color = "white",
    alpha = 0.85
  ) +
  scale_color_gdocs() +
  scale_y_reverse(
    breaks = seq(0, 200, 25),
    expand = expansion(mult = c(0.035, 0.035))
  ) +
  labs(
    x = "Linkage group",
    y = "Position (cM)"
  ) +
  theme_gdocs()

print(p_genetic_map)
```

```{r save-genetic-map-tiff, include=FALSE}
ggsave(
  "output/simulated/m01/figures/genetic_map.tiff",
  plot = p_genetic_map,
  device = "tiff",
  width = 9,
  height = 6,
  units = "in",
  dpi = 300,
  compression = "lzw"
)
```

The map now establishes the marker framework by itself. QTL are introduced only
once, in Section 6, where their distribution is compared across the six
simulation scenarios.

## 6. Simulation settings and QTL architecture""",
    "genetic-map transition",
)

# -----------------------------------------------------------------------------
# 6. Simulation model and scenarios. Remove the old combined-QTL map entirely.
# -----------------------------------------------------------------------------
regex_replace(
    r"### 6\.1 GENES software and genetic model\n\n.*?\n\n### 6\.2 Scenario settings and QTL positions",
    r"""### 6.1 GENES software and genetic model

The six scenarios were generated with **GENES** (Cruz, 2013, 2016). The control
file specifies `Model = 2`, represented by

\[
Y_i =
\mu +
\sum_j a_j +
\sum_j \sum_{j'} \alpha_j\alpha_{j'} +
\varepsilon_i .
\]

The terms have distinct roles in the simulation:

- \(Y_i\): phenotype generated for individual \(i\);
- \(\mu\): overall mean;
- \(\sum_j a_j\): contributions associated with loci;
- \(\sum_j\sum_{j'}\alpha_j\alpha_{j'}\): pairwise interaction contributions
  between loci;
- \(\varepsilon_i\): residual component.

This equation describes **data generation**, not the GBLUP-ADE or ANN prediction
models fitted later.

### 6.2 Scenario settings and QTL distribution""",
    "section 6.1",
)

replace_between(
    "### 6.2 Scenario settings and QTL distribution\n\n",
    "```{r simulation-scenarios}",
    """The control file contains six repeated blocks, one for each scenario C1-C6.
The code reads the blocks directly because the fields occur in a fixed order.
The reader can follow the preparation in four steps:

- **Read the scenario settings:** number of QTL, specified heritability, genetic
  model, constant, scale, and CV setting.
- **Read the QTL indices:** each selected QTL is stored as an integer marker
  index in the control file.
- **Match QTL to the genetic map:** each index is converted to its linkage group
  and position in cM using the global marker index from Section 5.
- **Reuse one QTL table:** the matched positions are used for the figure, the
  count table, and the object passed to later modules.

""",
)

# Remove the old combined-QTL map (formerly 6.3) and its save chunk. Keep only
# the scenario-specific figure, which is the informative comparison requested.
regex_replace(
    r"\nTo make the map biologically easier to read, each linkage group is represented.*?\n```\{r qtl-map,",
    """
The six scenarios differ in two main characteristics that should be interpreted
together:

- **QTL number increases:** 8, 40, 80, 120, 240, and 480 from C1 to C6;
- **specified heritability decreases:** 0.7 in C1-C2, 0.5 in C3-C4, and 0.3 in
  C5-C6;
- **other settings remain fixed:** `gmd = 0.5`, `Model = 2`, `Constant = 100`,
  `Scale = 1`, and `CV = 12`;
- **LG9 and LG10 contain no simulated QTL:** they retain markers but provide
  reference genomic regions without a true QTL signal.

The single QTL figure below is therefore organized by **scenario**. Each panel
uses the chromosome-like linkage-group representation from Section 5 and places
all QTL for that scenario on their mapped positions. This avoids repeating a
second combined QTL map while still showing both genomic location and the
increase in QTL density across C1-C6.

```{r qtl-map,""",
    "remove redundant combined QTL map",
)

replace_between(
    "```\n\nThe exact counts behind the figure are useful when comparing scenarios.",
    "```{r qtl-counts}",
    """```

The figure gives the spatial pattern, while the table below provides the exact
counts needed to verify it:

- rows correspond to scenarios C1-C6;
- columns correspond to LG1-LG10;
- each cell is the number of QTL placed in that linkage group;
- the zero counts in LG9 and LG10 make their reference role explicit.

""",
)

# -----------------------------------------------------------------------------
# 7. Genetic signal: break dense prose into interpretation points.
# -----------------------------------------------------------------------------
replace_between(
    "## 7. Phenotypic and genetic signal\n\n",
    "```{r phenotypic-genetic-signal}",
    r"""Because both phenotype \(Y\) and true genetic value \(G\) are known in the
simulation, the remaining component can be calculated directly as

\[
E = Y - G.
\]

The section then describes the strength of the simulated genetic signal using
four complementary quantities:

- **Phenotype-genetic correlation:** how closely the observed phenotype follows
  the known genetic value.
- **Genetic-residual correlation:** whether the simulated genetic and remaining
  components show residual association.
- **Realized heritability:** the proportion obtained from the genetic and
  residual variances actually present in the generated population.
- **Location and dispersion summaries:** means and standard deviations used to
  describe the scale of each scenario.

Together these summaries provide context for why prediction difficulty differs
among scenarios before any model is fitted.

""",
)

replace_between(
    "### 7.1 Specified and realized heritability\n\n",
    "```{r heritability-comparison,",
    """Two heritability quantities are intentionally kept separate:

- **Specified heritability:** the value entered in GENES when a scenario was
  generated.
- **Realized heritability:** the value calculated afterward from the genetic and
  residual variances observed in this finite simulated population.

The comparison shows how closely each generated sample reflects its specified
setting without redefining the scenario itself.

""",
)

replace_between(
    "### 7.2 GENES CV setting and empirical phenotype CV\n\n",
    "```{r cv-comparison,",
    """The value `CV = 12` stored by GENES and the empirical phenotype CV answer
different questions:

- **GENES CV setting:** an input recorded in the simulation control file;
- **empirical phenotype CV:** `100 x SD / mean`, calculated from the phenotype
  values actually generated in each scenario.

Displaying both prevents a simulation input from being mistaken for a
descriptive statistic of this particular finite population.

""",
)

# -----------------------------------------------------------------------------
# 8-9. Replace dense definition paragraphs with compact explanatory points.
# -----------------------------------------------------------------------------
replace_between(
    "### 8.2 Marker and individual properties\n\n",
    "```{r genotype-checks}",
    """The genotype matrix is also described from several complementary angles:

- **Missing genotype cells:** absent marker calls.
- **Duplicate individuals:** rows with identical complete marker profiles.
- **Duplicate markers:** columns with identical profiles across all individuals.
- **Monomorphic markers:** markers with no genotype variation.
- **Minor allele frequency (MAF):** balance between the two alleles at each
  marker.
- **Heterozygosity:** proportion of individuals in the heterozygous class at
  each marker.

These quantities describe the simulated data. They are not used here as an
automatic filtering rule.

""",
)

replace_between(
    "## 9. Parental genotypes\n\n",
    "```{r parental-genotypes}",
    """The parental file links the F2 population to the two homozygous parents used
by GENES. The chunk reads four pieces of information:

- parent identifier;
- linkage-group identifier;
- reported number of markers;
- the 401 marker states within each linkage group.

The resulting summary checks that both parents cover all ten linkage groups and
shows the contrasting fixed states from which the three F2 genotype classes were
generated.

""",
)

# -----------------------------------------------------------------------------
# 10. One undivided LD section, using bullets for within/between and workflow.
# -----------------------------------------------------------------------------
replace_between(
    "## 10. Linkage disequilibrium\n\n",
    "```{r linkage-disequilibrium,",
    r"""Linkage disequilibrium (LD) measures non-random association between marker
genotypes. Here it is summarized by \(r^2\), the squared correlation between two
marker columns.

The analysis distinguishes two kinds of marker pairs:

- **Within linkage group:** both markers belong to the same LG. Because they
  share the same genetic map, their separation can be measured in cM and LD can
  be examined as a function of map distance.
- **Between linkage groups:** the two markers belong to different LGs. A
  within-group map distance is not defined for such pairs, so their mean
  \(r^2\) is used as a background reference for association between different
  linkage groups.

The LD calculation follows a direct sequence:

1. standardize the 4,010 marker columns across the 1,000 individuals;
2. exploit the regular 0.5-cM marker spacing to convert each requested distance
   into a marker shift (for example, 10 cM = 20 intervals);
3. calculate \(r^2\) for all valid within-LG pairs at 0.5, 1, 2.5, 5, 10, 25,
   50, 100, and 200 cM;
4. independently sample 5,000 between-LG pairs to obtain the background
   reference;
5. compare the distance-dependent within-LG curve with the between-LG reference.

The x-axis displays the nine evaluated distances as ordered categories with
equal visual spacing because a continuous 0.5-200 cM axis compresses the short
distances. This changes only the figure layout: every calculation still uses the
true numeric distance in cM.

""",
)

replace_between(
    "```\n\nThe exact numerical summaries are shown below",
    "```{r linkage-disequilibrium-table}",
    """```

The figure summarizes the pattern visually; the tables below retain the exact
numbers needed to interpret it:

- the first table reports within-LG mean and median \(r^2\) at each true map
  distance;
- the second reports the between-LG background reference from 5,000 sampled
  pairs.

""",
)

# -----------------------------------------------------------------------------
# 11-12. Make final sections easier to scan.
# -----------------------------------------------------------------------------
replace_between(
    "## 11. Summary of the simulated data\n\n",
    "```{r data-summary}",
    """Before moving to the validation design, the final table collects the main
structural facts established in the module:

- population size and number of simulation scenarios;
- total markers, linkage groups, and markers per linkage group;
- missing, duplicate, and monomorphic genotype patterns;
- minimum MAF;
- background LD between linkage groups.

The table is a compact description of the prepared data, while the biological
and statistical interpretation remains in the sections where each quantity is
introduced.

""",
)

replace_between(
    "## 12. Shared data object for later modules\n\n",
    "```{r save-shared-data, include=FALSE}",
    """The later modules should not independently reinterpret or reconstruct the
simulation files. One shared object is therefore saved with the quantities
prepared above.

Its most important roles are:

- **`phenotype`:** response available for fitting only within the appropriate
  analysis set;
- **`genotype_m101`:** `-1/0/1` marker representation used by the prediction
  models;
- **`true_genetic_value`:** known simulated target reserved for held-out
  evaluation;
- **map and scenario objects:** linkage groups, QTL, scenario definitions, marker
  summaries, and LD values reused unchanged downstream.

The saving code is hidden because it is workflow plumbing rather than a new
scientific calculation. The historical field name `CV_metadata` is preserved
only inside the saved objects and CSV schema for compatibility; the visible
text consistently calls this quantity the **GENES CV setting**.

""",
)

# -----------------------------------------------------------------------------
# Contract checks for this editorial pass.
# -----------------------------------------------------------------------------
for forbidden in [
    "### 6.3",
    "### 6.4",
    "genetic-map-qtl",
    "genetic_map_with_qtl.tiff",
]:
    if forbidden in text:
        raise SystemExit(f"Redundant Section 6 content remains: {forbidden}")

if text.count("```{r save-") != text.count("ggsave("):
    raise SystemExit("Each ggsave() must have its own save-* chunk")

for match in re.finditer(r"```\{r save-[^}]+\}", text):
    if "include=FALSE" not in match.group(0):
        raise SystemExit(f"Visible ggsave chunk remains: {match.group(0)}")

if "### 10." in text:
    raise SystemExit("Section 10 must not contain numbered subsections")

if "output/simulated/m01/figures/genetic_map.tiff" not in text:
    raise SystemExit("New chromosome-like genetic map TIFF is missing")

path.write_text(text, encoding="utf-8", newline="\n")
print("OK - M01 reader-polish patch applied")
print("Redundant combined QTL map removed")
print("Chromosome-like marker map moved to Section 5")
print("Scenario-specific QTL map retained as the single QTL figure")
print("Long prose converted to descriptive reading points")
print("Section 10 remains a single section")
print("All ggsave chunks remain include=FALSE")
