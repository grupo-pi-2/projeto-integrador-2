from django.db import models
from django.forms.models import model_to_dict

# Create your models here.
class Setor(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return str(model_to_dict(self))
