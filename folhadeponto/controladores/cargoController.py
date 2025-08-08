
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from folhadeponto.models import Carreira, Cargo, Area
from folhadeponto.utilitarios import acoes
from django.db.models.functions import Upper, Trim

def listar_carreiras(id_campus):
    try:
        
        carreiras = Carreira.objects.filter(campus_id=id_campus).values("id", "nome").order_by("nome")
        
        return carreiras
    except Exception as e:
        print(f"Erro ao buscar carreiras: {e}")
        return {}
def listar_areas(id_campus):
    areas = Area.objects.filter(campus_id=id_campus).values('id', 'nome').order_by('nome')
    return areas

def ver_cargos(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        template = loader.get_template('cargos.html')
        id_campus = acoes.obter_id_campus(request.user.email)
        carreiras = list(listar_carreiras(id_campus))
        areas = list(listar_areas(id_campus))
    
        cargos = list(
            Cargo.objects.filter(campus_id=id_campus)
                .annotate(num_servidores=Count('servidor', distinct=True))  # Conta servidores distintos por cargo
                .values(
                    'id',
                    'nome',
                    'area__nome',
                    'nivel',
                    'data_cadastro',
                    'num_servidores',
                    'carreira__nome'
                )
        )
        dados_cargos = {
            'carreiras': carreiras,
            'cargos': cargos,
            'areas': areas
        }
        return HttpResponse(template.render(dados_cargos, request))
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')
 
def adicionar_cargo(request):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            dados = acoes.extrair_dados_da_requisicao(request, Cargo)
            try:
                id_campus =  acoes.obter_id_campus(request.user.email)
                dados['campus_id'] = id_campus
                nome_cargo = dados['nome'].strip().upper()
                id_area = dados['area_id']
                
                cargo_existe = Cargo.objects.annotate(nome_normalizado=Upper(Trim('nome'))).filter(
                    campus_id = id_campus,
                    nome_normalizado= nome_cargo,
                    area_id= id_area
                    ).first()
                
                if cargo_existe:
                    return acoes.resposta_json(status='erro', mensagem='O cargo já existe na área selecionada!')
                
                Cargo.objects.create(**dados)
                return acoes.resposta_json(status='sucesso', mensagem='Operação realizada com sucesso!')
            except Exception as ex:
                return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex))
        except Exception as e:
            return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(e))
    else:
        return acoes.resposta_json(status='erro', mensagem='Método não permitido.')


def excluir_cargo(request, id_cargo):
    if acoes.checar_tipo_requisicao(request, 'DELETE'):
        try:
            id_campus = acoes.obter_id_campus(request.user.email)
            num_deletados, _ = Cargo.objects.filter(campus_id=id_campus, id=id_cargo).delete()

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
                mensagem= acoes.interpretar_erro_mysql(e)
            )
    else:
        return acoes.resposta_json(
            status='erro',
            mensagem='Método não permitido.'
        )

def obter_cargo(request, id_cargo):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        id_campus = acoes.obter_id_campus(request.user.email)
        cargo = Cargo.objects.filter(campus_id=id_campus, id=id_cargo).values(
            'id',              
            'nome',             
            'nivel',           
            'data_cadastro',   
            'carreira__id',     
            'carreira__nome',
            'area__id',
            'area__nome',   
        ).first() 

        if not cargo:
            return acoes.resposta_json(
                status='erro',
                mensagem='Cargo não encontrado.'
            )

        return acoes.resposta_json(
            status='sucesso',
            mensagem='Operação realizada com sucesso!',
            dados=cargo
        )

    return acoes.resposta_json(
        status='erro',
        mensagem='Método não permitido.'
    )

def editar_cargo(request, id_cargo):
    if acoes.checar_tipo_requisicao(request, 'POST'):
        dados = acoes.extrair_dados_da_requisicao(request, Cargo)
        id_campus = acoes.obter_id_campus(request.user.email)
        registros_atualizados = Cargo.objects.filter(campus_id=id_campus, id=id_cargo).update(**dados)
        if registros_atualizados == 0:
            return acoes.resposta_json(status='erro', mensagem=f'Cargo não encontrado. id_campus: {id_campus}, id_cargo: {id_cargo}')
        return acoes.resposta_json(status='sucesso', mensagem='Operação realizada com sucesso!')
    return acoes.resposta_json(status='erro', mensagem='Método não permitido.')


def pesquisar_cargos(request):
    if acoes.checar_tipo_requisicao(request, 'GET'):
        try:
            nome = request.GET.get('nome','').strip()
            nivel = request.GET.get('nivel', '').strip()
            carreira = request.GET.get('carreira', '').strip()
            pgd = request.GET.get('pgd','').strip().lower()
            afastado = request.GET.get('afastado', '').strip().lower()
            tipo = request.GET.get('tipo', '').strip()


            id_campus = acoes.obter_id_campus(request.user.email)
            query = Cargo.objects.filter(campus_id=id_campus)
            
            if nome:
                query = query.filter(nome__icontains=nome)
                
            if nivel:
                query = query.filter(nivel=nivel)
            
            if afastado == '1':
                query =query.filter(servidor__em_afastamento = True)
            elif afastado == '0':
                query =query.filter(servidor__em_afastamento = False)
            
            if tipo:
                query =query.filter(servidor__tipo = tipo)
            
            if carreira:
                query = query.filter(carreira_id=carreira)
                
            if pgd == 'true':
                query = query.filter(servidor__em_pgd=True)
            elif pgd == 'false':
                query = query.filter(servidor__em_pgd=False)


            query = query.annotate(num_servidores=Count('servidor', distinct=True))
            
            cargos = query.values(
                'id',
                'nome',
                'nivel',
                'area__nome',
                'data_cadastro',
                'num_servidores',
                'carreira__nome'
            )

            return acoes.resposta_json(dados=list(cargos))

        except Exception as ex:
            return acoes.resposta_json(
                status='erro',
                mensagem=acoes.interpretar_erro_mysql(ex),
                dados=None
            )
    
    return acoes.resposta_json(status='erro', mensagem='Método não permitido.')



        

