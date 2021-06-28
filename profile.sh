#!/bin/sh

PYTHONPATH=src python3 -m cProfile -s time bin/samovar eg/chairs.samovar --min-events=8000
