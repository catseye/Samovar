#!/bin/sh

THIS_SCRIPT=`realpath $0`
cd `dirname $THIS_SCRIPT`
samovar scenes.samovar --seed=0 --min-events=40 > events.txt
python formatter.py < events.txt > novel.md
cat novel.md
wc -w novel.md

