#!/bin/bash



if [ -z "$PY3EVE" ]; then
  source usepy3 eve
  export PY3EVE=1
else
  echo "#set:py3eve"
fi


export PYTHONPATH=$PYBASE/envs/eve/lib/python3.6/site-packages/:$PYTHONPATH
