from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

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

class Servico(models.Model):
    class Status(models.TextChoices):
        CONCLUIDO = 'CON', _('Concluído')
        PENDENTE = 'PEN', _('Pendente')
        CANCELADO = 'CAN', _('Cancelado')

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, related_name='servicos')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=3,
        choices=Status,
        default=Status.PENDENTE,
    )
    periodo = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(model_to_dict(self))