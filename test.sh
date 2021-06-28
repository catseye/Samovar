#!/bin/sh

APPLIANCES=""

if [ "x$PYTHON" != "x" ]; then
    if command -v "$PYTHON" > /dev/null 2>&1; then
        PYTHONPATH=src $PYTHON src/samovar/tests.py || exit 1
    else
        echo "$PYTHON not found on executable search path. Aborting."
        exit 1
    fi
else
    MISSING=""
    if command -v python2 > /dev/null 2>&1; then
        PYTHONPATH=src python2 src/samovar/tests.py || exit 1
        APPLIANCES="$APPLIANCES doc/appliances/samovar.py2.md"
    else
        MISSING="${MISSING}2"
    fi
    if command -v python3 > /dev/null 2>&1; then
        PYTHONPATH=src python3 src/samovar/tests.py || exit 1
        APPLIANCES="$APPLIANCES doc/appliances/samovar.py3.md"
    else
        MISSING="${MISSING}3"
    fi
    if [ "x${MISSING}" = "x23" ]; then
        echo "Neither python2 nor python3 found on executable search path. Aborting."
        exit 1
    fi
fi

falderal $APPLIANCES doc/Samovar.md || exit 1
