document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('.btn-menu-indicador');
  const indicadorContainer = document.getElementById('indicador-container');
  const selectPeriodo = document.getElementById('periodo-select');

  buttons.forEach(button => {
    button.addEventListener('click', function() {
      buttons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');

      const indicadorId = this.getAttribute('data-indicador-id');
      const periodoSelecionado = selectPeriodo.value || mesAnoAtual();

      fetch(`/busca_indicador/${indicadorId}?periodo=${periodoSelecionado}`)
        .then(response => response.text())
        .then(data => {
          indicadorContainer.innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
    });
  });

  preencherSelectPeriodos();
  
  selectPeriodo.addEventListener('change', function() {
    const botaoIndicadorAtivo = document.querySelector('.btn-menu-indicador.active');
    if (botaoIndicadorAtivo) { botaoIndicadorAtivo.click(); }
  });
});

function preencherSelectPeriodos() {
  const periodos = gerarPeriodos();
  const select = document.getElementById('periodo-select');
  const mesAno = mesAnoAtual();

  periodos.forEach(periodo => {
    const option = document.createElement('option');
    option.value = periodo;
    option.textContent = periodo;
    if (periodo === mesAno) {
      option.selected = true;
    }
    select.appendChild(option);
  });
}

function carregarDadosModalDeServico(indicadorId, setorId, servicoId) {
  fetch('/lista_clientes/')
  .then(response => response.json())
  .then(clientes => {
    const selectCliente = document.getElementById('cliente-servico');
      selectCliente.innerHTML = '<option selected value="">Selecione o cliente</option>';
      clientes.forEach(cliente => {
        const option = document.createElement('option');
        option.value = cliente.id;
        
        let cnpjRazaoSocial = '';
        if (cliente.cnpj) { cnpjRazaoSocial += cliente.cnpj; }
        if (cliente.razao_social) { cnpjRazaoSocial += cliente.razao_social; }
        option.textContent = cnpjRazaoSocial;

        selectCliente.appendChild(option);
      });
    })
    .catch(error => console.error('Erro ao carregar clientes:', error));

  fetch('/lista_status_servico/')
    .then(response => response.json())
    .then(statusServicos => {
      const selectStatusServico = document.getElementById('status-servico');
      selectStatusServico.innerHTML = '<option selected value="">Selecione o status</option>';
      statusServicos.forEach(statusServico => {
        const option = document.createElement('option');
        option.value = statusServico.id;
        option.textContent = statusServico.descricao;
        selectStatusServico.appendChild(option);
      });
    })
    .catch(error => console.error('Erro ao carregar status de serviços:', error));

    const selectPeriodoServico = document.getElementById('periodo-servico');
    const periodos = gerarPeriodos();
    selectPeriodoServico.innerHTML = '<option selected value="">Selecione o período</option>';
    periodos.forEach(periodo => {
      const option = document.createElement('option');
      option.value = periodo;
      option.textContent = periodo;
      selectPeriodoServico.appendChild(option);
    });

    document.getElementById('indicador-servico').value = indicadorId;
    document.getElementById('setor-servico').value = setorId;
    
    if (servicoId) {
      fetch(`/busca_servico/${servicoId}`)
      .then(response => response.json())
      .then(servico => {
        const dataHoraInicio = servico.data_hora_inicio.replace('Z', '');
        const dataHoraFim = servico.data_hora_fim.replace('Z', '');

        document.getElementById('servico-id').value = servico.id;
        document.getElementById('cliente-servico').value = servico.cliente_id;
        document.getElementById('data-hora-inicio-servico').value = dataHoraInicio.slice(0, 16);
        document.getElementById('data-hora-fim-servico').value = dataHoraFim.slice(0, 16);
        document.getElementById('status-servico').value = servico.status;
        document.getElementById('periodo-servico').value = servico.periodo;
      })
      .catch(error => console.error('Erro ao buscar serviço:', error));
    }
}
 
function gerarPeriodos() {
  const periodos = [];
  const dataAtual = new Date();
  const totalMeses = 12;

  for (let mes = totalMeses; mes >= 1; mes--) {
    const data = new Date(dataAtual.getFullYear(), dataAtual.getMonth() - mes);
    const mesAno = `${String(data.getMonth() + 1).padStart(2, '0')}/${data.getFullYear()}`;
    periodos.push(mesAno);
  }

  const mesAtual = `${String(dataAtual.getMonth() + 1).padStart(2, '0')}/${dataAtual.getFullYear()}`;
  periodos.push(mesAtual);

  for (let mes = 1; mes <= totalMeses; mes++) {
    const data = new Date(dataAtual.getFullYear(), dataAtual.getMonth() + mes);
    const mesAno = `${String(data.getMonth() + 1).padStart(2, '0')}/${data.getFullYear()}`;
    periodos.push(mesAno);
  }

  return periodos;
}

