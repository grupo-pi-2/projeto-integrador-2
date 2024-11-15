from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from gestao_de_indicadores.models import Indicador, Setor, Cliente
from gestao_de_indicadores.services.metricas_indicador import MetricasIndicador
from django.contrib.auth.models import User

class MetricasIndicadorTest(TestCase):
  def setUp(self):
    setor = Setor.objects.create(nome="Setor")
    cliente = Cliente.objects.create(razao_social="Cliente Teste")
    responsavel = User.objects.create(username="user", is_superuser=False, is_staff=False)

    self.indicador_horas = Indicador.objects.create(
      nome="Indicador Horas",
      tipo_de_tempo_limite='horas',
      tempo_limite=8,
      setor=setor
    )

    self.indicador_dias = Indicador.objects.create(
      nome="Indicador Dias",
      tipo_de_tempo_limite='dias',
      tempo_limite=5,
      setor=setor
    )
    
    self.periodo = "11/2024"
    
    # Serviços indicador de horas
    self.indicador_horas.servicos.create(
      cliente=cliente,
      data_hora_inicio=datetime(2024, 11, 1, 0, 0),
      data_hora_fim=datetime(2024, 11, 1, 5, 0),
      setor=setor,
      status="CON",
      periodo="11/2024",
      responsavel=responsavel
    )

    self.indicador_horas.servicos.create(
      cliente=cliente,
      data_hora_inicio=datetime(2024, 11, 1, 0, 0),
      data_hora_fim=datetime(2024, 11, 1, 3, 0),
      setor=setor,
      status="CON",
      periodo="11/2024",
      responsavel=responsavel
    )
    
    self.indicador_horas.servicos.create(
      cliente=cliente,
      data_hora_inicio=datetime(2024, 11, 1, 0, 0),
      data_hora_fim=datetime(2024, 11, 1, 3, 0),
      setor=setor,
      status="PEN",
      periodo="11/2024",
      responsavel=responsavel
    )
      
    # Serviços indicador de dias
    self.indicador_dias.servicos.create(
      cliente=cliente,
      data_hora_inicio=datetime(2024, 11, 1, 0, 0),
      data_hora_fim=datetime(2024, 11, 2, 0, 0),
      setor=setor,
      status="CON",
      periodo="11/2024",
      responsavel=responsavel
    )
    
    self.indicador_dias.servicos.create(
      cliente=cliente,
      data_hora_inicio=datetime(2024, 11, 1, 0, 0),
      data_hora_fim=datetime(2024, 11, 4, 0, 0),
      setor=setor,
      status="CON",
      periodo="11/2024",
      responsavel=responsavel
    )
    
    self.indicador_dias.servicos.create(
      cliente=cliente,
      data_hora_inicio=datetime(2024, 11, 1, 0, 0),
      data_hora_fim=datetime(2024, 11, 2, 0, 0),
      setor=setor,
      status="PEN",
      periodo="11/2024",
      responsavel=responsavel
    )

  def test_gerar_indicadores_em_horas(self):
    metricas = MetricasIndicador(self.indicador_horas, self.indicador_horas.servicos, self.periodo)
    resultado = metricas.gerar()
    self.assertEqual(resultado['indicador'], self.indicador_horas)
    self.assertEqual(resultado['qtde_servicos_programados'], 3)
    self.assertEqual(resultado['qtde_servicos_concluidos'], 2)
    self.assertEqual(resultado['percentual_servicos_concluidos'], 67.0)
    self.assertEqual(resultado['tempo_medio_servicos_concluidos'], '04:00')
    self.assertEqual(resultado['percentual_tempo_servicos_concluidos'], 50.0)
    self.assertEqual(resultado['qtde_servicos_concluidos_no_ano'], 2)
      
  def test_gerar_indicadores_em_dias(self):
    metricas = MetricasIndicador(self.indicador_dias, self.indicador_dias.servicos, self.periodo)
    resultado = metricas.gerar()
    self.assertEqual(resultado['indicador'], self.indicador_dias)
    self.assertEqual(resultado['qtde_servicos_programados'], 3)
    self.assertEqual(resultado['qtde_servicos_concluidos'], 2)
    self.assertEqual(resultado['percentual_servicos_concluidos'], 67.0)
    self.assertEqual(resultado['tempo_medio_servicos_concluidos'], '2.0')
    self.assertEqual(resultado['percentual_tempo_servicos_concluidos'], 40.0)
    self.assertEqual(resultado['qtde_servicos_concluidos_no_ano'], 2)
