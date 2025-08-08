
let listaServidores = [];
let listaDatas = [];

// Gerar folha de ponto
function gerarTabelaPonto() {
  const mesAno = document.getElementById('txtData').value;
  const txtSetor = document.getElementById('txtSetor');
  const setor = txtSetor.options[txtSetor.selectedIndex].text;
  if (!mesAno) {
    alert("Selecione um mês.");
    return;
  }
  const [anoStr, mesStr] = mesAno.split('-');
  const mes = parseInt(mesStr);
  const ano = parseInt(anoStr);
  const ultimoDia = new Date(ano, mes, 0).getDate();

  const nomeMes = new Date(ano, mes - 1, 1).toLocaleDateString('pt-BR', { month: 'long' }).toUpperCase();
  const cssTabela = `
       <style type="text/css">
                    table {
                       border: 1px solid #000;
                       border-collapse: collapse !important;
                       width: 100% !important;
                       font-size: small;
                       border-spacing: 0; 
                    }
                    td {
                       height: 23px !important;
                       line-height: 23px !important;
                       font-size: xx-small;
                       padding: 0 !important;
                       border: 1px solid #000;
                       text-align: center;
                    }
        </style>`;

  const cabecalho = `${cssTabela}
        <center>
        <img alt="Logo de Buriticupu" src="/static/img/buriticupu_logo.png" style="height:40px" />
           <p style="text-align:center;">
           <span style="font-size:12px;">INSTITUTO FEDERAL DE EDUCA&Ccedil;&Atilde;O, CI&Ecirc;NCIA E TECNOLOGIA DO MARANH&Atilde;O - IFMA CAMPUS BURITICUPU&nbsp;<br />${setor}<br />
            <strong>CONTROLE DE FREQU&Ecirc;NCIA</strong></span>
           </p>
        </center>`
  let html = `${cabecalho}
    <table id="tabela-ponto" border="1" cellpadding="0" cellspacing="0">
  <colgroup>
    <col width="50" />
    <col width="130" />
    <col width="60" />
    <col width="130" />
    <col width="60" />
    <col width="130" />
    <col width="60" />
    <col width="130" />
    <col width="60" />
  </colgroup>
  <tbody>
    <tr>
      <td><strong>SETOR:</strong></td>
      <td>servidor_setor</td>
      <td colspan="2"><strong>SIAPE:</strong> servidor_matricula</td>
      <td colspan="2"><strong>MÊS:</strong> ${nomeMes}/${ano}</td>
      <td colspan="3"><strong>FUNÇÃO:</strong></td>
    </tr>
    <tr>
      <td><strong>NOME:</strong></td>
      <td colspan="3">servidor_nome</td>
      <td colspan="2">servidor_cargo</td>
      <td colspan="3">servidor_funcao</td>
    </tr>
    <tr>
      <td rowspan="2">Dia</td>
      <td colspan="2">Entrada</td>
      <td colspan="2">Saída</td>
      <td colspan="2">Entrada</td>
      <td colspan="2">Saída</td>
    </tr>
    <tr style="font-weight:bold;">
      <td>Rubrica</td>
      <td>Hora</td>
      <td>Rubrica</td>
      <td>Hora</td>
      <td>Rubrica</td>
      <td>Hora</td>
      <td>Rubrica</td>
      <td>Hora</td>
    </tr>
      `;

  for (let dia = 1; dia <= ultimoDia; dia++) {
    const dataAtual = new Date(ano, mes - 1, dia);
    const diaSemana = dataAtual.getDay();
    const diaStr = dia.toString().padStart(2, '0');

    const itensDoDia = listaDatas.filter(item => {
      const [anoItem, mesItem, diaItem] = item.data.split('-').map(n => parseInt(n, 10));
      const dataItem = new Date(anoItem, mesItem - 1, diaItem);
      return dataItem.toDateString() === dataAtual.toDateString();
    });

    if (itensDoDia.length > 0) {
      itensDoDia.forEach(item => {
        if (item.tipo === '1') {
          html += `
        <tr>
          <td>${diaStr}</td>
          <td>{rubrica}</td><td>{hora}</td>
          <td>{rubrica}</td><td>{hora}</td>
          <td>{rubrica}</td><td>{hora}</td>
          <td>{rubrica}</td><td>{hora}</td>
        </tr>`;
        } else if (item.tipo === '0') {

          const diasSemana = { 0: 'DOMINGO', 6: 'SÁBADO' };
          let valor = (diaSemana === 0 || diaSemana === 6) ? diasSemana[diaSemana] : item.nome;

          html += `
        <tr>
          <td>${diaStr}</td>
          <td colspan="8">${valor}</td>
        </tr>`;
        }
      });
    } else {
      if (diaSemana === 0) {
        html += `
      <tr>
        <td>${diaStr}</td>
        <td colspan="8">DOMINGO</td>
      </tr>`;
      } else if (diaSemana === 6) {
        html += `
      <tr>
        <td>${diaStr}</td>
        <td colspan="8">SÁBADO</td>
      </tr>`;
      } else {
        html += `
      <tr>
        <td>${diaStr}</td>
        <td>{rubrica}</td><td>{hora}</td>
        <td>{rubrica}</td><td>{hora}</td>
        <td>{rubrica}</td><td>{hora}</td>
        <td>{rubrica}</td><td>{hora}</td>
      </tr>`;
      }
    }
  }

  const tabela_assinaturas = `<br>
    <table style="width: 100%; text-align: center; border:none">
     <colgroup>
    <col width="250" />
    <col width="250" />
  </colgroup>
  <thead>
    <tr>
      <th style="border: none;"><strong>Visto em</strong>: ____/____/${ano}</th>
      <th style="border: none;">{visto_servidor}</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: none;"><br>___________________________________________________________________<br><strong>Chefe imediato</strong></td>
      <td style="border: none;">{assinatura_servidor}</td>
    </tr>
  </tbody>
</table>`;

  html += '</tbody></table>' + tabela_assinaturas + `<div style="page-break-after: always"><span style="display: none;">&nbsp;</span></div>`;

  CKEDITOR.instances['editor1'].setData(`<div class="container">${html}</div>`);
}
// Salvar folha de ponto gerada
function AdicionarFolha() {

  const setorFolha = obterElemento('txtSetor');
  const mesAnoFolha = obterElemento('txtData');
  const dados = CKEDITOR.instances['editor1'].getData();

  const campos = [setorFolha, mesAnoFolha];

  if (algumCampoVazio(campos)) {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  const formData = new FormData();

  formData.append('mes_ano', mesAnoFolha.value);
  formData.append('setor_id', setorFolha.value);
  formData.append('dados', dados);

  fetch(`/folhas/adicionar/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': ObterTokenCRSF(),
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'sucesso') {
        location.reload();
      } else {
        alert(data.mensagem);
      }
    })
    .catch(error => {
      alert('Erro na requisição');
    })
}
// Obter Servidores de um setor
function ObterServidoresDoSetor(id_setor) {
  fetch(`/folhas/servidoresdosetor/${id_setor}/`)
    .then(response => {
      if (!response.ok) throw new Error("Erro de rede");
      return response.json();
    })
    .then(data => {
      if (data.status === 'sucesso') {
        if (data.dados && data.dados.length > 0) {
          listaServidores = data.dados;
        } else {
          alert('Não existem servidores no setor selecionado!');
        }
      } else {
        console.error("Erro:", data.mensagem);
        alert("Erro: " + data.mensagem);
      }
    })
    .catch(error => {
      console.error("Erro na requisição:", error);
      alert('Erro na requisição.');
    });
}
// Obter Datas cadastradas do mês selecionado
function ObterDatasMesAnoSelecionado(mesAno) {
  const [anoStr, mesStr] = mesAno.split('-');

  fetch(`/folhas/datasmesanoselecionado/${anoStr}-${mesStr}/`)
    .then(response => {
      if (!response.ok) throw new Error("Erro de rede");
      return response.json();
    })
    .then(data => {
      if (data.status === 'sucesso') {
        if (data.dados && data.dados.length > 0) {
          listaDatas = data.dados;
        }

      } else {
        console.error("Erro:", data.mensagem);
        alert("Erro: " + data.mensagem);
      }
    })
    .catch(error => {
      console.error("Erro na requisição:", error);
      alert('Erro na requisição.');
    });
}
// Obtém a folha de frequência
function ObterFolha(folha_id) {
  fetch(`/folhas/obter/${folha_id}/`)
    .then(response => response.json())
    .then(data => {
      let html = '';
      if (data.status === 'sucesso') {
        const folhaBase = data.dados.folha.dados;
        const anoAtual = new Date().getFullYear();

        data.dados.servidores.forEach(element => {
          const em_afastamento = element.em_afastamento;

          const svg_diagonais = `
            <svg width="100%" height="50%" viewBox="0 0 100 100" preserveAspectRatio="none">
              <line x1="0" y1="0" x2="100" y2="100" stroke="black" stroke-width="1"/>
              <line x1="0" y1="100" x2="100" y2="0" stroke="black" stroke-width="1"/>
            </svg>
          `;

          html += folhaBase
            .replace('servidor_setor', element.setor__sigla)
            .replace('servidor_nome', element.nome)
            .replace('servidor_matricula', element.matricula)
            .replace('servidor_cargo',
              element.cargo__area__nome === '-'
                ? element.cargo__nome
                : `${element.cargo__nome} (${element.cargo__area__nome})`
            )
            .replace('servidor_funcao', element.funcao__nome || '')
            .replaceAll('{rubrica}', em_afastamento ? svg_diagonais : '')
            .replaceAll('{hora}', em_afastamento ? svg_diagonais : '')
            .replace('{visto_servidor}',
              em_afastamento
                ? `${element.tipo_afastamento_display}`
                : `<strong>Visto em</strong>: ____/____/${anoAtual}`
            )
            .replace('{assinatura_servidor}',
              em_afastamento
                ? `<strong>${formatarData(element.data_inicio_afastamento)} até ${formatarData(element.data_fim_afastamento)}</strong>`
                : `<br>___________________________________________________________________<br><strong>Servidor</strong>`
            )
        });

        abrirPopup(html);
      }
    })
    .catch(error => {
      alert('Erro na requisição:', error);
    });
}
// Obter dados de forma genérica
async function ListarDados(url) {
  return fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.status === 'sucesso') {
        return data;
      } else {
        alert(data.mensagem);
        return null;
      }
    })
    .catch(erro => {
      alert('Ocorreu um erro na requisição.');
      return null;
    });
}
// Adicionar Dados de forma genérica
async function InserirDados(url, formData, recarregar = true) {
  mostrarLoadingBar();
  return fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': ObterTokenCRSF(),
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'sucesso') {
        if (recarregar === true) {
          location.reload();
        } else {
          return data;
        }
      } else {
        alert(data.mensagem);
      }
    })
    .catch(error => {
      alert('Erro  na requisição.')
    })
    .finally(() => {
      esconderLoadingBar();
    });
}
// Obter um registro de forma genérica
async function ObterDados(url) {
  mostrarLoadingBar();
  return fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.status === 'sucesso') {
        return data;
      } else {
        alert(data.mensagem);
        return;
      }
    })
    .catch(error => {
      alert('Erro  na requisição.');
      return;
    }).finally(() => {
      esconderLoadingBar();
    });
}
// Editar um registro de forma genérica
async function EditarDados(url, formData) {
  mostrarLoadingBar();
  return fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': ObterTokenCRSF(),
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'sucesso') {
        location.reload();
      } else {
        alert(data.mensagem);
      }
    })
    .catch(error => {
      alert('Erro  na requisição.');
    }).finally(() => {
      esconderLoadingBar();
    });;
}
// Excluir dados de forma genérica
async function ExcluirDados(url) {
  mostrarLoadingBar();
  return fetch(url, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': ObterTokenCRSF(),
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(response => response.json())
    .then(data => {

      if (data.status === 'sucesso') {
        location.reload();
      } else {
        alert(data.mensagem);
        return;
      }
    })
    .catch(error => {
      alert('Erro  na requisição.')
      return;
    }).finally(() => {
      esconderLoadingBar();
    });
}
// Pesquisar dados de forma genérica com async/await
async function PesquisarDados(url) {
  mostrarLoadingBar();
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === 'sucesso') {
      return data;
    } else {
      alert(data.mensagem || 'Erro desconhecido ao processar os dados.');
      return null;
    }

  } catch (erro) {
    console.error(erro);
    alert('Erro na requisição. Verifique a conexão ou o servidor.');
    return null;
  } finally {
    esconderLoadingBar();
  }
}
async function ObterFeriadosNacionais() {
  mostrarLoadingBar();
  const ano = new Date();
  return fetch(`https://brasilapi.com.br/api/feriados/v1/${ano.getFullYear()}`)
    .then(response => response.json())
    .then(data => {
      if (data) {
        return data;
      }
    })
    .catch(error => {
      alert('Erro  na requisição.');
      return;
    }).finally(() => {
      esconderLoadingBar();
    });
}


async function AdicionarAfatasmentoDoServidor(id_servidor) {


  const txtTipoAfastamentoServidor = obterElemento('txtTipoAfastamentoServidor');
  const txtDataInicioAfastamentoServidor = obterElemento('txtDataInicioAfastamentoServidor');
  const txtDataFimAfastamentoServidor = obterElemento('txtDataFimAfastamentoServidor');
  const txtSubstitutoServidorEditar = obterElemento('txtSubstitutoServidorEditar');

  const campos = [txtTipoAfastamentoServidor, txtDataInicioAfastamentoServidor, txtDataFimAfastamentoServidor];

  if (algumCampoVazio(campos)) {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  const formData = new FormData();

  if (isCheckboxMarcado('txtEmAfastamentoServidor')) {
    formData.append('em_afastamento', '1');
    formData.append('tipo_afastamento', txtTipoAfastamentoServidor.value);
    formData.append('data_inicio_afastamento', txtDataInicioAfastamentoServidor.value);
    formData.append('data_fim_afastamento', txtDataFimAfastamentoServidor.value);
    formData.append('id_substituto', txtSubstitutoServidorEditar.value);
  } else {
    formData.append('em_afastamento', '0');
  }

  mostrarLoadingBar();

  return fetch(`/servidores/afastamentos/adicionar/${id_servidor}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': ObterTokenCRSF(),
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      alert(data.mensagem);
    })
    .catch(error => {
      alert('Erro  na requisição.');
      return;
    }).finally(() => {
      esconderLoadingBar();
    });
}




