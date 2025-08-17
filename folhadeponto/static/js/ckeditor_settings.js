  CKEDITOR.replace('editor1', {
    height: 1000,
    allowedContent: true
  });

  CKEDITOR.on('instanceReady', function (evt) {
    const cke_22 = obterElemento('cke_22');
    const cke_39 = obterElemento('cke_39');
    cke_22.style.display='none';
    cke_39.style.display='none';
    const botaoSalvar = document.querySelector('.cke_button__save');
    if (botaoSalvar) {
      botaoSalvar.classList.remove('cke_button_disabled');
      botaoSalvar.classList.add('cke_button_off')
      botaoSalvar.removeAttribute('aria-disabled');
      botaoSalvar.onclick = function () {
        AdicionarFolha();
        return false;
      };
    }
  });
