document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('.btn-custom');
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
