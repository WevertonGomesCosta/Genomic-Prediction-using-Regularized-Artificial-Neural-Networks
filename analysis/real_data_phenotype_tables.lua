-- Apply the existing Bootstrap table style to static R01 Markdown tables.
-- Scientific tables are generated separately by knitr::kable().
local reference_tables = {
  ["Variables in the phenotypic data"] = true,
  ["Terms in the phenotypic mixed model"] = true,
  ["Trait-specific fitting settings"] = true,
  ["Saved phenotypic outputs and their role in the genomic workflow"] = true
}

function Table(tbl)
  local caption = pandoc.utils.stringify(tbl.caption.long)
  if reference_tables[caption] then
    tbl.attr = pandoc.Attr("", {
      "table", "table-striped", "table-hover", "table-bordered"
    }, {width = "100%"})
  end
  return tbl
end
