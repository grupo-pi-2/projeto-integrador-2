from django.db import models
from django.forms.models import model_to_dict

# Create your models here.
class Setor(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return str(model_to_dict(self))
    
class Indicador(models.Model):
    nome = models.CharField(max_length=50)
    tipo_de_tempo_limite = models.CharField(max_length=10)
    tempo_limite = models.PositiveIntegerField()
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)

    def __str__(self):
        return str(model_to_dict(self))