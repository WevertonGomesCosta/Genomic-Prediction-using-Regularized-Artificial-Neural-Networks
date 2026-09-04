from pathlib import Path

path = Path("analysis/simulated_data_audit.Rmd")
text = path.read_text(encoding="utf-8")

replacements = [
    (
        "Every figure displayed in the page uses `theme_gdocs()````\n\nFor figure output, two rules are applied consistently:",
        "For figure output, two rules are applied consistently:",
        "package/figure formatting artifact",
    ),
    (
        "The exact counts behind the figure are useful when comparing scenarios.```\n\nThe figure gives the spatial pattern, while the table below provides the exact\ncounts needed to verify it:",
        "The figure gives the spatial pattern, while the table below provides the exact\ncounts needed to verify it:",
        "QTL-count formatting artifact",
    ),
    (
        "The exact numerical summaries are shown below```\n\nThe figure summarizes the pattern visually; the tables below retain the exact\nnumbers needed to interpret it:",
        "The figure summarizes the pattern visually; the tables below retain the exact\nnumbers needed to interpret it:",
        "LD-table formatting artifact",
    ),
    (
        """The separation between Sections 5 and 6 is intentional:\n\n- **Section 5** establishes only the marker framework and linkage-group\n  structure;\n- **Section 6** adds QTL once, using the scenario-specific figure to compare\n  their positions and density across C1-C6.\n\nThis avoids presenting the same QTL information in both a combined map and a\nscenario map.""",
        """With the marker map defined, the simulated genetic architecture can be added\nwithout mixing the two levels of information:\n\n- **Marker framework:** Section 5 establishes LG1-LG10, marker order, and map\n  positions independently of the simulated QTL.\n- **QTL architecture:** Section 6 places the QTL from each scenario on that fixed\n  framework and compares their distribution across C1-C6.\n\nKeeping these layers separate lets the reader first understand where markers are\nlocated and then examine which of those positions were selected as QTL in each\nscenario.""",
        "Section 5 to Section 6 transition",
    ),
    (
        """The two simulated parents are contrasting homozygotes, so an F2 population is\nexpected to approach a `1:2:1` segregation for the three genotype classes. The\nnext calculation uses every genotype call in the 1,000 x 4,010 matrix to compare\nthe observed proportions with the theoretical values 0.25, 0.50, and 0.25.""",
        """The expected segregation follows directly from the simulated cross:\n\n- **Parental contrast:** the two parents are homozygous for opposite marker\n  states.\n- **F2 expectation:** the three genotype classes should occur approximately in\n  the ratio `1:2:1`, corresponding to proportions 0.25, 0.50, and 0.25.\n- **Observed comparison:** all genotype calls in the 1,000 x 4,010 matrix are\n  used to calculate the realized class proportions.\n\nThe figure therefore compares the complete simulated marker matrix with the\ntheoretical segregation expected for an F2 population.""",
        "F2 segregation introduction",
    ),
]

for old, new, label in replacements:
    if old not in text:
        raise SystemExit(f"Missing expected text for: {label}")
    text = text.replace(old, new, 1)

# Guard against the formatting residues fixed above.
for bad in [
    "theme_gdocs()````",
    "useful when comparing scenarios.```",
    "summaries are shown below```",
]:
    if bad in text:
        raise SystemExit(f"Formatting residue remains: {bad}")

path.write_text(text, encoding="utf-8", newline="\n")
print("OK - M01 reader-text cleanup applied")
