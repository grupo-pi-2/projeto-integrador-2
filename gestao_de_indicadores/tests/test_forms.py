from django.test import TestCase
from django import forms
from gestao_de_indicadores.models import Servico
from gestao_de_indicadores.forms import ServicoForm, ClienteForm

from gestao_de_indicadores.models import Cliente, Indicador, Setor
from django.contrib.auth.models import User
from datetime import datetime

class ServicoFormTestCase(TestCase):
  def test_servico_form_structure(self):
    form = ServicoForm()
    
    self.assertIsInstance(form, forms.ModelForm)
    self.assertEqual(form.Meta.model, Servico)
    self.assertEqual(form.Meta.fields, ['cliente', 'data_hora_inicio', 'data_hora_fim', 'indicador', 'setor', 'status', 'periodo', 'responsavel'])
    
    self.assertIsInstance(form.fields['data_hora_inicio'].widget, forms.DateTimeInput)    
    self.assertIsInstance(form.fields['data_hora_fim'].widget, forms.DateTimeInput)

    self.assertEqual(form.fields['cliente'].label, 'Cliente')
    self.assertEqual(form.fields['data_hora_inicio'].label, 'Data/Hora Início')
    self.assertEqual(form.fields['data_hora_fim'].label, 'Data/Hora Fim')
    self.assertEqual(form.fields['indicador'].label, 'Indicador')
    self.assertEqual(form.fields['setor'].label, 'Setor')
    self.assertEqual(form.fields['status'].label, 'Status')
    self.assertEqual(form.fields['periodo'].label, 'Período')
    self.assertEqual(form.fields['responsavel'].label, 'Responsável')
    
  def test_valid_servico_form(self):
    setor = Setor.objects.create(nome="Setor")
    cliente = Cliente.objects.create(razao_social="Cliente Teste")
    indicador = Indicador.objects.create(nome="Indicador", tipo_de_tempo_limite="horas", tempo_limite=5, indicador_geral=False, setor=setor)
    responsavel = User.objects.create_user(username="Maria")

    form_data = {
      'cliente': cliente.id,
      'data_hora_inicio': datetime(2024, 11, 1, 0, 0),
      'data_hora_fim': datetime(2024, 11, 1, 1, 0),
      'indicador': indicador.id,
      'setor': setor.id,
      'status': 'PEN',
      'periodo': '11/2024',
      'responsavel': responsavel.id,
    }
    form = ServicoForm(data=form_data)

    self.assertTrue(form.is_valid())
    
    
  def test_invalid_servico_form(self):
    form = ServicoForm({})
    
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors, {
      'cliente': ['This field is required.'],
      'data_hora_inicio': ['This field is required.'],
      'data_hora_fim': ['This field is required.'],
      'indicador': ['This field is required.'],
      'setor': ['This field is required.'],
      'status': ['This field is required.'],
      'periodo': ['This field is required.'],
      'responsavel': ['This field is required.'],
    })
    
class ClienteFormTestCase(TestCase):
  def test_cliente_form_structure(self):
    form = ClienteForm()
    
    self.assertIsInstance(form, forms.ModelForm)
    self.assertEqual(form.Meta.model, Cliente)
    self.assertEqual(form.Meta.fields, ['cnpj', 'razao_social'])
    
    self.assertEqual(form.fields['cnpj'].label, 'CNPJ')
    self.assertEqual(form.fields['razao_social'].label, 'Razão Social')
    
  def test_valid_cliente_form(self):
    form_data = {
      'cnpj': '12345678901234',
      'razao_social': 'Cliente Teste',
    }
    form = ClienteForm(data=form_data)

    self.assertTrue(form.is_valid())
    
  def test_invalid_cliente_form(self):
    form = ClienteForm({})
    
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors, {
      'cnpj': ['This field is required.'],
      'razao_social': ['This field is required.'],
    })