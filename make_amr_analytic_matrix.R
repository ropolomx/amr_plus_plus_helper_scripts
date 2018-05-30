
# Load packages -----------------------------------------------------------

library(tidyverse)

# library(stringr) 
# Need to load if using tidyverse version 1.1.1. Not necessary to load separately if using tidyverse 1.2.1

library(here)

# Create directory for aggregated data ------------------------------------

aggregated_dir <- here("resistome_workshop")

ifelse(
  !dir.exists(aggregated_dir), 
  dir.create((aggregated_dir), mode='777'), 
FALSE
)

# Read AMR Resistome Analyzer Results -------------------------------

# Parse the results with Python script first
# Then collect the names of the parsed files

amrCovSamplerPaths <- Sys.glob(here("AMR_parsed", '*_parsed.tab'))

amrCovSamplerNames <- list.files(
  path = here("./AMR_parsed"),
  pattern = "*_parsed.tab"
  ) %>%
  map(function(x) str_replace(x, "_CovSampler_parsed\\.tab$", ""))

amrCovSampler <- amrCovSamplerPaths %>%
  map(function(x) read_tsv(x)) %>% 
      set_names(nm=amrCovSamplerNames)

amrReportsMerged <- amrCovSampler %>%
  map_dfr(function(x) x, .id="Sample")
          
amrReportsFiltered <- amrReportsMerged %>%
  filter(`Gene Fraction` >= 75)

amrAnalytical <- amrReportsFiltered %>%
  select(Sample, Header, Hits) %>%
  spread(key = Sample, value = Hits, fill = 0)

amrClassification <- amrAnalytical$Header

amrAnalytical <- amrAnalytical %>%
  select(-Header) %>%
  as.matrix(.)

row.names(amrAnalytical) <- amrClassification

write.csv(amrAnalytical, here('resistome_workshop', 'amr_analytic_matrix.csv'))