class MetricasIndicador:
  def __init__(self, indicador, servicos, periodo):
    self.indicador = indicador
    self.servicos = servicos
    self.periodo = periodo

  def gerar(self):
    return { 
      'qtde_servicos_programados': self._qtde_servicos_programados(),
      'qtde_servicos_concluidos': self._qtde_servicos_concluidos(),
      'percentual_servicos_concluidos': self._percentual_servicos_concluidos(),
      'tempo_medio_servicos_concluidos': self._tempo_medio_servicos_concluidos(),
      'percentual_tempo_servicos_concluidos': self._percentual_tempo_servicos_concluidos(),
      'qtde_servicos_concluidos_no_ano': self._qtde_servicos_concluidos_no_ano()
    }
  
  def _servicos_concluidos(self):
    return self.servicos.filter(status='CON')

  def _qtde_servicos_programados(self):
    return self.servicos.count()

  def _qtde_servicos_concluidos(self):
    return self._servicos_concluidos().count()

  def _percentual_servicos_concluidos(self):
    if self._qtde_servicos_programados() and self._qtde_servicos_concluidos() > 0:
      return round(self._qtde_servicos_concluidos() / self._qtde_servicos_programados(), 2) * 100
    
    return 0
  
  def _tempo_total_em_segundos_servicos_concluidos(self):
    return sum(servico.tempo_total_em_segundos() for servico in self._servicos_concluidos())
  
  def _tempo_medio_em_segundos_servicos_concluidos(self):
    if self._qtde_servicos_concluidos() and self._tempo_total_em_segundos_servicos_concluidos() > 0:
      return self._tempo_total_em_segundos_servicos_concluidos() / self._qtde_servicos_concluidos()
    
    return 0

  def _tempo_medio_em_horas_e_minutos_servicos_concluidos(self):
    if self._tempo_medio_em_segundos_servicos_concluidos() > 0:
      horas = int(self._tempo_medio_em_segundos_servicos_concluidos() / 3600)
      minutos = int(self._tempo_medio_em_segundos_servicos_concluidos() % 3600 // 60)
      return f"{horas:02}:{minutos:02}"
    
    return '00:00'
  
  def _tempo_total_em_dias_servicos_concluidos(self):
    return sum(servico.dias_total() for servico in self._servicos_concluidos())

  def _tempo_medio_em_dias_servicos_concluidos(self):
    if self._qtde_servicos_concluidos() and self._tempo_total_em_dias_servicos_concluidos() > 0:
      return self._tempo_total_em_dias_servicos_concluidos() / self._qtde_servicos_concluidos()
    
    return 0

  def _tempo_medio_servicos_concluidos(self):
    if self.indicador.tipo_de_tempo_limite == 'horas':
      return f'{self._tempo_medio_em_horas_e_minutos_servicos_concluidos()}'

    if self.indicador.tipo_de_tempo_limite == 'dias':
      return f'{self._tempo_medio_em_dias_servicos_concluidos()}'

  def _percentual_tempo_servicos_concluidos(self):
    if self.indicador.tipo_de_tempo_limite == 'horas':
      if self.indicador.tempo_limite and self._tempo_medio_em_segundos_servicos_concluidos() > 0:
        tempo_limite_em_segundos = self.indicador.tempo_limite * 3600
        return round(self._tempo_medio_em_segundos_servicos_concluidos() / tempo_limite_em_segundos, 2) * 100     
      
      return 0
    
    if self.indicador.tipo_de_tempo_limite == 'dias':
      if self.indicador.tempo_limite and self._tempo_medio_em_dias_servicos_concluidos() > 0:
        return round(self._tempo_medio_em_dias_servicos_concluidos() / self.indicador.tempo_limite, 2) * 100
      
      return 0
    
  def _qtde_servicos_concluidos_no_ano(self):
    qtde_servicos_concluidos_no_ano = 0

    for periodo_acumulado in self._periodos_do_ano():
      qtde_servicos_concluidos = self.servicos.filter(periodo=periodo_acumulado, status='CON').count()
      qtde_servicos_concluidos_no_ano += qtde_servicos_concluidos
    
    return qtde_servicos_concluidos_no_ano

  def _periodos_do_ano(self):
    mes_atual, ano_atual = map(int, self.periodo.split('/'))

    periodos_do_ano = []

    for mes in range(mes_atual, 0, -1):
      periodos_do_ano.append(f'{mes:02d}/{ano_atual}')
    
    return periodos_do_ano