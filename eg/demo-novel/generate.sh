#!/bin/sh

THIS_SCRIPT=`realpath $0`
cd `dirname $THIS_SCRIPT`
mkdir -p build
samovar scenes.samovar --seed=0 --min-events=40 > build/events.txt
python formatter.py < build/events.txt > build/novel.md
cat build/novel.md
wc -w build/novel.md
