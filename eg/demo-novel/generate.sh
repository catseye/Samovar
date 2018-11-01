#!/bin/sh

samovar settings.samovar scenes.samovar --min-events=12 | python formatter.py
