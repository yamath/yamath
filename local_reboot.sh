#! /bin/bash
source /home/yamatteo/bloomingmath-project/venv/bin/activate
cd /home/yamatteo/bloomingmath-project/yamath
rm local
python manage.py makemigrations backend blooming content
python manage.py migrate
#python manage.py shell -c "import backup.erase_database;"
python manage.py shell -c "import backup.upload;"
#python manage.py runserver