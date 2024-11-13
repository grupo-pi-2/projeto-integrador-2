from django import forms
from .models import Servico, Cliente

class ServicoForm(forms.ModelForm):
    class Meta:
      model = Servico
      fields = ['cliente', 'data_hora_inicio', 'data_hora_fim', 'indicador', 'setor', 'status', 'periodo', 'responsavel']
      widgets = {
        'data_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        'data_hora_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
      }
      labels = {
        'cliente': 'Cliente',
        'data_hora_inicio': 'Data/Hora Início',
        'data_hora_fim': 'Data/Hora Fim',
        'indicador': 'Indicador',
        'setor': 'Setor',
        'status': 'Status',
        'periodo': 'Período',
        'responsavel': 'Responsável',
      }

class ClienteForm(forms.ModelForm):
    class Meta:
      model = Cliente
      fields = ['cnpj', 'razao_social']
      labels = {
        'cnpj': 'CNPJ',
        'razao_social': 'Razão Social',
      }