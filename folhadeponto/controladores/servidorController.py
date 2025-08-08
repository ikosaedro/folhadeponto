
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from folhadeponto.models import Cargo, Setor, Funcao, Servidor, Area
from folhadeponto.utilitarios import acoes
from datetime import date

def listar_cargos(id_campus):
    cargos = Cargo.objects.filter(campus_id=id_campus).values('id', 'nome','area__nome').order_by("nome")
    return cargos

def listar_setores(id_campus):
    setores = Setor.objects.filter(campus_id=id_campus).values('id', 'sigla').order_by("sigla")
    return setores

def listar_funcoes(id_campus):
    funcoes = Funcao.objects.filter(campus_id=id_campus).values('id', 'nome').order_by('nome')
    return funcoes

def listar_areas(id_campus):
    areas = Area.objects.filter(campus_id=id_campus).values('id', 'nome').order_by('nome')
    return areas

def ver_servidores(request):
    id_campus = acoes.obter_id_campus(request.user.email)
    
    servidores = list(Servidor.objects.filter(campus_id=id_campus).values(
        'id',
        'nome',
        'matricula',
        'cargo__nome',
        'cargo__area__nome',
        'tipo',
        'em_afastamento',
        'data_inicio_afastamento',
        'data_fim_afastamento',
        'contrato__data_fim_contrato',
        'funcao__nome',
        'setor__sigla',
        'data_exercicio',
        'data_cadastro'
    ))

    
    hoje = date.today()
    for servidor in servidores:
      data_fim = servidor.get('contrato__data_fim_contrato')
      if data_fim:
          servidor['dias_restantes'] = (data_fim - hoje).days
      else:
          servidor['dias_restantes'] = 0 

    servidores_contratados = [s for s in servidores if s['tipo'] == 'CONTRATADO']

    contexto = {
        'servidores': servidores,
        'servidores_contratados': list(servidores_contratados),
        'cargos': list(listar_cargos(id_campus)),
        'setores': list(listar_setores(id_campus)),
        'funcoes': list(listar_funcoes(id_campus)),
        'areas': list(listar_areas(id_campus)),
    }

    return render(request, 'servidores.html', contexto)


def obter_servidor(request, id_servidor):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            servidor = Servidor.objects.filter(campus_id=id_campus,id=id_servidor).values(
                'id',               
                'nome',             
                'matricula',
                'em_pgd',
                'em_afastamento',
                'tipo',
                'tipo_afastamento',
                'data_inicio_afastamento',
                'data_fim_afastamento',
                'substituto',        
                'data_exercicio',   
                'data_cadastro',    
                'cargo__id',        
                'setor__id',        
                'funcao__id',       
            ).first()

            if not servidor:
                return acoes.resposta_json(
                    status='erro',
                    mensagem='Servidor não encontrado.'
                )
            
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro obtido com sucesso',
                dados=servidor
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

