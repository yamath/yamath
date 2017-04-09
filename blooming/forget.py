from bloomerprofile.models import *
from random import choice
import logging

for bloomer in Bloomer.objects.all():
    bloomer.add_forget()

logging.info("Everybody forgot something")