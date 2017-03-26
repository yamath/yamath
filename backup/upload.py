import blooming.models as blooming
from django.contrib.auth.models import User
import backup.datadump as dump

for u in dump.users:
    print(u[1])