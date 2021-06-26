#!/bin/sh

PYTHONPATH=src python2 src/samovar/tests.py || exit 1
PYTHONPATH=src python3 src/samovar/tests.py || exit 1
falderal -b doc/Samovar.md || exit 1
