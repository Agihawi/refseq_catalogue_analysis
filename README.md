#This repo will curate information about various NCBI refseq releases

To run simply type:
`scripts/analyse_refseq.py`

which should need about 20gb RAM as of 2nd dec 2019

Then when you have an up to date file in 
`data/refseq_analysis.tsv`

You can render some plots with the rmarkdown with
`scripts/render_refseq.Rmd`

The script should produce a nice output in the plots/directory
