from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from gestao_de_indicadores.models import Indicador, Cliente, Setor
from django.contrib.auth.models import User

class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("index")

        setor = Setor.objects.create(nome="Setor")
        cliente = Cliente.objects.create(razao_social="Cliente Teste")
        responsavel = User.objects.create(username="user", is_superuser=False, is_staff=False)
        indicador = Indicador.objects.get(nome="Auditorias")
        indicador.servicos.create(cliente=cliente, data_hora_inicio=datetime(2024, 11, 1, 0, 0), data_hora_fim=datetime(2024, 11, 2, 1, 0), indicador=indicador, setor=setor, status="CON", periodo="01/2024", responsavel=responsavel)

    def test_index_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("indicadores", response.context)
        self.assertIn("indicador_auditoria", response.context)
        self.assertIn("servicos", response.context)
        self.assertIn("metricas", response.context)
        self.assertIn("clientes", response.context)
        self.assertIn("responsaveis", response.context)

class BuscaIndicadorTestCase(TestCase):
    def setUp(self):
        setor = Setor.objects.create(nome="Setor")
        cliente = Cliente.objects.create(razao_social="Cliente Teste")
        responsavel = User.objects.create(username="user", is_superuser=False, is_staff=False)
        self.indicador = Indicador.objects.get(nome="Auditorias")
        self.indicador.servicos.create(cliente=cliente, data_hora_inicio=datetime(2024, 11, 1, 0, 0), data_hora_fim=datetime(2024, 11, 2, 1, 0), setor=setor, status="CON", periodo="01/2024", responsavel=responsavel)
        self.indicador_geral = Indicador.objects.get(nome="Painel KPI", indicador_geral=True)

        self.client = Client()

    def test_busca_indicador_view(self):
        url = reverse("busca_indicador", args=[self.indicador.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("indicador", response.context)
        self.assertIn("servicos", response.context)

    def test_busca_indicador_geral_view(self):
        url = reverse("busca_indicador", args=[self.indicador_geral.id])
        response = self.client.get(url)

        self.assertIn("indicador", response.context)
        self.assertIn("subindicadores", response.context)

class ListaClientesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("lista_clientes")

        self.cliente = Cliente.objects.create(razao_social="Cliente Teste", cnpj="12345678000195")

    def test_lista_clientes_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        clientes_mapeados = response.json()
        self.assertEqual(len(clientes_mapeados), 1)
        self.assertEqual(clientes_mapeados[0]["razao_social"], "12345678000195 - Cliente Teste")
        self.assertEqual(clientes_mapeados[0]["id"], self.cliente.id)
        
class ListaStatusServicoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("lista_status_servico")

    def test_lista_status_servico_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        status = response.json()
        self.assertEqual(len(status), 3)
        self.assertEqual(status[0]["id"], "CON")
        self.assertEqual(status[0]["descricao"], "Concluído")
        self.assertEqual(status[1]["id"], "PEN")
        self.assertEqual(status[1]["descricao"], "Pendente")
        self.assertEqual(status[2]["id"], "CAN")
        self.assertEqual(status[2]["descricao"], "Cancelado")

class ListaResponsaveisTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("lista_responsaveis")

        self.user = User.objects.create_user(username="Maria", first_name="Maria")

    def test_lista_responsaveis_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        responsaveis = response.json()
        self.assertEqual(len(responsaveis), 1)
        self.assertEqual(responsaveis[0]["nome"], "Maria")
        self.assertEqual(responsaveis[0]["id"], self.user.id)
        
class CriaServicoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("cria_servico")

        setor = Setor.objects.create(nome="Setor")
        cliente = Cliente.objects.create(razao_social="Cliente Teste")
        responsavel = User.objects.create(username="user", is_superuser=False, is_staff=False)
        indicador = Indicador.objects.get(nome="Auditorias")

        self.data = {
            "cliente": cliente.id,
            "data_hora_inicio": "2024-11-01T00:00",
            "data_hora_fim": "2024-11-02T01:00",
            "indicador": indicador.id,
            "setor": setor.id,
            "status": "CON",
            "periodo": "01/2024",
            "responsavel": responsavel.id
        }

    def test_cria_servico_view(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        servico = response.json()
        self.assertEqual(servico["success"], True)
        self.assertEqual(servico["indicador"], str(self.data["indicador"]))
        
    def test_cria_servico_invalido_view(self):
        self.data["cliente"] = ""
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        servico = response.json()
        self.assertEqual(servico["success"], False)
        self.assertEqual(len(servico["errors"]), 1)
        self.assertEqual(servico["errors"], { "Cliente": ["This field is required."] })

class ExcluiServicoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        setor = Setor.objects.create(nome="Setor")
        cliente = Cliente.objects.create(razao_social="Cliente Teste")
        responsavel = User.objects.create(username="user", is_superuser=False, is_staff=False)
        self.indicador = Indicador.objects.get(nome="Auditorias")
        servico = self.indicador.servicos.create(cliente=cliente, data_hora_inicio=datetime(2024, 11, 1, 0, 0), data_hora_fim=datetime(2024, 11, 2, 1, 0), setor=setor, status="CON", periodo="01/2024", responsavel=responsavel)

        self.url = reverse("exclui_servico", args=[servico.id])

    def test_exclui_servico_view(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        servico = response.json()
        self.assertEqual(servico["success"], True)
        self.assertEqual(servico["indicador"], self.indicador.id)
        
class BuscaServicoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        setor = Setor.objects.create(nome="Setor")
        self.cliente = Cliente.objects.create(razao_social="Cliente Teste")
        self.responsavel = User.objects.create(username="user", is_superuser=False, is_staff=False)
        indicador = Indicador.objects.get(nome="Auditorias")
        self.servico = indicador.servicos.create(cliente=self.cliente, data_hora_inicio=datetime(2024, 11, 1, 0, 0), data_hora_fim=datetime(2024, 11, 2, 1, 0), indicador=indicador, setor=setor, status="CON", periodo="01/2024", responsavel=self.responsavel)

        self.url = reverse("busca_servico", args=[self.servico.id])

    def test_busca_servico_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        servico = response.json()
        self.assertEqual(servico["id"], self.servico.id)
        self.assertEqual(servico["cliente_id"], self.cliente.id)
        self.assertEqual(servico["data_hora_inicio"], "2024-11-01T00:00:00Z")
        self.assertEqual(servico["data_hora_fim"], "2024-11-02T01:00:00Z")
        self.assertEqual(servico["status"], "CON")
        self.assertEqual(servico["periodo"], "01/2024")
        self.assertEqual(servico["responsavel_id"], self.responsavel.id)
        
class AtualizaServicoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        setor = Setor.objects.create(nome="Setor")
        cliente = Cliente.objects.create(razao_social="Cliente Teste")
        responsavel = User.objects.create(username="user", is_superuser=False, is_staff=False)
        self.indicador = Indicador.objects.get(nome="Auditorias")
        servico = self.indicador.servicos.create(cliente=cliente, data_hora_inicio=datetime(2024, 11, 1, 0, 0), data_hora_fim=datetime(2024, 11, 2, 1, 0), setor=setor, status="PEN", periodo="01/2024", responsavel=responsavel)

        self.url = reverse("atualiza_servico", args=[servico.id])

        self.data = {
            "cliente": cliente.id,
            "data_hora_inicio": "2024-11-01T00:00",
            "data_hora_fim": "2024-11-02T01:00",
            "indicador": self.indicador.id,
            "setor": setor.id,
            "status": "CON",
            "periodo": "01/2024",
            "responsavel": responsavel.id
        }
        
    def test_atualiza_servico_view(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        servico = response.json()
        self.assertEqual(servico["success"], True)
        self.assertEqual(servico["indicador"], str(self.indicador.id))
        
    def test_atualiza_servico_invalido_view(self):
        self.data["cliente"] = ""
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        servico = response.json()
        self.assertEqual(servico["success"], False)
        self.assertEqual(len(servico["errors"]), 1)
        self.assertEqual(servico["errors"], { "Cliente": ["This field is required."] })
        
class ClientesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("clientes")

        Cliente.objects.create(razao_social="Cliente Teste", cnpj="12345678000195")

    def test_clientes_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("clientes", response.context)

class CriaClienteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("cria_cliente")

        self.data = {
            "razao_social": "Cliente Teste",
            "cnpj": "12345678000195"
        }

    def test_cria_cliente_view(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        cliente = response.json()        
        self.assertEqual(cliente["success"], True)
        
    def test_cria_cliente_invalido_view(self):
        self.data["razao_social"] = ""
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        cliente = response.json()
        self.assertEqual(cliente["success"], False)
        self.assertEqual(len(cliente["errors"]), 1)
        self.assertEqual(cliente["errors"], { "Razão Social": ["This field is required."] })

class BuscaClienteTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.cliente = Cliente.objects.create(razao_social="Cliente", cnpj="12345678901234")
        
    def test_busca_cliente_view(self):
        url = reverse("busca_cliente", args=[self.cliente.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        cliente = response.json()
        self.assertEqual(cliente["id"], self.cliente.id)
        self.assertEqual(cliente["cnpj"], "12345678901234")
        self.assertEqual(cliente["razao_social"], "Cliente")
        
class AtualizaClienteTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.cliente = Cliente.objects.create(razao_social="Cliente", cnpj="12345678901234")

        self.url = reverse("atualiza_cliente", args=[self.cliente.id])

        self.data = {
            "razao_social": "Cliente Teste",
            "cnpj": "12345678901234"
        }
        
    def test_atualiza_cliente_view(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        cliente = response.json()
        self.assertEqual(cliente["success"], True)
        
    def test_atualiza_cliente_invalido_view(self):
        self.data["razao_social"] = ""
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        cliente = response.json()
        self.assertEqual(cliente["success"], False)
        self.assertEqual(len(cliente["errors"]), 1)
        self.assertEqual(cliente["errors"], { "Razão Social": ["This field is required."] })
        
class ExcluiClienteTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        cliente = Cliente.objects.create(razao_social="Cliente", cnpj="12345678901234")

        self.url = reverse("exclui_cliente", args=[cliente.id])

    def test_exclui_cliente_view(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        cliente = response.json()
        self.assertEqual(cliente["success"], True)