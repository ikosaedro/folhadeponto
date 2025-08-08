from folhadeponto.utilitarios import acoes
from folhadeponto.controladores import contratoController, pefilController, areaController, usuarioController, cargoController, dataController, servidorController, setorController, funcaoController, carreiraController, folhaController

# Metódos de acesso
def tela_login(request):
    return acoes.tela_login(request)

def sair(request):
   return acoes.sair(request)

def efetuar_login(request):
    return acoes.efetuar_login(request)

def inicio(request):
    return acoes.inicio(request)

# Métodos para Model Usuario
def ver_usuarios(request):
    return acoes.checar_permissao_acesso_superuser(request, usuarioController.ver_usuarios)

def adicionar_usuario(request):
    return acoes.checar_permissao_acesso_superuser(request, usuarioController.adicionar_usuario)

def excluir_usuario(request, id_usuario):
    return acoes.checar_permissao_acesso_superuser(request, usuarioController.excluir_usuario, id_usuario)

def obter_usuario(request, id_usuario):
    return acoes.checar_permissao_acesso_superuser(request, usuarioController.obter_usuario, id_usuario)
 
def cadastrar_usuario_e_campus(request):
    return usuarioController.cadastrar_usuario_e_campus(request)


# Métodos para Model Servidor
def ver_servidores(request):
    return acoes.checar_permissao_acesso_superuser(request, servidorController.ver_servidores)

def obter_servidor(request, id_servidor):
    return acoes.checar_permissao_acesso_superuser(request, servidorController.obter_servidor, id_servidor)

def editar_servidor(request, id_servidor):
    return acoes.checar_permissao_acesso_superuser(request, servidorController.editar_servidor, id_servidor)

def excluir_servidor(request, id_servidor):
    return acoes.checar_permissao_acesso_superuser(request, servidorController.excluir_servidor, id_servidor)

def adicionar_servidor(request):
    return acoes.checar_permissao_acesso_superuser(request, servidorController.adicionar_servidor)

def pesquisar_servidores(request):
    return acoes.checar_permissao_acesso_superuser(request, servidorController.pesquisar_servidores, bloquear=False)

def adicionar_afastamento_servidor(request, id_servidor):
    return acoes.checar_permissao_acesso_superuser(request, servidorController.adicionar_afastamento_servidor, id_servidor)

# Métodos para Model Setor
def ver_setores(request):
    return acoes.checar_permissao_acesso_superuser(request, setorController.ver_setores)

def excluir_setor(request, id_setor):
    return acoes.checar_permissao_acesso_superuser(request, setorController.excluir_setor, id_setor)

def adicionar_setor(request):
    return acoes.checar_permissao_acesso_superuser(request, setorController.adicionar_setor)

def obter_setor(request, id_setor):
    return acoes.checar_permissao_acesso_superuser(request, setorController.obter_setor, id_setor)

def editar_setor(request, id_setor):
    return acoes.checar_permissao_acesso_superuser(request, setorController.editar_setor, id_setor)

def pesquisar_setores(request):
    return acoes.checar_permissao_acesso_superuser(request, setorController.pesquisar_setores, bloquear=False)


# Métodos para Model Cargo
def ver_cargos(request):
    return acoes.checar_permissao_acesso_superuser(request, cargoController.ver_cargos)

def adicionar_cargo(request):
    return acoes.checar_permissao_acesso_superuser(request, cargoController.adicionar_cargo)

def excluir_cargo(request, id_cargo):
    return acoes.checar_permissao_acesso_superuser(request, cargoController.excluir_cargo, id_cargo)

def obter_cargo(request, id_cargo):
    return acoes.checar_permissao_acesso_superuser(request, cargoController.obter_cargo, id_cargo)


def editar_cargo(request, id_cargo):
    return acoes.checar_permissao_acesso_superuser(request, cargoController.editar_cargo, id_cargo)
 
def pesquisar_cargos(request):
    return acoes.checar_permissao_acesso_superuser(request, cargoController.pesquisar_cargos, bloquear=False)

# Métodos para Model Funcao
def ver_funcoes(request):
    return acoes.checar_permissao_acesso_superuser(request, funcaoController.ver_funcoes)

def adicionar_funcao(request):
    return acoes.checar_permissao_acesso_superuser(request, funcaoController.adicionar_funcao)

def obter_funcao(request, id_funcao):
    return acoes.checar_permissao_acesso_superuser(request,funcaoController.obter_funcao, id_funcao )

def editar_funcao(request, id_funcao):
    return acoes.checar_permissao_acesso_superuser(request,funcaoController.editar_funcao, id_funcao )

