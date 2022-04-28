#!/bin/bash
 

if [ -z "$PY3EVE" ]; then
  source usepy3 eve
  export PYTHONPATH=$(dirname $(which python))/envs/eve/lib/python3.6/site-packages/:$PYTHONPATH 
  export PY3EVE=1
else
  echo "#set:py3eve"
fi
