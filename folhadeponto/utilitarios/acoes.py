
from django.http import JsonResponse
from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

@login_required(login_url='/login/')
def checar_permissao_acesso_superuser(request, funcao_callback, parametro=None, bloquear=True):
    if super_usuario(request):
        if parametro is not None:
            return funcao_callback(request, parametro)
        return funcao_callback(request)
    
    if not bloquear:
        if parametro is not None:
            return funcao_callback(request, parametro)
        return funcao_callback(request)
    
    return render(request,'restrito.html') 


def tela_login(request):
    
    if request.user.is_authenticated:
        redirect ('')
    return render (request, 'acesso/login.html')

def sair(request):
    if request.user.is_authenticated:
         logout(request)
    return render (request, 'acesso/login.html')

from django.contrib.auth import authenticate, login

def efetuar_login(request):
    if checar_tipo_requisicao(request, 'POST'):
        
        email = request.POST.get('txtEmail')
        senha = request.POST.get('txtSenha')

        user = authenticate(request, email=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect('inicio')  
        else:
            messages.error(request, 'E-mail ou senha inválidos.')

    return render(request, 'acesso/login.html')


        
@login_required(login_url='/login/')
def inicio(request):
    return render(request,'index.html')
  
def obter_tipo_requisicao(request):
    return request.method if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'] else None
    
# Função para verificar se o tipo de requisição HTTP corresponde ao esperado
def checar_tipo_requisicao(request, tipo):
    # Compara o método da requisição (GET, POST, etc.) com o tipo esperado
    if request.method == tipo:
        return True
    else:
        return False

from django.db import models

def obter_usuario(email):
    from django.contrib.auth.models import User
    from folhadeponto.models import Usuario
    try:
        user = User.objects.filter(email=email).first()
        return Usuario.objects.get(user=user)
    except (User.DoesNotExist, Usuario.DoesNotExist):
        return None

def obter_id_campus(email):
    usuario = obter_usuario(email)
    if not usuario or not usuario.campus:
        return None
    return usuario.campus.id

def obter_id_servidor_logado(request):
    from folhadeponto.models import Servidor
    servidor_id = Servidor.objects.filter(usuario__user_id=request.user.id).values_list('id', flat=True).first()
    return servidor_id


def extrair_dados_da_requisicao(request, modelo=None):
    # Inicializa dicionário para armazenar os dados extraídos
    dados = {}

    # Se não for passado um modelo, simplesmente retorna os campos do POST
    # Convertendo valores vazios ('') para None
    if not modelo:
        return {
            chave: (valor if valor != '' else None)
            for chave, valor in request.POST.items()
        }

    # Se o modelo for informado, percorre os campos do modelo
    for field in modelo._meta.get_fields():
        nome_campo = field.name

        # Trata campos ManyToMany: getlist sempre retorna lista (vazia ou não)
        if field.many_to_many:
            dados[nome_campo] = request.POST.getlist(nome_campo)

        # Campos normais e ForeignKeys
        elif field.concrete and not field.auto_created:

            # FOREIGN KEY
            if isinstance(field, models.ForeignKey):
                # Tenta obter o valor do campo_id ou campo
                valor_id = request.POST.get(f"{nome_campo}_id")
                valor_nome = request.POST.get(nome_campo)

                if valor_id is not None:
                    dados[f"{nome_campo}_id"] = valor_id if valor_id != '' else None
                elif valor_nome is not None:
                    dados[f"{nome_campo}_id"] = valor_nome if valor_nome != '' else None

            # CAMPOS SIMPLES
            else:
                if nome_campo in request.POST:
                    valor = request.POST[nome_campo]
                    dados[nome_campo] = valor if valor != '' else None

    # Retorna o dicionário final com os dados tratados
    return dados


# Função utilitária para padronizar a resposta JSON de uma view
def resposta_json(status='sucesso', mensagem='Operação realizada com sucesso!', dados=None, http_status=200):
    
    # Cria um dicionário base com status e mensagem da resposta
    resposta = {
        'status': status,        # Exemplo: 'sucesso' ou 'erro'
        'mensagem': mensagem     # Mensagem que será exibida ao cliente
    }

    # Se o parâmetro 'dados' for passado, mescla ele ao dicionário de resposta
    if dados:
        resposta['dados'] = dados 

    # Retorna a resposta como um JsonResponse com o status HTTP definido (padrão 200)
    return JsonResponse(resposta, status=http_status) 

def interpretar_erro_mysql(excecao):
    # Converte a exceção em string (pode ser útil para log ou análise adicional, se necessário)
    erro = str(excecao)

    # Dicionário que mapeia códigos de erro MySQL para mensagens amigáveis ao usuário
    erros_comuns = {
        1045: "Falha na autenticação. Verifique seu usuário ou senha.",                        # Erro de login (usuário/senha incorretos)
        1049: "Banco de dados não encontrado.",                                                # O banco informado não existe
        2003: "Não foi possível conectar ao servidor do banco de dados.",                     # Servidor não acessível
        1062: "Registro já existe. Dados duplicados não são permitidos.",                     # Violação de chave única (duplicidade)
        1451: "Não é possível excluir este item pois ele está relacionado a outros dados.",    # Violação de integridade referencial (chave estrangeira) ao excluir
        1452: "Não é possível salvar este item porque ele depende de outro dado que não existe.", # Violação de integridade referencial (chave estrangeira) ao inserir/atualizar
        1146: "Erro interno na estrutura de dados. Contate o suporte.",                        # Tabela não existe
        1054: "Erro de dados fornecidos. Por favor, verifique os campos informados.",          # Coluna não encontrada
        1366: "Valor incorreto para um campo. Verifique o formato dos dados.",                 # Valor de tipo incompatível (ex: string em campo numérico)
    }

    # Verifica se a exceção possui argumentos e se o primeiro argumento é o código de erro
    if hasattr(excecao, 'args') and isinstance(excecao.args, tuple):
        codigo_erro = excecao.args[0]  # Captura o código numérico do erro
        # Retorna a mensagem amigável com base no código, ou uma mensagem padrão se o código for desconhecido
        return erros_comuns.get(codigo_erro, "Ocorreu um erro inesperado ao acessar o banco de dados.")
    else:
        # Caso a exceção não tenha a estrutura esperada, retorna uma mensagem genérica
        return "Erro desconhecido ao processar a solicitação. Tente novamente mais tarde."

def validar_arquivo_imagens(value):
    if not value.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        raise ValidationError('Apenas arquivos PDF ou imagens são permitidos.')

def super_usuario(request):
    return request.user.is_superuser