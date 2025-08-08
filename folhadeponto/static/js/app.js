
// Controle tabs
document.querySelectorAll('.tab-nav li').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabId = tab.getAttribute('data-tab');

        document.querySelectorAll('.tab-nav li').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));

        tab.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});


function toggleDropdown(button) {
    const menu = button.nextElementSibling;
    document.querySelectorAll('.custom-dropdown-menu').forEach(el => {
        if (el !== menu) el.classList.remove('show');
    });
    menu.classList.toggle('show');
    document.addEventListener('click', function closeDropdown(e) {
        if (!button.parentElement.contains(e.target)) {
            menu.classList.remove('show');
            document.removeEventListener('click', closeDropdown);
        }
    });
}


const btn = document.getElementById("userMenuButton");
const dropdown = document.getElementById("userDropdown");

btn.addEventListener("click", () => {
    dropdown.classList.toggle("oculto");
    dropdown.classList.toggle("visivel");
});

// Fechar dropdown clicando fora
window.addEventListener("click", function (e) {
    if (!btn.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.add("oculto");
        dropdown.classList.remove("visivel");
    }
});

// Obtém a referência do botão de alternância da sidebar
const toggleButton = document.getElementById('toggle-btn')

// Obtém a referência do elemento da sidebar
const sidebar = document.getElementById('sidebar')

/**
 * Função que alterna a visibilidade (expandida ou recolhida) da sidebar.
 * Também alterna a rotação do botão e fecha todos os submenus abertos.
 */
function toggleSidebar() {
    // Alterna a classe 'close' na sidebar (recolhe ou expande)
    sidebar.classList.toggle('close')

    // Alterna a classe 'rotate' no botão (gira o ícone)
    toggleButton.classList.toggle('rotate')

    // Fecha todos os submenus que estiverem abertos
    closeAllSubMenus()
}

/**
 * Função que alterna a visibilidade de um submenu específico.
 * Se o submenu ainda não está visível, fecha todos os outros.
 * Também gira o ícone do botão e, se a sidebar estiver recolhida, expande-a.
 * 
 * @param {HTMLElement} button - Botão que controla o submenu.
 */
function toggleSubMenu(button) {

    // Se o submenu ainda não está aberto, fecha todos os outros submenus
    if (!button.nextElementSibling.classList.contains('show')) {
        closeAllSubMenus()
    }

    // Alterna a exibição do submenu atual
    button.nextElementSibling.classList.toggle('show')

    // Alterna a rotação do botão do submenu
    button.classList.toggle('rotate')

    // Se a sidebar estiver recolhida, expande-a automaticamente
    if (sidebar.classList.contains('close')) {
        sidebar.classList.toggle('close')
        toggleButton.classList.toggle('rotate')
    }
}

/**
 * Fecha todos os submenus abertos e remove a rotação dos botões
 */
function closeAllSubMenus() {
    // Seleciona todos os elementos com a classe 'show' (submenus abertos)
    Array.from(sidebar.getElementsByClassName('show')).forEach(ul => {
        // Remove a classe 'show' para esconder o submenu
        ul.classList.remove('show')

        // Remove a rotação do botão correspondente
        ul.previousElementSibling.classList.remove('rotate')
    })
}

function obterElemento(id) {
    const elemento = document.getElementById(id);
    return elemento;
}

function carregarViaAjax(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar a página');
            }
            return response.text(); // obtém HTML como texto
        })
        .then(html => {
            document.getElementById('conteudo').innerHTML = html;
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
            document.getElementById('conteudo').innerHTML = '<p>Erro ao carregar o conteúdo.</p>';
        });
}

function obterValorCelula(id_linha, indice) {
    const linha = obterElemento(id_linha);

    if (!linha) {
        alert(`Linha com id ${id_linha} não existe.`);
        return;
    }

    const celulas = linha.querySelectorAll('td');

    if (indice < 0 || indice >= celulas.length) {
        alert(`Índice da célula (${indice}) inválido.`);
        return;
    }

    const valorCelula = celulas[indice].textContent.trim();
    return valorCelula;
}

function setarHTML(controle, valor) {
    const elemento = obterElemento(controle);
    elemento.innerHTML = valor;
}

function obterHTML(controle) {
    const valor = obterElemento(controle).innerHTML;
    return valor;
}
function obterValor(controle) {
    const valor = obterElemento(controle).value;
    return valor;
}
function setarValor(controle, valor) {
    const elemento = obterElemento(controle);
    elemento.value = valor;
}

