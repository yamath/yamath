#!/bin/bash
source /venv/bin/activate
cd yamath/
python manage.py shell -c "import yapp.forget;"