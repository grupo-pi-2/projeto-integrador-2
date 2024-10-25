from django.db import models
from django.forms.models import model_to_dict

# Create your models here.
class Setor(models.Model):
    nome = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(model_to_dict(self))
    
class Indicador(models.Model):
    nome = models.CharField(max_length=50)
    tipo_de_tempo_limite = models.CharField(max_length=10)
    tempo_limite = models.PositiveIntegerField()
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(model_to_dict(self))
    
class Cliente(models.Model):
    razao_social = models.CharField(max_length=150, blank=False)
    cnpj = models.CharField(max_length=14, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(model_to_dict(self))

