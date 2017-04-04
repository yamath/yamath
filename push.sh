#! /bin/sh
cp yamath/cloudsettings.py yamath/settings.py
git add .
git commit -m "$@"
git push origin master
cp yamath/hardcopysettings.py yamath/seyyings.py
echo "Ricordati di fare il pull dall'altro lato!"
