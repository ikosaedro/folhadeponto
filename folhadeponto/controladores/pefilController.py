from django.shortcuts import render


from folhadeponto.models import  Setor
from folhadeponto.utilitarios import acoes
from django.db.models import Count


def ver_perfil(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        id_campus = acoes.obter_id_campus(request.user.email)
        servidor_id = acoes.obter_id_servidor_logado(request)
        
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
            'setores': setores,
        }
        return render(request, 'perfil.html', dados_setores)
    
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')