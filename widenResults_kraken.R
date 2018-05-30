
# Load packages -----------------------------------------------------------

library(tidyverse)
library(pavian)
library(here)


# Custom functions for script ---------------------------------------------

mutate_tax <- function(lineage, tax_pattern){
  split_lin <- map(
    lineage,
    ~ str_extract(.x, tax_pattern) %>%
      purrr::discard(is.na)
  )
  split_lin <- split_lin %>% as.character()
}

make_kraken_analytical <- function(x, column){
  x <- x %>%
    select(Sample, column, taxLineage) %>%
    spread(key = Sample, value = column, fill = 0) %>%
    rename(Lineage = taxLineage)
  x
}
# Create directory for aggregated data ------------------------------------

aggregated_dir <- here("aggregated_data_for_analysis")

ifelse(
  !dir.exists(aggregated_dir), 
  dir.create((aggregated_dir), mode='777'), 
FALSE
)

# Read and parse Kraken reports with Pavian backend -----------------------

# Obtain the filenames of all Kraken reports

krakenReportPaths <- Sys.glob(here("Kraken_reports",'*.tabular'))

krakenReportNames <- list.files(path = here("Kraken_reports"), pattern = '*.tabular')

krakenReportNames <- 
  krakenReportNames %>%
  map(~ str_replace(.x, "\\.tabular$", "")) %>%
  map(~ str_replace(.x, "_Kraken",""))

krakenReportsPavian <-
  krakenReportPaths %>%
  map(function(x) pavian::read_report(x)) %>%
  set_names(nm = krakenReportNames)
  
krakenReportsPavian <-
  krakenReportsPavian %>%
  map(safely(function(x){
    filt <- pavian::filter_taxon(
    report = x, 
    filter_taxon = c("Eukaryota"),
    rm_clade = TRUE, 
    do_message = TRUE
    )
    filt
}))

taxa_to_remove <- c("u_unclassified", "-_root", "-_cellular organisms")

krakenReportsPavianFilter <-
  krakenReportsPavian %>%
  map(function(x) {
    new_df <- x$result %>%
      filter(!name %in% taxa_to_remove) %>%
      filter(taxRank != "-") %>%
      filter(cladeReads >= 5) %>%
      mutate(taxLineage = str_replace(taxLineage, "-_root\\|-_cellular organisms\\|", "")) %>%
      mutate(taxLineage = str_replace(taxLineage, "-_root\\|", ""))
    new_df
  }
)

# Format taxonomy lineages for Shiny app ----------------------------------

kraken_taxonomy <- 
  krakenReportsPavianFilter %>%
  map(
    ~ mutate(.x, splitting = str_split(taxLineage, "\\|"))
  )

kraken_taxonomy_split <- 
  kraken_taxonomy %>% 
  map(function(x){
    split_tax <- x %>%
      mutate(Domain = mutate_tax(splitting, "^d_.*")) %>% 
      mutate(Phylum = mutate_tax(splitting, "^p_.*")) %>% 
      mutate(Class = mutate_tax(splitting, "^c_.*")) %>%
      mutate(Order = mutate_tax(splitting, "^o_.*")) %>%
      mutate(Family = mutate_tax(splitting, "^f_.*")) %>%
      mutate(Genus = mutate_tax(splitting, "^g_.*")) %>%
      mutate(Species = mutate_tax(splitting, "^s_.*"))
    split_tax
  })

kraken_taxonomy_split <- 
  kraken_taxonomy_split %>%
  map(~ select(.x, -splitting))

kraken_taxonomy_split <-
  kraken_taxonomy_split %>%
  map(~ mutate(
    .x,
    taxLineage = paste(
      Domain,
      Phylum,
      Class,
      Order,
      Family,
      Genus,
      Species,
      sep = "|")
  ))

# Convert all character(0) instances to NA and merge data frames

krakenReportsPavianMerged <-
  kraken_taxonomy_split %>%
  map_dfr(
    ~ mutate(
      .x,
      taxLineage = str_replace_all(taxLineage, "character\\(0\\)", "NA")),
    .id = "Sample")

# Export Analytic Matrices for Clade and Taxon Reads ----------------------

tax_columns <- c("cladeReads", "taxonReads")
  
krakenAnalytical <-
  map(tax_columns,
    ~ make_kraken_analytical(krakenReportsPavianMerged, .x)) %>%
  set_names(nm = tax_columns)

krakenAnalytical <- 
  krakenAnalytical %>%
  map(function(x){
    row.names(x) <- x$Lineage
    x
  })

krakenAnalytical <- 
  krakenAnalytical %>%
  map(
    ~ select(.x, -Lineage)
  )

krakenAnalytical <- krakenAnalytical %>%
  map(function(x){
    mat <- x[rowSums(x) > 0,]
    mat
  })
  
iwalk(
  krakenAnalytical,
  ~ write.csv(
    .x,
    here(
      "aggregated_data_for_analysis",
      paste0("krakenAnalytical", "_", .y, ".csv")
    )
  )
)

