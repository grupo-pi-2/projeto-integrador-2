from django.http import HttpResponse, JsonResponse
from .forms import ServicoForm, ClienteForm
from django.shortcuts import render, redirect
from django.template import loader
from datetime import datetime

from .models import Indicador, Cliente, Servico

# Create your views here.
def index(request):
  data_atual = datetime.now()
  periodo_padrao = data_atual.strftime('%m/%Y')
  periodo = request.GET.get('periodo') or periodo_padrao

  indicadores = Indicador.objects.all().order_by("created_at")
  indicador_auditoria = Indicador.objects.get(nome="Auditorias")
  servicos = indicador_auditoria.servicos.filter(periodo=periodo)

  qtde_servicos_programados = servicos.count()
  qtde_servicos_concluidos = servicos.filter(status='CON').count()
  media_em_percentual = round(qtde_servicos_concluidos / qtde_servicos_programados, 2) * 100 if qtde_servicos_programados > 0 else 0
  tempo_total_servicos = sum(servico.tempo_total_em_segundos() for servico in servicos)
  media_tempo_servicos = tempo_total_servicos / qtde_servicos_concluidos if qtde_servicos_concluidos and tempo_total_servicos > 0 else 0
  media_tempo_em_horas_servicos = (media_tempo_servicos / 3600) if media_tempo_servicos > 0 else 0
  media_tempo_em_minutos_servicos = int(media_tempo_servicos % 3600 // 60) if media_tempo_servicos > 0 else 0
  media_tempo_em_horas_e_minutos_servicos = f"{int(media_tempo_em_horas_servicos):02}:{media_tempo_em_minutos_servicos:02}"
  percentual_horas_concluidos = round(media_tempo_em_horas_servicos / indicador_auditoria.tempo_limite, 2) * 100 if indicador_auditoria.tempo_limite > 0 else 0

  mes_atual, ano_atual = map(int, periodo.split('/'))
  periodos_do_ano = []
  for mes in range(mes_atual, 0, -1):
    periodos_do_ano.append(f'{mes:02d}/{ano_atual}')

  qtde_servicos_concluidos_no_ano = 0
  for periodo_acumulado in periodos_do_ano:
    qtde_servicos_concluidos = indicador_auditoria.servicos.filter(periodo=periodo_acumulado, status='CON').count()
    qtde_servicos_concluidos_no_ano += qtde_servicos_concluidos

  metricas = {
    'programados': qtde_servicos_programados,
    'concluidos': qtde_servicos_concluidos,
    'percentual_concluidos': media_em_percentual,
    'media_em_horas': media_tempo_em_horas_e_minutos_servicos,
    'percentual_horas_concluidos': percentual_horas_concluidos,
    'qtde_servicos_concluidos_no_ano': qtde_servicos_concluidos_no_ano,
  }

  template = loader.get_template("gestao_de_indicadores/index.html")
  context = { "indicadores": indicadores, "indicador_auditoria": indicador_auditoria, "servicos": servicos, "metricas": metricas }
  return HttpResponse(template.render(context, request))

def busca_indicador(request, indicador_id):
  data_atual = datetime.now()
  periodo_padrao = data_atual.strftime('%m/%Y')
  periodo = request.GET.get('periodo') or periodo_padrao

  indicador = Indicador.objects.get(id=indicador_id)

  if indicador.indicador_geral:
    mes_atual, ano_atual = map(int, periodo.split('/'))
    periodos_do_ano = []
    for mes in range(mes_atual, 0, -1):
      periodos_do_ano.append(f'{mes:02d}/{ano_atual}')

    subindicadores = indicador.subindicadores.all().order_by("created_at")
    subindicadores_servicos = []
    for subindicador in subindicadores:
      qtde_servicos_concluidos_no_ano = 0
      for periodo_acumulado in periodos_do_ano:
        qtde_servicos_concluidos = subindicador.servicos.filter(periodo=periodo_acumulado, status='CON').count()
        qtde_servicos_concluidos_no_ano += qtde_servicos_concluidos

      servicos = subindicador.servicos.filter(periodo=periodo)
      servicos_concluidos = servicos.filter(status='CON')
      
      qtde_servicos_concluidos = servicos_concluidos.count()
      qtde_servicos_total = servicos.count()
      percentual_servicos_concluidos = round(qtde_servicos_concluidos / qtde_servicos_total, 2) * 100 if qtde_servicos_total > 0 else 0
      
      tempo_total_servicos = sum(servico.tempo_total_em_segundos() for servico in servicos_concluidos)
      media_tempo_servicos = tempo_total_servicos / qtde_servicos_concluidos if qtde_servicos_concluidos and tempo_total_servicos > 0 else 0
      media_tempo_em_horas_servicos = (media_tempo_servicos / 3600) if media_tempo_servicos > 0 else 0
      media_tempo_em_minutos_servicos = int(media_tempo_servicos % 3600 // 60) if media_tempo_servicos > 0 else 0
      media_tempo_em_horas_e_minutos_servicos = f"{int(media_tempo_em_horas_servicos):02}:{media_tempo_em_minutos_servicos:02}"
      percentual_tempo_em_horas_servicos = round(media_tempo_em_horas_servicos / subindicador.tempo_limite, 2) * 100 if subindicador.tempo_limite > 0 else 0

      dias_total_servicos = sum(servico.dias_total() for servico in servicos_concluidos)
      media_dias_servicos = dias_total_servicos / qtde_servicos_concluidos if qtde_servicos_concluidos and dias_total_servicos > 0 else 0
      percentual_dias_servicos = round((media_dias_servicos * 100) / subindicador.tempo_limite, 2) if subindicador.tempo_limite and media_dias_servicos > 0 else 0

      subindicadores_servicos.append({
        'indicador': subindicador,
        'qtde_servicos_concluidos': qtde_servicos_concluidos,
        'qtde_servicos_total': qtde_servicos_total,
        'percentual_servicos_concluidos': percentual_servicos_concluidos,
        'media_tempo_em_horas_servicos': media_tempo_em_horas_e_minutos_servicos,
        'media_dias_servicos': int(media_dias_servicos),
        'percentual_tempo_em_horas_servicos': percentual_tempo_em_horas_servicos,
        'percentual_dias_servicos': percentual_dias_servicos,
        'qtde_servicos_concluidos_no_ano': qtde_servicos_concluidos_no_ano
      })
    data = {'indicador': indicador, 'subindicadores': subindicadores_servicos}
  else:
    servicos = indicador.servicos.filter(periodo=periodo)

    qtde_servicos_programados = servicos.count()
    qtde_servicos_concluidos = servicos.filter(status='CON').count()
    media_em_percentual = round(qtde_servicos_concluidos / qtde_servicos_programados, 2) * 100 if qtde_servicos_programados > 0 else 0
    tempo_total_servicos = sum(servico.tempo_total_em_segundos() for servico in servicos)
    media_tempo_servicos = tempo_total_servicos / qtde_servicos_concluidos if qtde_servicos_concluidos and tempo_total_servicos > 0 else 0
    media_tempo_em_horas_servicos = (media_tempo_servicos / 3600) if media_tempo_servicos > 0 else 0
    media_tempo_em_minutos_servicos = int(media_tempo_servicos % 3600 // 60) if media_tempo_servicos > 0 else 0
    media_tempo_em_horas_e_minutos_servicos = f"{int(media_tempo_em_horas_servicos):02}:{media_tempo_em_minutos_servicos:02}"
    percentual_horas_concluidos = round(media_tempo_em_horas_servicos / indicador.tempo_limite, 2) * 100 if indicador.tempo_limite > 0 else 0
  
    dias_total_servicos = sum(servico.dias_total() for servico in servicos)
    media_dias_servicos = dias_total_servicos / qtde_servicos_concluidos if qtde_servicos_concluidos and dias_total_servicos > 0 else 0
    percentual_dias_servicos = round((media_dias_servicos * 100) / indicador.tempo_limite, 2) if indicador.tempo_limite and media_dias_servicos > 0 else 0

    mes_atual, ano_atual = map(int, periodo.split('/'))
    periodos_do_ano = []
    for mes in range(mes_atual, 0, -1):
      periodos_do_ano.append(f'{mes:02d}/{ano_atual}')

    qtde_servicos_concluidos_no_ano = 0
    for periodo_acumulado in periodos_do_ano:
      qtd_servicos_concluidos = indicador.servicos.filter(periodo=periodo_acumulado, status='CON').count()
      qtde_servicos_concluidos_no_ano += qtd_servicos_concluidos

    metricas = {
      'programados': qtde_servicos_programados,
      'concluidos': qtde_servicos_concluidos,
      'percentual_concluidos': media_em_percentual,
      'media_em_horas': media_tempo_em_horas_e_minutos_servicos,
      'percentual_horas_concluidos': percentual_horas_concluidos,
      'qtde_servicos_concluidos_no_ano': qtde_servicos_concluidos_no_ano,
      'media_em_dias': media_dias_servicos,
      'percentual_dias_concluidos': percentual_dias_servicos,
    }

    data = {'indicador': indicador, 'servicos': servicos, 'metricas': metricas}
  
  html = render(request, 'gestao_de_indicadores/indicador.html', data)
  return HttpResponse(html.content, content_type='text/html')

def lista_clientes(request):
  clientes = Cliente.objects.all()
  clientes_mapeados = [{"id": cliente.id, "razao_social": f"{cliente.cnpj} - {cliente.razao_social}"} for cliente in clientes]
  return JsonResponse(clientes_mapeados, safe=False, content_type='application/json')

def lista_status_servico(request):
  statuses = Servico.Status.choices
  status_mapeados = [{"id": status[0], "descricao": status[1]} for status in statuses]
  return JsonResponse(status_mapeados, safe=False, content_type='application/json')

def cria_servico(request):
  if request.method == 'POST':
    form = ServicoForm(request.POST)

    if form.is_valid():
      form.save()
      return JsonResponse({'success': True, 'indicador': request.POST['indicador']})
    else:
      errors = {form.fields[field_name].label: messages for field_name, messages in form.errors.items()}
      return JsonResponse({'success': False, 'errors': errors })
  else :
    redirect('index')

def exclui_servico(request, servico_id):
  servico = Servico.objects.get(id=servico_id)
  
  if request.method == 'DELETE':
    servico.delete()
    return JsonResponse({'success': True, 'indicador': servico.indicador_id})
  
def busca_servico(request, servico_id):
  servico = Servico.objects.get(id=servico_id)
  servico_mapeado = {
    "id": servico.id,
    "cliente_id": servico.cliente_id,
    "data_hora_inicio": servico.data_hora_inicio,
    "data_hora_fim": servico.data_hora_fim,
    "status": servico.status,
    "periodo": servico.periodo
  }
  return JsonResponse(servico_mapeado, safe=False, content_type='application/json')

def atualiza_servico(request, servico_id):
  if request.method == 'POST':
    servico = Servico.objects.get(id=servico_id)
    form = ServicoForm(request.POST, instance=servico)
    
    if form.is_valid():
      form.save()
      return JsonResponse({'success': True, 'indicador': request.POST['indicador']})
    else:
      errors = {form.fields[field_name].label: messages for field_name, messages in form.errors.items()}
      return JsonResponse({'success': False, 'errors': errors })
  else :
    redirect('index')

def clientes(request):
  clientes = Cliente.objects.all()
  template = loader.get_template("gestao_de_indicadores/clientes.html")
  context = { "clientes": clientes }
  return HttpResponse(template.render(context, request))

def cria_cliente(request):
  if request.method == 'POST':
    form = ClienteForm(request.POST)

    if form.is_valid():
      form.save()
      return JsonResponse({'success': True})
    else:
      errors = {form.fields[field_name].label: messages for field_name, messages in form.errors.items()}
      return JsonResponse({'success': False, 'errors': errors })
  else :
    redirect('clientes')

def busca_cliente(request, cliente_id):
  cliente = Cliente.objects.get(id=cliente_id)
  cliente_mapeado = {
    "id": cliente.id,
    "cnpj": cliente.cnpj,
    "razao_social": cliente.razao_social,
  }
  return JsonResponse(cliente_mapeado, safe=False, content_type='application/json')

def atualiza_cliente(request, cliente_id):
  if request.method == 'POST':
    cliente = Cliente.objects.get(id=cliente_id)
    form = ClienteForm(request.POST, instance=cliente)
    
    if form.is_valid():
      form.save()
      return JsonResponse({'success': True})
    else:
      errors = {form.fields[field_name].label: messages for field_name, messages in form.errors.items()}
      return JsonResponse({'success': False, 'errors': errors })
  else :
    redirect('clientes')

def exclui_cliente(request, cliente_id):
  cliente = Cliente.objects.get(id=cliente_id)
  
  if request.method == 'DELETE':
    cliente.delete()
    return JsonResponse({'success': True})
  

