#!/bin/bash

if [ -z "$PY3EVE" ]; then
  source usepy3 eve
  export PY3EVE=1
else
  echo "#set:py3eve"
fi


python ./trees.py -germanic -v
python trees.py -slavic -v -skbio -alldb # slovenian clashes with russian
python trees.py -slavic-small -v -skbio -alldb # split into bulgarian/serb-croat russian/polish after removing slovenian
python trees.py -uralic -v -skbio # uralic
python  phylocompute.py  # write invariants to ./data/phyloinvariants.json

