#!/bin/sh

if [ "x$PYTHON" = "x" ]; then
    PYTHON="python2.7"
fi
PYTHONPATH=src $PYTHON src/samovar/tests.py -v || exit 1
falderal -b doc/Samovar.md || exit 1
