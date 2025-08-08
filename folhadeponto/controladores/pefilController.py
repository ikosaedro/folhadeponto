from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import JsonResponse
from django.template import loader
from folhadeponto.models import Area,  Servidor, Setor, Usuario
from folhadeponto.utilitarios import acoes
from django.db import models
from django.db.models import Count, Q, OuterRef, Subquery


def ver_perfil(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        id_campus = acoes.obter_id_campus(request.user.email)
        servidor_id = acoes.obter_id_servidor_logado(request)
        servidor = Servidor.objects.get(id=servidor_id)
        setores = list(
            Setor.objects
            .filter(
                campus_id=id_campus, 
                responsavel__id=servidor_id)
            .annotate(
                num_servidores=Count('servidores', distinct=True),
                num_cargos=Count('servidores__cargo', distinct=True))
            .values(
                    'id',
                    'nome',
                    'sigla',
                    'responsavel__nome',
                    'num_cargos',
                    'num_servidores',
                    'data_cadastro'
                )
        )
        
        dados_setores = {
            'servidor': servidor, 
            'setores': setores,
        }
        return render(request, 'perfil.html', dados_setores)
    
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')