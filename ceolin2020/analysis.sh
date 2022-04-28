#!/bin/bash

# make romance family sswl+longobardi tree with modified jaccard metric

python sswl_modjaccard_rom.py &> romance_sswl_modified_jaccard.txt

# make trees with outgroups

python subfamilies_outgroup.py 
