from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import JsonResponse
from django.template import loader
from django.db.models import Count
from folhadeponto.models import Data, Setor, Servidor, Data, Folha
from folhadeponto.utilitarios import acoes


def listar_setores(id_campus, servidor_id):
    setores = Setor.objects.filter(campus_id=id_campus, responsavel__id=servidor_id).values('id', 'sigla','nome').order_by('nome')
    return setores

def obter_datas_mes_selecionado(request, mesAno):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            
            anoStr, mesStr= mesAno.split('-')
            mes = int(mesStr)
            ano = int(anoStr)
            
            datas = Data.objects.filter(campus_id=id_campus, data__year=ano, data__month=mes).values(
                'id', 
                'nome', 
                'data', 
                'tipo')
            return acoes.resposta_json(status='sucesso', mensagem='Dados obtidos com sucesso', dados=list(datas))
        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=str(ex),
                dados=None
            )
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')
    
def lista_folhas(id_campus, servidor_id):
    
    folhas = Folha.objects.filter(campus_id=id_campus, setor__responsavel__id=servidor_id).annotate(num_servidores=Count('setor__servidores')).values(
        'id',
        'setor__nome',
        'setor__sigla',
        'mes_ano',
        'num_servidores'
    ).order_by('-mes_ano')
    return folhas


def ver_folhas(request):
    id_campus = acoes.obter_id_campus(request.user.email)
    servidor_id = acoes.obter_id_servidor_logado(request)
    dados = {
        'setores': list(listar_setores(id_campus, servidor_id)),
        'folhas': list(lista_folhas(id_campus, servidor_id))
    }
    return render(request, 'folha.html', dados)

def obter_servidores_do_setor(request, id_setor):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            servidores = list(Servidor.objects.filter(campus_id=id_campus, setor__id=id_setor).values(
                'id', 
                'nome', 
                'matricula', 
                'cargo__nome', 
                'funcao__nome', 
                'setor__sigla',
                'data_exercicio', 
                'data_cadastro'
            ))
            
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Dados obtidos com sucesso',
                dados=servidores
            )
        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=str(ex),
                dados=None
            )
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')

def adicionar_folha(request):
    
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            dados = acoes.extrair_dados_da_requisicao(request, Folha)
            try:
                dados['campus_id'] = acoes.obter_id_campus(request.user.email)
                Folha.objects.create(**dados)
                
                return acoes.resposta_json(
                status='sucesso',
                mensagem='Dados obtidos com sucesso'
            )
            except Exception as ex:
                return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex))
            
        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex),
                dados=None
            )
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')


def emitir_folhas(request):
    dados = {
        'setores': list(listar_setores(request))
    }
    return render(request,  'emitir.html', dados)

def obter_folha(request, folha_id):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            folha = Folha.objects.filter(campus_id=id_campus, id=folha_id).values(
                'id',
                'setor_id',
                'setor__nome',
                'mes_ano',
                'dados',
                'data_cadastro',
            ).first()

            if folha:
                servidores = list(Servidor.objects.filter(campus_id=id_campus, setor_id=folha['setor_id']).values(
                    'id',
                    'nome',
                    'matricula',
                    'cargo__nome',
                    'cargo__area__nome',
                    'funcao__nome',
                    'setor__sigla',
                    'data_exercicio',
                    'data_cadastro'
                ).order_by("nome"))
            else:
                servidores = []

            dados = {
                'folha': folha,
                'servidores': servidores
            }

            if folha and servidores:
                return acoes.resposta_json(
                    status='sucesso',
                    mensagem='Dados obtidos com sucesso.',
                    dados=dados
                )
            else:
                return acoes.resposta_json(
                    status='vazio',
                    mensagem='Nenhuma folha para o setor e mês selecionado.',
                    dados=dados
                )

        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=str(ex),
                dados=None
            )
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.'
        )


def pesquisar_folhas(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            setor = request.GET.get('setor')
            data = request.GET.get('data')

            # Inicia a query com a contagem de servidores
            query = Folha.objects.filter(campus_id=id_campus).annotate(
                num_servidores=Count('setor__servidores')
            )

            # Aplica filtros apenas se os parâmetros forem fornecidos
            if setor:
                query = query.filter(setor_id=setor)
            if data:
                query = query.filter(mes_ano=data)

            # Monta o resultado
            folhas = query.values(
                'id',
                'setor__nome',
                'setor__sigla',
                'mes_ano',
                'num_servidores'
            )

            return acoes.resposta_json(dados=list(folhas))

        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex),
                dados=None
            )
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido!',
            dados=None)

def excluir_folha(request, id_folha):
    if acoes.checar_tipo_requisicao(request, 'DELETE'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            
            Folha.objects.filter(campus_id=id_campus,id=id_folha).delete()
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro excluído com sucesso!'
            )
        except Exception as e:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(e)
            )
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.'
        )