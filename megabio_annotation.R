library(dplyr)

# Read data

megabioCSU <- read.csv('megabio_annotations_CSU.csv')

aafcProtIDs <- read.table('megabioAAFCProtID.txt')

megabioNew <- megabioCSU[megabioCSU$ProtID %in% aafcProtIDs$V1,]

megabioNew <- megabioCSU[megabioCSU$ProtID %in% aafcProtIDs$V1,]

write.csv(megabioNew, 'megabio_AAFC_v0.1_annotations.csv', row.names = FALSE)

megabioNewHeaders <- read.csv('megabio_updated_headers.csv')

megabioMerged <- merge(megabioNew, megabioNewHeaders, by="ProtID")

write.csv(megabioMerged, 'megabio_AAFC_v0.1_Merged.csv', row.names = FALSE)

megabioNewClean <- megabioMerged %>% select(-c("Header", "ProtID"))

megabioNewClean <- megabioMerged %>% select(-c(.data$Header, .data$ProtID))

names(megabioNewClean) <- c('gene', 'class', 'mechanism', 'header')

write.csv(megabioNewClean, 'megabio_AAFC_v0.1_annotations_NewHeader.csv')
