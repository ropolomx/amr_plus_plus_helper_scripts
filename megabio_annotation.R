library(dplyr)

# Read data

megabioCSU <- read.csv('megabio_annotations_CSU.csv')

aafcProtIDs <- read.table('megabioAAFCProtID.txt')

# Filter old dataset to match Protein IDs only present in new dataset

megabioNew <- megabioCSU[megabioCSU$ProtID %in% aafcProtIDs$V1,]

write.csv(megabioNew, 'megabio_AAFC_v0.1_annotations.csv', row.names = FALSE)

# Read file generated with Pandas that includes the ProtIDs and the new headers
megabioNewHeaders <- read.csv('megabio_updated_headers.csv')

# Merge data frames by Protein ID
megabioMerged <- merge(megabioNew, megabioNewHeaders, by="ProtID")

# Export to CSV
write.csv(megabioMerged, 'megabio_AAFC_v0.1_Merged.csv', row.names = FALSE)

# Remove unnecessary columns for Galaxy workflow

megabioNewClean <- megabioMerged %>% select(-c(.data$Header, .data$ProtID))

# Rename dataframe columns

names(megabioNewClean) <- c('gene', 'class', 'mechanism', 'header')

# Export to CSV: this is the "official" MegaBio

write.csv(megabioNewClean, 'megabio_AAFC_v0.1_annotations_NewHeader.csv')
