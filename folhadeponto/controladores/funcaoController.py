from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from folhadeponto.models import Funcao
from django.db.models import Count
from folhadeponto.utilitarios import acoes

def ver_funcao(request):
    return render(request, 'funcoes.html')

# Define uma view para exibir as funções cadastradas
def ver_funcoes(request):
    # Verifica se a requisição é do tipo GET
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            # Carrega o template HTML que será usado para renderizar os dados
            template = loader.get_template('funcoes.html')

            # Consulta o banco de dados para obter todas as funções
            # e anota (adiciona) a contagem distinta de servidores relacionados a cada função
            funcoes = Funcao.objects.annotate(
                num_servidores=Count('servidor', distinct=True)  
            ).values(
                'id',
                'nome',
                'sigla',
                'num_servidores',  
                'data_cadastro'
            )
            # Prepara os dados para serem passados ao template
            dados = {
                'funcoes': funcoes
            }

            # Renderiza o template com os dados e retorna como resposta
            return HttpResponse(template.render(dados, request))

        except Exception as ex:
            # Em caso de erro, retorna uma resposta JSON com mensagem de erro
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex)
            )
    else:
        # Se o método HTTP não for GET, retorna erro de método não permitido
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')

    

# Define uma função para lidar com a requisição de adição de uma nova função
def adicionar_funcao(request):
    # Verifica se o tipo da requisição HTTP é POST
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            # Extrai os dados da requisição e os mapeia para o modelo Funcao
            dados = acoes.extrair_dados_da_requisicao(request, Funcao)
            
            try:
                dados['campus_id'] = acoes.obter_id_campus(request.user.email)
            except:
                return acoes.resposta_json(status='erro', mensagem='Usuário não autenticado')
            
            # Cria um novo registro na tabela 'Funcao' com os dados extraídos
            Funcao.objects.create(**dados)

            # Retorna uma resposta JSON indicando sucesso
            return acoes.resposta_json(status='sucesso', mensagem='Registro adicionado com sucesso!')
        
        except Exception as ex:
            # Em caso de erro inesperado, retorna uma mensagem genérica
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex)
            )
    
    else:
        # Se o método da requisição não for POST, retorna erro informando que o método não é permitido
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')

def obter_funcao(request, id_funcao):
    # Verifica se a requisição é do tipo GET
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            funcao = Funcao.objects.filter(campus_id=id_campus, id=id_funcao).values(
                'id',
                'nome',
                'sigla'
            ).first()

            # Verifica se o resultado da consulta está vazio
            if not funcao:
                # Retorna uma resposta JSON informando que não foi possível encontrar o registro
                return acoes.resposta_json(
                    status='erro',
                    mensagem='Não foi possível obter o registro requerido.'
                )
            
            # Retorna uma resposta JSON de sucesso com os dados da função
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Operação realizada com sucesso!',
                dados=funcao
            )

        except Exception as ex:
            # Em caso de erro inesperado, retorna uma mensagem genérica
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex)
            )
    else:
        # Se o método da requisição não for GET, retorna erro informando que o método não é permitido
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.'
        )

# View para excluir uma função específica, dado seu ID, via requisição DELETE
def excluir_funcao(request, id_funcao):
    # Verifica se a requisição é do tipo DELETE
    if acoes.checar_tipo_requisicao(request, 'DELETE'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            num_deletados, _ = Funcao.objects.filter(campus_id=id_campus, id=id_funcao).delete()

            # Verifica se algum registro foi realmente deletado
            if num_deletados > 0:
                return acoes.resposta_json(
                    status='sucesso',
                    mensagem='Registro excluído com sucesso!'
                )
            else:
                # Nenhum registro foi encontrado com o ID informado
                return acoes.resposta_json(
                    status='erro',
                    mensagem='Nenhum registro encontrado para exclusão.'
                )

        except Exception as e:
            # Em caso de erro na exclusão (ex: erro no banco de dados), retorna mensagem de erro
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(e)
            )
    else:
        # Caso a requisição não seja do tipo DELETE, retorna erro
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.'
        )


def editar_funcao(request, id_funcao):
    
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            
            dados = acoes.extrair_dados_da_requisicao(request, Funcao)
            id_campus = acoes.obter_id_campus(request.user.email)

            registros_atualizados = Funcao.objects.filter(campus_id=id_campus, id=id_funcao).update(**dados)
            
            if registros_atualizados == 0:
                return acoes.resposta_json('erro', 'Nenhum registro foi atualizado.')
            
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Operação realizada com sucesso!'
            )

        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex),
                dados=None
            )

    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.',
            dados=None
        )

def pesquisar_funcoes(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
           
            nome = request.GET.get('nome', '')
            id_campus = acoes.obter_id_campus(request.user.email)
            
            funcoes = Funcao.objects.annotate(
                num_servidores=Count('servidor', distinct=True)  
            ).filter(campus_id=id_campus, nome__icontains=nome).values(
                'id',
                'nome',
                'sigla',
                'num_servidores',  
                'data_cadastro'   
            )
            return acoes.resposta_json(dados=list(funcoes))
        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex),
                dados=None
            )
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.',
            dados=None
        )