#!/usr/bin/env Rscript
library(readr)
library(dplyr)
library(stringr)

#obtain command line arguments
args = commandArgs(trailingOnly=TRUE)

input_filename = args[1]
#input_filename = 'RefSeq-release2.catalog.gz'

# Load key files
in_cat <- read_tsv(file=input_filename, 
                   col_names =c('TaxID', 'Species_Name', 'Accession_version', 'GI_num', 'refseq_release', 'refseq_status', 'length'))
cat_summary = read_tsv(file='../data/clean_catalogue.tsv', col_names=TRUE)

# Find summary data
num_unique_taxid <- length(unique(in_cat$TaxID))
num_unique_species <- length(unique(in_cat$Species_Name))
# Summarise complete genomes
num_complete_fungi <- length(which(in_cat$refseq_release== 'complete|fungi'))
num_complete_invertebrate <- length(which(in_cat$refseq_release== 'complete|invertebrate'))
num_complete_microbial <- length(which(in_cat$refseq_release== 'complete|microbial'))
num_complete_plasmid <- length(which(in_cat$refseq_release== 'complete|plasmid'))
num_complete_protozoa <- length(which(in_cat$refseq_release== 'complete|protozoa'))
num_complete_mammalian <- length(which(in_cat$refseq_release== 'complete|vertebrate_mammalian'))
num_complete_other_vertebrate <- length(which(in_cat$refseq_release== 'complete|vertebrate_other'))
num_complete_viral <- length(which(in_cat$refseq_release== 'complete|viral'))
num_complete_plant <- length(which(in_cat$refseq_release=='complete|plant'))
num_complete_bacterial <- length(which(in_cat$refseq_release=='bacteria|complete'))

# Isolate catalogue size and date information from catalogue summary
cat_data <- cat_summary %>% 
  filter(str_detect(catalogue, pattern=input_filename))

cat_data <- as.matrix(cat_data)

cat_date_of_release <- unname(cat_data[1,2])
cat_catalogue_size <- unname(cat_data[1,3])
# Make a dataframe of summary data
results_df <- data.frame(category= input_filename,
                         date_of_release = cat_date_of_release,
                         catalogue_size = cat_catalogue_size,
                         unique_taxids = num_unique_taxid,
                         unique_species = num_unique_species,
                         complete_fungi =  num_complete_fungi,
                         complete_invertebrate  =  num_complete_invertebrate, 
                         complete_microbial  =  num_complete_microbial,
                         complete_plasmid  =  num_complete_plasmid,
                         complete_protozoa =  num_complete_protozoa,
                         complete_mammalian  =  num_complete_mammalian,
                         complete_other_vertebrate  =  num_complete_other_vertebrate,
                         complete_viral  =  num_complete_viral,
                         complete_plant  =  num_complete_plant,
                         complete_bacterial = num_complete_bacterial)

#write results to file or append to file
if(!file.exists('../data/refseq_analysis.tsv')) {
  write.table(results_df, file = '../data/refseq_analysis.tsv', row.names = FALSE, col.names = TRUE, sep='\t', quote=FALSE)
} else{
  old_results <- read_tsv(file='../data/refseq_analysis.tsv', col_names=TRUE)
  new_results <- rbind(old_results, results_df)
  #check for duplicates
  new_results <- new_results %>% filter(!duplicated(new_results))
  write.table(new_results, file = '../data/refseq_analysis.tsv', row.names = FALSE, col.names = TRUE, sep='\t', quote=FALSE)
}