function salvarServico() {
  const form = document.getElementById('servicoForm');
  const formData = new FormData(form);
  const servicoId = formData.get('servico_id');

  const url = servicoId ? `/atualiza_servico/${servicoId}/` : '/cria_servico/';

  fetch(url, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
    }
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalServico'));
        modal.hide();

        const botaoIndicador = document.querySelector(`.btn-menu-indicador[data-indicador-id="${data.indicador}"]`);
        if (botaoIndicador) { botaoIndicador.click(); }
      } else {
        const erros_servico = document.getElementById('erros-servico');
        erros_servico.innerHTML = '<ul></ul>';
        erros_servico.style.display = 'block';

        for (const [field, messages] of Object.entries(data.errors)) {
          const erro = document.createElement('li');
          erro.textContent = `${field}: ${messages.join(", ")}`;
          erros_servico.querySelector('ul').appendChild(erro);
        }
      }
  })
  .catch(error => console.error('Erro ao cadastrar serviço:', error));
}

function apagarServico(servicoId) {
  if (confirm('Você tem certeza que deseja apagar este serviço?')) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`exclui_servico/${servicoId}/`, {
      method: 'DELETE',
      headers: { 'X-CSRFToken': csrfToken }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const botaoIndicador = document.querySelector(`.btn-menu-indicador[data-indicador-id="${data.indicador}"]`);
        if (botaoIndicador) { botaoIndicador.click(); }
      } else {
        alert("Ocorreu um erro ao apagar o serviço");
      }
    })
    .catch(error => console.error('Erro ao apagar serviço:', error));
  }
}

function salvarCliente() {
  const form = document.getElementById('clienteForm');
  const formData = new FormData(form);
  const clienteId = formData.get('cliente_id');

  const url = clienteId ? `/atualiza_cliente/${clienteId}/` : '/cria_cliente/';

  fetch(url, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
    }
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
        window.location.reload();
      } else {
        const erros_cliente = document.getElementById('erros-cliente');
        erros_cliente.innerHTML = '<ul></ul>';
        erros_cliente.style.display = 'block';

        for (const [field, messages] of Object.entries(data.errors)) {
          const erro = document.createElement('li');
          erro.textContent = `${field}: ${messages.join(", ")}`;
          erros_cliente.querySelector('ul').appendChild(erro);
        }
      }
  })
  .catch(error => console.error('Erro ao cadastrar cliente:', error));
}

function carregarDadosFormDeCliente(clienteId) {
  if (clienteId) {
    fetch(`/busca_cliente/${clienteId}`)
    .then(response => response.json())
    .then(cliente => {
      document.getElementById('cliente-id').value = cliente.id;
      document.getElementById('cnpj-cliente').value = cliente.cnpj;
      document.getElementById('razao-social-cliente').value = cliente.razao_social;
    })
    .catch(error => console.error('Erro ao buscar cliente:', error));
  }
}

function apagarCliente(clienteId) {
  if (confirm('Você tem certeza que deseja apagar este cliente?')) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/exclui_cliente/${clienteId}/`, {
      method: 'DELETE',
      headers: { 'X-CSRFToken': csrfToken }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.location.reload();
      } else {
        alert("Ocorreu um erro ao apagar o cliente");
      }
    })
    .catch(error => console.error('Erro ao apagar cliente:', error));
  }
}

function pesquisarCnpj(cnpj) {
  if (cnpj) {
    url = `https://api.cnpjs.dev/v1/${cnpj}`;

    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data.cnpj === cnpj) {
          document.getElementById('razao-social-cliente').value = data.razao_social;
        } else {
          document.getElementById('razao-social-cliente').value = "";
          alert(data.title);
        }
      })
      .catch(error => console.error('Erro ao buscar CNPJ:', error));
  } else {
    alert("Por favor, insira um CNPJ para pesquisar.");
  }
}

function mesAnoAtual() {
  const dataAtual = new Date();
  const mesAtual = String(dataAtual.getMonth() + 1).padStart(2, '0');
  const anoAtual = dataAtual.getFullYear();
  return `${mesAtual}/${anoAtual}`;
}