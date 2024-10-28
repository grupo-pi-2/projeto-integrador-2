document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('.btn-menu-indicador');
  const indicadorContainer = document.getElementById('indicador-container');

  buttons.forEach(button => {
    button.addEventListener('click', function() {
      const indicadorId = this.getAttribute('data-indicador-id');

      fetch(`/busca_indicador/${indicadorId}`)
        .then(response => response.text())
        .then(data => {
          indicadorContainer.innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
    });
  });
});

function carregarDadosModalDeServico(indicadorId, setorId) {
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

  fetch(form.action, {
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