function setarDataId(idElemento, valor) {
    const elemento = document.getElementById(idElemento);
    if (elemento) {
        elemento.setAttribute('data-id', valor);
    } else {
        console.warn('Elemento não encontrado:', idElemento);
    }
}

function CaixaDeImpressao() {
    window.print();
}

// Obtenção do CSRF Token
function ObterTokenCRSF() {
    const name = 'csrftoken'
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function montarFormData(obj) {
    const formData = new FormData();
    for (const chave in obj) {
        if (obj.hasOwnProperty(chave)) {
            formData.append(chave, obj[chave]);
        }
    }
    return formData;
}

// Função que verifica se algum campo está vazio em uma lista de inputs/selects
function algumCampoVazio(campos) {
    for (let campo of campos) {
        // Remove espaços e verifica se o valor está vazio
        if (campo.value.trim() === '') {
            campo.focus(); // Dá foco no primeiro campo vazio encontrado
            return true;   // Retorna true indicando que há pelo menos um campo vazio
        }
    }
    return false; // Todos os campos estão preenchidos
}

function abrir(modalId) {
    const modal = obterElemento(`${modalId}`);
    const fundo = obterElemento(`${modalId}Backdrop`);

    modal.style.display = 'flex';
    fundo.style.display = 'block';
    void modal.offsetWidth;
    void fundo.offsetWidth;
    modal.classList.add('show');
    fundo.classList.add('show');
    modal.focus();
}

function fechar(modalId) {
    const modal = obterElemento(`${modalId}`);
    const fundo = obterElemento(`${modalId}Backdrop`);

    modal.classList.remove('show');
    fundo.classList.remove('show');
    setTimeout(() => {
        modal.style.display = 'none';
        modal.style.display = 'none';
    }, 300);
}

function mostrarLoadingBar() {
    obterElemento('loadingSpinner').style.display = 'flex';
}

function esconderLoadingBar() {
    obterElemento('loadingSpinner').style.display = 'none';
}

function formatarData(dataIso) {
    if (!dataIso) return '-';
    const data = new Date(dataIso + 'T00:00:00Z'); // força UTC
    const dia = String(data.getUTCDate()).padStart(2, '0');
    const mes = String(data.getUTCMonth() + 1).padStart(2, '0');
    const ano = data.getUTCFullYear();
    return `${dia}/${mes}/${ano}`;
}

function formatarDataHora(isoString) {
    const data = new Date(isoString);
    const dia = String(data.getDate()).padStart(2, '0');
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const ano = data.getFullYear();
    const hora = String(data.getHours()).padStart(2, '0');
    const minuto = String(data.getMinutes()).padStart(2, '0');
    return `${dia}/${mes}/${ano} ${hora}:${minuto}`;
}

function obterDiaDaSemana(dataStr) {
    const diasSemana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira',
        'Quinta-feira', 'Sexta-feira', 'Sábado'];

    const partes = dataStr.split('-');
    const ano = parseInt(partes[0], 10);
    const mes = parseInt(partes[1], 10) - 1;
    const dia = parseInt(partes[2], 10);

    const data = new Date(ano, mes, dia);
    const diaSemana = data.getDay();

    return diasSemana[diaSemana];
}

function abrirPopup(html) {
    const novaJanela = window.open('', '_blank', 'width=794, height=1123');
    novaJanela.document.write(`
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <title>Filha de frequência</title>
    </head>
    <body onload="window.print();window.close();">
      ${html}
    </body>
    </html>
  `);
    novaJanela.document.close();
}

function limparFormulario(controle) {
    const form = obterElemento(controle);
    form.querySelectorAll("input, textarea, select").forEach(campo => {
        if (campo.type === "checkbox" || campo.type === "radio") {
            campo.checked = false;
        } else {
            campo.value = "";
        }
    });
}

function exibirPeloCheckBox(checkbox, idDiv) {
  const div = obterElemento(idDiv);
  if (div) {
    div.style.display = checkbox.checked ? 'block' : 'none';
  }
}


function marcarCheckbox(idCheckbox, valor) {
  const checkbox = obterElemento(idCheckbox);
  if (checkbox) {
    checkbox.checked = valor === true;
  }
}

function isCheckboxMarcado(idCheckbox) {
  const checkbox = obterElemento(idCheckbox);
  if (checkbox) {
    return checkbox.checked;
  }
  return false;
}