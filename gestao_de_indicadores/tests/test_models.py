from django.test import TestCase

from gestao_de_indicadores.models import Setor, Indicador, Cliente, Servico
from django.contrib.auth.models import User
from datetime import datetime, timezone

class SetorTestCase(TestCase):
  def setUp(self):
    Setor.objects.create(nome="Setor")

  def test_setor_str(self):
    setor = Setor.objects.get(nome="Setor")
    self.assertEqual(str(setor), str({ 'id': setor.id, 'nome': "Setor" }))
  
  def test_setor_nome(self):
    setor = Setor.objects.get(nome="Setor")
    self.assertEqual(setor.nome, "Setor")

class IndicadorTestCase(TestCase):
  def setUp(self):
    setor = Setor.objects.create(nome="Setor")
    Indicador.objects.create(nome="Indicador", tipo_de_tempo_limite="horas", tempo_limite=5, indicador_geral=True, setor=setor)

  def test_indicador_str(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(str(indicador), str({
      'id': indicador.id,
      'nome': "Indicador",
      'tipo_de_tempo_limite': "horas",
      'tempo_limite': 5,
      'setor': indicador.setor_id,
      'indicador_geral': True,
      'indicador_pai': None,
      'ordenacao': 1,
    }))
  
  def test_indicador_nome(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.nome, "Indicador")
    
  def test_indicador_tipo_de_tempo_limite(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.tipo_de_tempo_limite, "horas")
    
  def test_indicador_tempo_limite(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.tempo_limite, 5)
    
  def test_indicador_setor(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.setor.nome, "Setor")
    
  def test_indicador_indicador_geral(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.indicador_geral, True)
    
  def test_indicador_indicador_pai(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.indicador_pai, None)
    
  def test_indicador_ordenacao(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.ordenacao, 1)
    
  def test_indicador_is_auditorias(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.is_auditorias(), False)
    
  def test_indicador_is_painel_kpi(self):
    indicador = Indicador.objects.get(nome="Indicador")
    self.assertEqual(indicador.is_painel_kpi(), False)

class ClienteTestCase(TestCase):
  def setUp(self):
    Cliente.objects.create(razao_social="Cliente", cnpj="12345678901234")

  def test_cliente_str(self):
    cliente = Cliente.objects.get(razao_social="Cliente")
    self.assertEqual(str(cliente), str({ 'id': cliente.id, 'razao_social': "Cliente", 'cnpj': "12345678901234" }))
  
  def test_cliente_razao_social(self):
    cliente = Cliente.objects.get(razao_social="Cliente")
    self.assertEqual(cliente.razao_social, "Cliente")
    
  def test_cliente_cnpj(self):
    cliente = Cliente.objects.get(razao_social="Cliente")
    self.assertEqual(cliente.cnpj, "12345678901234")
    
class ServicoTestCase(TestCase):
  def setUp(self):
    setor = Setor.objects.create(nome="Setor")
    indicador = Indicador.objects.create(nome="Indicador", tipo_de_tempo_limite="horas", tempo_limite=5, indicador_geral=True, setor=setor)
    cliente = Cliente.objects.create(razao_social="Cliente", cnpj="12345678901234")
    responsavel =  User.objects.create_user(username="Maria")
    Servico.objects.create(cliente=cliente, data_hora_inicio=datetime(2024, 11, 1, 0, 0, tzinfo=timezone.utc), data_hora_fim=datetime(2024, 11, 2, 1, 0, tzinfo=timezone.utc), indicador=indicador, setor=setor, status="CON", periodo="11/2024", responsavel=responsavel)

  def test_servico_str(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(str(servico), str({
      'id': servico.id,
      'cliente': servico.cliente_id,
      'data_hora_inicio': servico.data_hora_inicio,
      'data_hora_fim': servico.data_hora_fim,
      'indicador': servico.indicador_id,
      'setor': servico.setor_id,
      'status': "CON",
      'periodo': "11/2024",
      'responsavel': servico.responsavel_id
    }))
  
  def test_servico_cliente(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.cliente.razao_social, "Cliente")
    
  def test_servico_data_hora_inicio(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.data_hora_inicio.isoformat().replace('+00:00', 'Z'), '2024-11-01T00:00:00Z')
    
  def test_servico_data_hora_fim(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.data_hora_fim.isoformat().replace('+00:00', 'Z'), '2024-11-02T01:00:00Z')
    
  def test_servico_indicador(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.indicador.nome, "Indicador")
    
  def test_servico_setor(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.setor.nome, "Setor")
    
  def test_servico_status(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.status, "CON")
    
  def test_servico_periodo(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.periodo, "11/2024")
    
  def test_servico_responsavel(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.responsavel.username, "Maria")
    
  def test_tempo_total_formatado(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.tempo_total_formatado(), "25:00")
    
  def test_tempo_total_em_segundos(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.tempo_total_em_segundos(), 90000.0)
    
  def test_dias_total_formatado(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.dias_total_formatado(), "1")
    
  def test_dias_total(self):
    servico = Servico.objects.get(cliente__razao_social="Cliente")
    self.assertEqual(servico.dias_total(), 1)