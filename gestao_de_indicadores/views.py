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
  template = loader.get_template("gestao_de_indicadores/index.html")
  context = { "indicadores": indicadores, "indicador_auditoria": indicador_auditoria, "servicos": servicos }
  return HttpResponse(template.render(context, request))

def busca_indicador(request, indicador_id):
  data_atual = datetime.now()
  periodo_padrao = data_atual.strftime('%m/%Y')
  periodo = request.GET.get('periodo') or periodo_padrao

  indicador = Indicador.objects.get(id=indicador_id)
  servicos = indicador.servicos.filter(periodo=periodo)
  html = render(request, 'gestao_de_indicadores/indicador.html', {'indicador': indicador, 'servicos': servicos})
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
  

