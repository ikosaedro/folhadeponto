from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.db.models import Count
from folhadeponto.models import Contrato, Servidor
from folhadeponto.utilitarios import acoes
from django.db.models.functions import Upper, Trim
from datetime import datetime
from django.db.models import Subquery, OuterRef
from datetime import date


def ver_contratos(request):
    
    id_campus = acoes.obter_id_campus(request.user.email)
    contratos = Contrato.objects.filter(campus_id=id_campus,).values(
        'id',
        'servidor_id',
        'servidor__nome',
        'data_inicio_contrato',
        'data_fim_contrato'
    )
    
    dados = {
        'contratos': contratos
    }
    return render(request, 'substitutos.html', dados)


def adicionar_contrato(request):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            dados = acoes.extrair_dados_da_requisicao(request, Contrato)
            try:
                dados['campus_id'] = acoes.obter_id_campus(request.user.email)
            except:
                return acoes.resposta_json(status='erro', mensagem='Usuário não autenticado')

            Contrato.objects.create(**dados)

            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro adicionado com sucesso.'
            )
        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex)
            )
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido!'
        )
    
def obter_contrato(request, id_servidor):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            contrato = Contrato.objects.filter(campus_id=id_campus, servidor_id=id_servidor).values(
                'id',
                'servidor__nome',
                'data_inicio_contrato',
                'data_fim_contrato'       
            ).first()

            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro obtido com sucesso',
                dados=contrato
            )

        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex)
            )
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido!'
        )
    
def pesquisar_servidores(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            nome = request.GET.get('nome')
            data_inicio = request.GET.get('data_inicio')
            data_fim_param = request.GET.get('data_fim')  # novo nome
            id_campus = acoes.obter_id_campus(request.user.email)
            query = Contrato.objects.filter(campus_id=id_campus)

            if nome:
                query = query.filter(servidor__nome__icontains=nome)

            if data_inicio:
                try:
                    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                    query = query.filter(data_inicio_contrato__gte=data_inicio)
                except ValueError:
                    pass 

            if data_fim_param:
                try:
                    data_fim_date = datetime.strptime(data_fim_param, '%Y-%m-%d').date()
                    query = query.filter(data_fim_contrato__lte=data_fim_date)
                except ValueError:
                    pass

            servidor_substituido = Servidor.objects.filter(
                substituto=OuterRef('servidor_id')
            ).values('nome')[:1]

            query = query.annotate(
                servidor_substituido_nome=Subquery(servidor_substituido)
            )

            contratos = query.values(
                'id',
                'servidor_id',
                'servidor__nome',
                'servidor_substituido_nome',
                'data_inicio_contrato',
                'data_fim_contrato'
            )

            hoje = date.today()
            for contrato in contratos:
                fim_contrato = contrato.get('data_fim_contrato')
                if fim_contrato:
                    contrato['dias_restantes'] = (fim_contrato - hoje).days
                else:
                    contrato['dias_restantes'] = 0

            return acoes.resposta_json(
                status='sucesso',
                mensagem='Dados obtidos com sucesso',
                dados=list(contratos))
        
        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex)
            )
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido!'
        )