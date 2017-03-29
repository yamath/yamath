#! /bin/bash
source /home/yamatteo/bloomingmath-project/venv/bin/activate
cd /home/yamatteo/bloomingmath-project/yamath
rm local
python manage.py makemigrations backend blooming
python manage.py migrate
python manage.py runserver