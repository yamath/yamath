#! /bin/bash
git add .
git commit -m '$1'
git push origin master
echo "Ricordati di fare il pull dal sito!"
