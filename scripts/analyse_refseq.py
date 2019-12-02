#!/usr/bin/env python
# script to analyse historical refseq releases
import os
import glob
import re
import sys
import hashlib

# Function to md5check files - shamelessly stolen from https://www.joelverhagen.com/blog/2011/02/md5-hash-of-file-in-python/
def md5check(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

#obtain script path and set as working directory of script
script_path = os.path.dirname(os.path.abspath( __file__ ))
print('Script Path: \n%s\n' %script_path)
os.chdir(script_path)
print('mkdir -pv ../data ../plots' )

#retrieve md5 of local catalogue collection
if os.path.exists('../data/refseq.txt'):
    old_md5 = md5check('../data/refseq.txt')
else:
    old_md5='None'

#update local ref seq catalogue
os.system("set -euo pipefail; curl -L https://ftp.ncbi.nlm.nih.gov/refseq/release/release-catalog/archive/ | grep 'catalog.gz' > ../data/refseq.txt")

#retrieve new md5 checksum and stop script if no new additions
#if md5check('../data/refseq.txt') == old_md5:
#    raise ValueError('No new data releases for refseq!')

# Read in  latest catalog result
with open('../data/refseq.txt', 'rt') as infile:
    refseq_raw = infile.readlines()

#define lists to append clean database results to
catalogue = []
dates = []
sizes = []

#obtain release version, date and size of each refseq release in a nicely formatted table
for line in refseq_raw:
    dirty_cat = line.split('</a>                                  ')[0]
    clean_cat = dirty_cat.split('">')[-1]
    dirty_size = line.split(':')[-1]
    dirty_size = dirty_size[2:]
    clean_size = re.sub('\n', '', dirty_size)
    dirty_date = line.split('</a>')[-1]
    dirty_date = dirty_date.split(':')[0]
    dirty_date = dirty_date.split(' ')[-2]
    clean_date = re.sub(' ','', dirty_date)
    print('%s\t%s\t%s' %(clean_cat, clean_date, clean_size) )
    catalogue.append(clean_cat)
    dates.append(clean_date)
    sizes.append(clean_size)

#save catalogue to a file
catfile =  open('../data/clean_catalogue.tsv', 'wt')
catfile.write('catalogue\tdate_released\tsize\n')
for i in range(0,len(catalogue)):
    catfile.write('%s\t%s\t%s\n' %(catalogue[i], dates[i], sizes[i]) )
catfile.close()    


#loop through the list of files processed - download and process any that need to be done
if not os.path.exists('../data/refseq_analysis.tsv'):
    os.system('echo "category	date_of_release	catalogue_size	unique_taxids	unique_species	complete_fungi	complete_invertebrate	complete_microbial	complete_plasmid	complete_protozoa	complete_mammaliancomplete_other_vertebrate	complete_viral	complete_plant" > ../data/refseq_analysis.tsv')

with open('../data/refseq_analysis.tsv', 'rt') as analysed_file:
    analysed = analysed_file.readlines()

analysed_catalogues = []

for line in analysed:
    cat = line.split('\t')[0]
    if cat != 'category':
        analysed_catalogues.append(cat)

for cat in catalogue:
    if cat in analysed_catalogues:
        continue
    else:
        # Download the Catalogue
        os.system('wget https://ftp.ncbi.nlm.nih.gov/refseq/release/release-catalog/archive/%s' %(cat) )
        # Analyse the Catalogue
        os.system('Rscript read_catalogue.R %s' %(cat) )
        # Remove the large file
        os.system('rm -f %s' %(cat) )


#render the html of the new data