def editar_servidor(request, id_servidor):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            dados = acoes.extrair_dados_da_requisicao(request, Servidor)
            id_campus = acoes.obter_id_campus(request.user.email)
            registros_atualizados = Servidor.objects.filter(campus_id=id_campus, id=id_servidor).update(**dados)
            
            if registros_atualizados == 0:
                return acoes.resposta_json(
                    status='erro',
                    mensagem='Nenhum registro foi atualizado.'
                )
            
            return acoes.resposta_json(
                status='sucesso',
                mensagem='Registro atualizado com sucesso.'
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



def adicionar_afastamento_servidor(request, id_servidor):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            id_substituto = request.POST.get('id_substituto')
            em_afastamento = request.POST.get('em_afastamento') == '1'
            tipo_afastamento = request.POST.get('tipo_afastamento')
            data_inicio_afastamento = request.POST.get('data_inicio_afastamento')
            data_fim_afastamento = request.POST.get('data_fim_afastamento')

            servidor = Servidor.objects.get(id=id_servidor)

            if servidor.tipo != 'EFETIVO':
                return acoes.resposta_json(
                    status='erro',
                    mensagem='Apenas servidores EFETIVOS podem ser afastados e ter substituto.'
                )

            servidor.em_afastamento = em_afastamento

            if em_afastamento:
                servidor.tipo_afastamento = tipo_afastamento
                servidor.data_inicio_afastamento = data_inicio_afastamento
                servidor.data_fim_afastamento = data_fim_afastamento

                if id_substituto:
                    substituto = Servidor.objects.get(id=id_substituto)

                    if substituto.tipo != 'CONTRATADO':
                        return acoes.resposta_json(
                            status='erro',
                            mensagem='O substituto deve ser um servidor do tipo CONTRATADO.'
                        )

                    servidor.substituto = substituto
                else:
                    servidor.substituto = None  
            else:
                servidor.tipo_afastamento = None
                servidor.data_inicio_afastamento = None
                servidor.data_fim_afastamento = None
                servidor.substituto = None  

            servidor.save()

            return acoes.resposta_json(
                status='sucesso',
                mensagem='Afastamento atualizado com sucesso.'
            )

        except Servidor.DoesNotExist:
            return acoes.resposta_json(
                status='erro',
                mensagem='Servidor não encontrado.'
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


def excluir_servidor(request, id_servidor):
    if acoes.checar_tipo_requisicao(request, 'DELETE'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            num_deletados, _ = Servidor.objects.filter(campus_id=id_campus, id=id_servidor).delete()
            
            if num_deletados == 0:
                return acoes.resposta_json(status='erro', mensagem='Nenhum registro foi excluído.')
            
            return acoes.resposta_json(status='sucesso', mensagem='Registro excluído com sucesso!')

        except Exception as ex:
            return acoes.interpretar_erro_mysql(ex)
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido!'
        )
            
def adicionar_servidor(request):
    
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            
            dados = acoes.extrair_dados_da_requisicao(request, Servidor)
            
            try:
                dados['campus_id'] = acoes.obter_id_campus(request.user.email)
            except:
                return acoes.resposta_json(status='erro', mensagem='Usuário não autenticado')

            Servidor.objects.create(**dados)
            
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

def pesquisar_servidores(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            
            nome = request.GET.get('nome')
            afastado = request.GET.get('afastado')
            tipo = request.GET.get('tipo')
            id_cargo = request.GET.get('idCargo')
            id_setor = request.GET.get('idSetor')
            id_funcao = request.GET.get('idFuncao')
            id_area = request.GET.get('idArea')
            emPgd =  request.GET.get('em_pgd')
            
            id_campus = acoes.obter_id_campus(request.user.email)
            
            query = Servidor.objects.filter(campus_id=id_campus)
            
            if nome:
                query = query.filter(nome__icontains=nome)
            
            if afastado:
                query = query.filter(em_afastamento = afastado)
            
            if tipo:
                query = query.filter(tipo=tipo)
                
            if id_cargo:
                query = query.filter(cargo_id=id_cargo)  
            
            if id_setor:
                query = query.filter(setor_id=id_setor)
            
            if id_funcao:
                query = query.filter(funcao_id=id_funcao)
            
            if id_area:
                query = query.filter(cargo__area__id=id_area)
            
            if emPgd:
                query = query.filter(em_pgd=emPgd)
            
            servidores = query.values(
                'id',
                'nome',
                'matricula',
                'cargo__nome',
                'em_afastamento',
                'cargo__area__nome',
                'contrato__data_fim_contrato',
                'tipo',
                'funcao__nome',
                'setor__sigla',
                'data_exercicio',
                'data_cadastro'
            )

            hoje = date.today()
            
            for servidor in servidores:
                data_fim = servidor.get('contrato__data_fim_contrato')
                if data_fim:
                    servidor['dias_restantes'] = (data_fim - hoje).days
                else:
                    servidor['dias_restantes'] = 0

            return acoes.resposta_json(dados=list(servidores))
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
    