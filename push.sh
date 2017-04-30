#! /bin/sh
cp yamath/cloudsettings.py yamath/settings.py
git add .
git commit -m "$@"
git push https://yamath:raimondi127@github.com/yamath/yamath.git master
cp yamath/hardcopysettings.py yamath/settings.py
echo "Ricordati di fare il pull dall'altro lato!"
