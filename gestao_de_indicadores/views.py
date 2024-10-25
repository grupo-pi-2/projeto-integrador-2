from django.http import HttpResponse
from django.template import loader

from .models import Indicador

# Create your views here.
def index(request):
  indicadores = Indicador.objects.all().order_by("created_at")
  template = loader.get_template("gestao_de_indicadores/index.html")
  context = { "indicadores": indicadores }
  return HttpResponse(template.render(context, request))