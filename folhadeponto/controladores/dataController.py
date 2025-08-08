from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import JsonResponse
from django.template import loader
from folhadeponto.models import Data
from folhadeponto.utilitarios import acoes


def ver_datas(request):
    
    id_campus = acoes.obter_id_campus(request.user.email)
    
    datas = Data.objects.filter(campus_id=id_campus,).values(
        'id',
        'nome',
        'data',
        'abrangencia',
        'tipo',
        'data_cadastro'
    )
    
    dados = {
        'datas': datas
    }
    return render(request, 'datas.html', dados)

def obter_data(request, id_data):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            data = (
                Data.objects.filter(campus_id=id_campus, id = id_data)  
                .values(
                    'nome',
                    'data',
                    'abrangencia',
                    'tipo',     
                ).first()  
            )
            if not data:
                return acoes.resposta_json(status='erro', mensagem='Setor não encontrado.',dados=None)

            return acoes.resposta_json(status='sucesso', mensagem='Operação realizada com sucesso.', dados=data)

        except Exception as ex:
            return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex))
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.', dados=None)
    
def excluir_data(request, id_data):
    if acoes.checar_tipo_requisicao(request, 'DELETE'):
        id_campus = acoes.obter_id_campus(request.user.email)
        try:
            Data.objects.filter(campus_id=id_campus, id=id_data).delete()
            return acoes.resposta_json(status='sucesso', mensagem='Registro excluído com sucesso!')
        except Exception as e:
            return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(e))
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')
        
def adicionar_data(request):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            dados = acoes.extrair_dados_da_requisicao(request, Data)
            
            try:
                dados['campus_id'] = acoes.obter_id_campus(request.user.email)
            except:
                return acoes.resposta_json(status='erro', mensagem='Usuário não autenticado')
            
            Data.objects.create(**dados)
            return acoes.resposta_json(status='sucesso', mensagem='Operação realizada com sucesso!')
        except Exception as e:
            return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(e))
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')

def editar_data(request, id_data):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            dados = acoes.extrair_dados_da_requisicao(request, Data)
            registros_atualizados = Data.objects.filter(campus_id=id_campus, id=id_data).update(**dados)

            if registros_atualizados == 0:
                return acoes.resposta_json('erro', 'Nenhum registro foi atualizado.')

            return acoes.resposta_json(status='sucesso', mensagem='Operação realizada com sucesso!'
            )

        except Exception as ex:
            return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex), dados=None)
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.', dados=None)
    
def pesquisar_datas(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            data = request.GET.get('data')
            descricao = request.GET.get('descricao')  
            tipo = request.GET.get('tipo')
            abrangencia = request.GET.get('abrangencia')
            id_campus = acoes.obter_id_campus(request.user.email)
            
            query = Data.objects.filter(campus_id=id_campus)
            
            if data:
                query = query.filter(data=data)
            
            if descricao:
                query = query.filter(nome__icontains=descricao)
            
            if tipo:
                query = query.filter(tipo=tipo)
            
            if abrangencia:
                query = query.filter(abrangencia=abrangencia)
            
            datas = query.values(
                'id',
                'nome',
                'data',
                'abrangencia',
                'tipo',
                'data_cadastro'
            )
            
            return acoes.resposta_json(dados=list(datas))

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
   