from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from django.conf import settings

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
    indicador_geral = models.BooleanField(default=False)
    indicador_pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subindicadores')
    ordenacao = models.IntegerField(default=1)

    def __str__(self):
        return str(model_to_dict(self))

    def is_auditorias(self):
        return self.nome == "Auditorias"

    def is_painel_kpi(self):
        return self.nome == "Painel KPI"
    
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
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='servicos',
    )

    def __str__(self):
        return str(model_to_dict(self))
    
    def tempo_total_formatado(self):
        total = self.data_hora_fim - self.data_hora_inicio
        total_segundos = total.total_seconds()
        horas = int(total_segundos // 3600)
        minutos = int((total_segundos % 3600) // 60)
        return f"{horas:02}:{minutos:02}"

    def tempo_total_em_segundos(self):
        total = self.data_hora_fim - self.data_hora_inicio
        return total.total_seconds()

    def dias_total_formatado(self):
        total = self.data_hora_fim - self.data_hora_inicio
        return f"{total.days}"

    def dias_total(self):
        total = self.data_hora_fim - self.data_hora_inicio
        return total.days
    