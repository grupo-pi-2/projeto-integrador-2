from django.http import HttpResponse, JsonResponse
from .forms import ServicoForm
from django.shortcuts import render, redirect
from django.template import loader

from .models import Indicador, Cliente, Servico

# Create your views here.
def index(request):
  indicadores = Indicador.objects.all().order_by("created_at")
  indicador_auditoria = Indicador.objects.get(nome="Auditorias")
  servicos = indicador_auditoria.servicos.all()
  template = loader.get_template("gestao_de_indicadores/index.html")
  context = { "indicadores": indicadores, "indicador_auditoria": indicador_auditoria, "servicos": servicos }
  return HttpResponse(template.render(context, request))

def busca_indicador(request, indicador_id):
  indicador = Indicador.objects.get(id=indicador_id)
  servicos = indicador.servicos.all()
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

def salva_servico(request):
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
  
  if request.method == 'POST':
    servico.delete()
    return JsonResponse({'success': True, 'indicador': servico.indicador_id})