from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import JsonResponse
from django.template import loader
from folhadeponto.models import Area,  Servidor, Cargo, Usuario
from folhadeponto.utilitarios import acoes
from django.db import models
from django.db.models import Count, Q, OuterRef, Subquery

def ver_areas(request):
    
    if acoes.checar_tipo_requisicao(request, 'GET'):
        
        template = loader.get_template('areas.html')
        
        id_campus = acoes.obter_id_campus(request.user.email)

        areas = Area.objects.filter(campus_id = id_campus).annotate(
            num_cargos=Count('cargo', distinct=True),  
            num_servidores=Count('cargo__servidor', distinct=True) 
        ).values('id', 'nome', 'data_cadastro', 'num_cargos', 'num_servidores')  

        dados = {'areas': areas}
        
        return HttpResponse(template.render(dados, request))

    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')

def adicionar_area(request):
    
    if not acoes.checar_tipo_requisicao(request, 'POST'):
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')

    try:
        dados = acoes.extrair_dados_da_requisicao(request, modelo=Area)
        try:
            dados['campus_id'] =  acoes.obter_id_campus(request.user.email)
        except Usuario.DoesNotExist:
            return acoes.resposta_json(status='erro', mensagem='Usuário não autenticado')
            
        Area.objects.create(**dados)
        return acoes.resposta_json(status='sucesso')
    
    except Exception as ex:
        return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex))
    
def obter_area(request, id_area):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            area = Area.objects.filter(campus_id = id_campus, id=id_area).values('nome').first()
            if not area:
                return acoes.resposta_json(
                status='erro',
                mensagem='Carreira não encontrada.'
            )
            
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro obtido com sucesso',
                dados= area
            )
            
        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex)
            )
    else:
         return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.'
        )

def editar_area(request, id_area):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        dados = request.POST
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            Area.objects.filter(campus_id = id_campus, id=id_area).update(nome=dados['nome'])
            
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro atualizado com sucesso!'
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

def excluir_area(request, id_area):
    
    if acoes.checar_tipo_requisicao(request, 'DELETE'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            Area.objects.filter(campus_id = id_campus, id=id_area).delete()
            
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

def pesquisar_areas(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
           
            nome = request.GET.get('nome', '')
            id_campus = acoes.obter_id_campus(request.user.email)
            
            areas = Area.objects.annotate(
                num_cargos=Count('cargo', distinct=True),
                num_servidores=Count('cargo__servidor', distinct=True)  
            ).filter(campus_id=id_campus, nome__icontains=nome).values(
                'id',
                'nome',
                'num_cargos',
                'num_servidores',  
                'data_cadastro'   
            )
            return acoes.resposta_json(dados=list(areas))
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