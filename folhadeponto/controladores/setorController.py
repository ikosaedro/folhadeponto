from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import JsonResponse
from django.template import loader
from django.db import models
from django.db.models import Subquery, OuterRef, Exists
from django.db.models import Count, Q
from folhadeponto.models import Setor, Servidor
from folhadeponto.utilitarios import acoes

def listar_servidores(id_campus):
    try:
        servidores = Servidor.objects.filter(campus_id=id_campus).values("id", "nome").order_by("nome")
        return servidores
    except Exception as e:
        return {}

def ver_setores(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        
        template = loader.get_template('setores.html')
       
        id_campus = acoes.obter_id_campus(request.user.email)
        setores = list(
            Setor.objects
            .filter(
                campus_id= id_campus)
            .annotate(
                num_servidores=Count('servidores'))
            .values(
                    'id',
                    'nome',
                    'sigla',
                    'responsavel__nome',
                    'num_servidores',
                    'data_cadastro'
                )
        )
        servidores = list(listar_servidores(id_campus))
        dados_setores = {
            'setores': setores,
            'servidores': servidores,
        }
        return HttpResponse(template.render(dados_setores, request))
    
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')
    

def adicionar_setor(request):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            dados = acoes.extrair_dados_da_requisicao(request, Setor)
            try:
                dados['campus_id'] = acoes.obter_id_campus(request.user.email)
            except:
                return acoes.resposta_json(status='erro', mensagem='Usuário não autenticado')
            Setor.objects.create(**dados)
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Setor adicionado com sucesso!'
            )

        except Exception as e:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(e)
            )
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')
    
       
def excluir_setor(request, id_setor):
    if acoes.checar_tipo_requisicao(request, 'DELETE'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            num_deletados, _ = Setor.objects.filter(campus_id=id_campus, id=id_setor).delete()

            if num_deletados > 0:
                return acoes.resposta_json(
                    status='sucesso',
                    mensagem='Registro excluído com sucesso!'
                )
            else:
                return acoes.resposta_json(
                    status='erro',
                    mensagem='Nenhum registro encontrado para exclusão.'
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
        
def obter_setor(request, id_setor):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            setor = (
                Setor.objects
                .filter(campus_id=id_campus, id=id_setor)  # Filtra o setor pelo ID
                .values(
                    'nome',
                    'sigla',
                    'responsavel__id',     # ID do servidor responsável
                )
                .first()  
            )
            if not setor:
                return acoes.resposta_json(
                    status='erro',
                    mensagem='Setor não encontrado.',
                    dados=None
                )
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Operação realizada com sucesso.',
                dados=setor
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

def editar_setor(request, id_setor):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            dados = acoes.extrair_dados_da_requisicao(request, Setor)
            id_campus = acoes.obter_id_campus(request.user.email)
            
            registros_atualizados = Setor.objects.filter(campus_id=id_campus, id=id_setor).update(**dados)
            
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

def pesquisar_setores(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            responsavel = request.GET.get('responsavel', '').strip()
            nome_sigla = request.GET.get('nomeSigla', '').strip()
            nivel = request.GET.get('nivel', '').strip()
            pgd = request.GET.get('pgd', '').strip().lower()
            afastado = request.GET.get('afastado', '').strip().lower()
            tipo = request.GET.get('tipo', '').strip()
            id_campus = acoes.obter_id_campus(request.user.email)

            query = Setor.objects.filter(campus_id=id_campus)

            if responsavel:
                query = query.filter(responsavel_id=responsavel)

            if nome_sigla:
                query = query.filter(
                    Q(nome__icontains=nome_sigla) | Q(sigla__icontains=nome_sigla)
                )

            # Filtros para servidores vinculados ao setor
            servidores_filtrados = Servidor.objects.filter(setor=OuterRef('pk'))

            if nivel:
                servidores_filtrados = servidores_filtrados.filter(cargo__nivel=nivel)

            if pgd == 'true':
                servidores_filtrados = servidores_filtrados.filter(em_pgd=True)
            elif pgd == 'false':
                servidores_filtrados = servidores_filtrados.filter(em_pgd=False)

            if afastado == '1':
                servidores_filtrados = servidores_filtrados.filter(em_afastamento=True)
            elif afastado == '0':
                servidores_filtrados = servidores_filtrados.filter(em_afastamento=False)

            if tipo:
                servidores_filtrados = servidores_filtrados.filter(tipo=tipo)

            # Subquery para contar servidores filtrados por setor
            query = query.annotate(
                num_servidores=Subquery(
                    servidores_filtrados.values('setor')
                    .annotate(total=Count('id'))
                    .values('total')[:1],
                    output_field=models.IntegerField()
                )
            )

            setores = query.values(
                'id',
                'nome',
                'sigla',
                'responsavel__nome',
                'num_servidores',
                'data_cadastro'
            )

            return acoes.resposta_json(dados=list(setores))

        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex),
                dados=None
            )

    return acoes.resposta_json(
        status='erro',
        mensagem='Método não permitido!',
        dados=None
    )
