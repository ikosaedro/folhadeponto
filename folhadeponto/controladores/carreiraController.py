from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import JsonResponse
from django.template import loader
from folhadeponto.models import Carreira,  Servidor, Cargo, Usuario
from folhadeponto.utilitarios import acoes
from django.db import models
from django.db.models import Count, Q, OuterRef, Subquery

def ver_carreiras(request):
    
    if acoes.checar_tipo_requisicao(request, 'GET'):
        template = loader.get_template('carreiras.html')
        
        id_campus = acoes.obter_id_campus(request.user.email)

        carreiras = Carreira.objects.filter(campus_id = id_campus).annotate(
            num_cargos=Count('cargo', distinct=True),  
            num_servidores=Count('cargo__servidor', distinct=True) 
        ).values('id', 'nome', 'data_cadastro', 'num_cargos', 'num_servidores')  

        dados = {'carreiras': carreiras}

        return HttpResponse(template.render(dados, request))

    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')
    
def adicionar_carreira(request):
    if not acoes.checar_tipo_requisicao(request, 'POST'):
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')

    try:
        dados = acoes.extrair_dados_da_requisicao(request, modelo=Carreira)
        try:
            dados['campus_id'] =  acoes.obter_id_campus(request.user.email)
        except Usuario.DoesNotExist:
            return acoes.resposta_json(status='erro', mensagem='Usuário não autenticado')
            
        Carreira.objects.create(**dados)
        return acoes.resposta_json(status='sucesso')
    
    except Exception as ex:
        return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex) )

def obter_cairreira(request, id_carreira):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            carreira = Carreira.objects.filter(campus_id = id_campus, id=id_carreira).values('nome').first()
            if not carreira:
                return acoes.resposta_json(
                status='erro',
                mensagem='Carreira não encontrada.'
            )
            
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro obtido com sucesso',
                dados= carreira
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


def editar_carreira(request, id_carreira):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        dados = request.POST
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            Carreira.objects.filter(campus_id = id_campus, id=id_carreira).update(nome=dados['nome'])
            
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro atualizado com sucesso!'
            )
        except Exception as e:
            # Em caso de erro, retorna uma mensagem amigável utilizando o interpretador de erros
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(e)
            )
    else:
        # Caso a requisição não seja POST, retorna erro de método não permitido
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.'
        )
        
def excluir_carreira(request, id_carreira):
    # Verifica se a requisição recebida é do tipo DELETE
    if acoes.checar_tipo_requisicao(request, 'DELETE'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            Carreira.objects.filter(campus_id = id_campus, id=id_carreira).delete()

            # Retorna uma resposta de sucesso após exclusão
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro excluído com sucesso!'
            )
        except Exception as e:
            # Em caso de erro na exclusão (ex: integridade referencial), retorna mensagem amigável
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(e)  # Usa a função para interpretar erros do MySQL
            )
    else:
        # Caso o método HTTP não seja DELETE, retorna erro de método não permitido
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.'
        )

def pesquisar_carreiras(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            nome = request.GET.get('nome', '').strip()
            nivel = request.GET.get('nivel', '').strip()
            pgd = request.GET.get('pgd', '').strip().lower()
            afastado = request.GET.get('afastado', '').strip().lower()
            tipo = request.GET.get('tipo', '').strip()

            # Filtro principal por nome da carreira
            id_campus = acoes.obter_id_campus(request.user.email)
            query = Carreira.objects.filter(campus_id=id_campus, nome__icontains=nome)

            # Filtros que serão usados nas subqueries
            cargo_filter = Q(carreira=OuterRef('pk'))
            servidor_filter = Q(cargo__carreira=OuterRef('pk'))

            if nivel:
                cargo_filter &= Q(nivel=nivel)
                servidor_filter &= Q(cargo__nivel=nivel)

            if pgd == 'true':
                servidor_filter &= Q(em_pgd=True)
            elif pgd == 'false':
                servidor_filter &= Q(em_pgd=False)

            if afastado == '1':
                servidor_filter &= Q(em_afastamento=True)
            elif afastado == '0':
                servidor_filter &= Q(em_afastamento=False)

            if tipo:
                servidor_filter &= Q(tipo=tipo)

            # Subquery para contar cargos distintos por carreira
            subquery_num_cargos = Cargo.objects.filter(cargo_filter) \
                .values('carreira') \
                .annotate(total=Count('id', distinct=True)) \
                .values('total')

            # Subquery para contar servidores distintos por carreira
            subquery_num_servidores = Servidor.objects.filter(servidor_filter) \
                .values('cargo__carreira') \
                .annotate(total=Count('id', distinct=True)) \
                .values('total')

            # Anotando os valores com subqueries
            query = query.annotate(
                num_cargos=Subquery(subquery_num_cargos, output_field=models.IntegerField()),
                num_servidores=Subquery(subquery_num_servidores, output_field=models.IntegerField())
            )

            # Garantindo valores únicos por carreira
            carreiras = query.values(
                'id', 'nome', 'data_cadastro', 'num_cargos', 'num_servidores'
            ).order_by('nome')

            return acoes.resposta_json(dados=list(carreiras))

        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex)
            )

    return acoes.resposta_json(
        status='erro',
        mensagem='Método não permitido.'
    )

