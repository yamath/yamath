#! /bin/sh
git add .
git commit -m "$@"
git push origin master
echo "Ricordati di fare il pull dall'altro lato!"