def excluir_funcao(request, id_funcao):
    return acoes.checar_permissao_acesso_superuser(request,funcaoController.excluir_funcao, id_funcao )

def pesquisar_funcoes(request):
    return acoes.checar_permissao_acesso_superuser(request,funcaoController.pesquisar_funcoes)

# Métodos para Model Datas
def ver_datas(request):
    return acoes.checar_permissao_acesso_superuser(request, dataController.ver_datas)

def adicionar_data(request):
    return acoes.checar_permissao_acesso_superuser(request, dataController.adicionar_data)

def obter_data(request, id_data):
    return acoes.checar_permissao_acesso_superuser(request, dataController.obter_data, id_data)

def editar_data(request, id_data):
    return acoes.checar_permissao_acesso_superuser(request,dataController.editar_data, id_data)

def excluir_data(request, id_data):
    return acoes.checar_permissao_acesso_superuser(request, dataController.excluir_data, id_data)

def pesquisar_datas(request):
    return acoes.checar_permissao_acesso_superuser(request, dataController.pesquisar_datas)

# Métodos Model Carreira
def ver_carreiras(request):
    return acoes.checar_permissao_acesso_superuser(request, carreiraController.ver_carreiras)

def adicionar_carreiras(request):
    return acoes.checar_permissao_acesso_superuser(request, carreiraController.adicionar_carreira)

def editar_carreira(request, id_carreira):
    return acoes.checar_permissao_acesso_superuser(request,carreiraController.editar_carreira, id_carreira)

def obter_carreira(request, id_carreira):
    return acoes.checar_permissao_acesso_superuser(request, carreiraController.obter_cairreira, id_carreira)

def excluir_carreira(request, id_carreira):
    return acoes.checar_permissao_acesso_superuser(request,carreiraController.excluir_carreira, id_carreira )

def pesquisar_carreiras(request):
    return acoes.checar_permissao_acesso_superuser(request, carreiraController.pesquisar_carreiras, bloquear=False)

# Métodos para Model Folha
def ver_folhas(request):
    return acoes.checar_permissao_acesso_superuser(request, folhaController.ver_folhas, bloquear=False)

def emitir_folhas(request):
    return acoes.checar_permissao_acesso_superuser(request, folhaController.emitir_folhas, bloquear=False)

def obter_folha(request, folha_id):
    return acoes.checar_permissao_acesso_superuser(request, folhaController.obter_folha, folha_id, bloquear=False)

def adicionar_folha(request):
    return acoes.checar_permissao_acesso_superuser(request,folhaController.adicionar_folha, bloquear=False)

def pesquisar_folhas(request):
    return acoes.checar_permissao_acesso_superuser(request, folhaController.pesquisar_folhas, bloquear=False)

def excluir_folha(request, id_folha):
    return acoes.checar_permissao_acesso_superuser(request,folhaController.excluir_folha, id_folha, bloquear=False)

def obter_servidores_do_setor(request, id_setor):
    return acoes.checar_permissao_acesso_superuser(request, folhaController.obter_servidores_do_setor, id_setor, bloquear=False)

def obter_datas_mes_selecionado(request, mesAno):
    return acoes.checar_permissao_acesso_superuser(request, folhaController.obter_datas_mes_selecionado, mesAno, bloquear=False)

# Métodos Modelo Area 
def ver_areas(request):
    return acoes.checar_permissao_acesso_superuser(request, areaController.ver_areas)
   
def adicionar_area(request):
    return acoes.checar_permissao_acesso_superuser(request, areaController.adicionar_area)

def obter_area(request, id_area):
    return acoes.checar_permissao_acesso_superuser(request, areaController.obter_area, id_area)
    

def editar_area(request, id_area):
    return acoes.checar_permissao_acesso_superuser(request,areaController.editar_area, id_area)


def excluir_area(request, id_area):
    return acoes.checar_permissao_acesso_superuser(request, areaController.excluir_area, id_area)

def pesquisar_areas(request):
    return acoes.checar_permissao_acesso_superuser(request, areaController.pesquisar_areas)
   
# Métodos acesso Perfil 
def ver_perfil(request):
    return acoes.checar_permissao_acesso_superuser(request, pefilController.ver_perfil, bloquear=False)

# Métodos Modelo Contrato
def adicionar_contrato(request):
    return acoes.checar_permissao_acesso_superuser(request, contratoController.adicionar_contrato)

def obter_contrato(request, id_servidor):
    return acoes.checar_permissao_acesso_superuser(request, contratoController.obter_contrato, id_servidor)

def pesquisar_contratos(request):
    return acoes.checar_permissao_acesso_superuser(request, contratoController.pesquisar_servidores, bloquear=False)