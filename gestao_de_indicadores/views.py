from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Indicador

# Create your views here.
def index(request):
  indicadores = Indicador.objects.all().order_by("created_at")
  indicador_auditoria = Indicador.objects.get(nome="Auditorias")
  template = loader.get_template("gestao_de_indicadores/index.html")
  context = { "indicadores": indicadores, "indicador_auditoria": indicador_auditoria }
  return HttpResponse(template.render(context, request))

def busca_indicador(request, indicador_id):
  indicador = Indicador.objects.get(id=indicador_id)
  html = render(request, 'gestao_de_indicadores/indicador.html', {'indicador': indicador})
  return HttpResponse(html.content, content_type='text/html')
