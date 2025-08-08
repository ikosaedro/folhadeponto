from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from folhadeponto.models import Campus, Usuario, Servidor
from folhadeponto.utilitarios import acoes
from folhadeponto.controladores.setorController import listar_servidores
from folhadeponto.controladores.servidorController import obter_servidor
import json

def cadastrar_usuario_e_campus(request):
    
    if acoes.checar_tipo_requisicao(request, 'POST'):
        try:
            
            nome_campus = request.POST.get('nome')
            sigla_campus = request.POST.get('sigla')
            logo_campus = request.FILES.get('logo')
            
            nome_usuario = request.POST.get('nomeUsuario')
            email_usuario = request.POST.get('emailUsuario')
            senha = request.POST.get('senhaUsuario')
            confirmacao = request.POST.get('confirmacaoSenhaUsuario')
            
            if senha != confirmacao:
                return acoes.resposta_json(status='erro', mensagem='As senhas não coincidem.', dados= None)
            
            try:
                campus = Campus.objects.create(nome=nome_campus, sigla=sigla_campus, logo=logo_campus)
            except Exception as ex:
                return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex), dados= None)
            try:
                user = User.objects.create_user(username=email_usuario, email=email_usuario, password=senha,
                                        first_name=nome_usuario)
            except Exception as ex:
                return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex), dados= None)
            try:
                 Usuario.objects.create(user=user, campus=campus)
            except Exception as ex:
                return acoes.resposta_json(status='erro', mensagem=acoes.interpretar_erro_mysql(ex), dados= None)
            
            return acoes.resposta_json(status='sucesso', mensagem='Cadastro realizado com sucesso.', dados= None)
        except Exception as ex:
            return acoes.resposta_json(status='sucesso', mensagem=acoes.interpretar_erro_mysql(ex), dados= None)
        

def ver_usuarios(request):
    
    id_campus = acoes.obter_id_campus(request.user.email)
    servidores = listar_servidores(acoes.obter_id_campus(request.user.email))
    usuarios = Usuario.objects.filter(campus_id=id_campus).values(
        'id',
        'servidor__nome',
        'user__email',
        'user__is_superuser',
        'user__is_active',
        'data_cadastro'
    )
    
    dados = {
        'servidores': list(servidores),
        'usuarios':list(usuarios)
    }
    return render (request, 'usuarios.html', dados)

def excluir_usuario(request, id_usuario):
    if not acoes.checar_tipo_requisicao(request, 'DELETE'):
        return acoes.resposta_json(status='erro', mensagem='Requisição inválida.', dados=None)
    try:
        
        usuario = Usuario.objects.get(id = id_usuario)
        user = User.objects.get(id=usuario.user_id)
        
        usuario.delete()
        user.delete()
        
        return acoes.resposta_json(status='sucesso', mensagem='Cadastro realizado com sucesso.', dados= None)
    
    except Exception as ex:
        return acoes.resposta_json(
            status='erro',
            mensagem=str(ex),
            dados=None
        )

def obter_usuario(request, id_usuario):
    if not acoes.checar_tipo_requisicao(request, 'GET'):
        return acoes.resposta_json(status='erro', mensagem='Requisição inválida.', dados=None)
    try:
        
         usuario = Usuario.objects.filter(id = id_usuario).values(
             'id',
             'user__username',
             'user__email',
             'user__is_superuser',
             'user__is_active',
             'data_cadastro'
             ).first()
         
         return acoes.resposta_json(status='sucesso', mensagem='Usuário obtido com sucesso.', dados=usuario)
    except Exception as ex:
        return acoes.resposta_json(
            status='erro',
            mensagem=acoes.interpretar_erro_mysql(ex),
            dados=None
        )

def editar_usuario(request, id_usuario):
    if not acoes.checar_tipo_requisicao(request, 'POST'):
        return 

from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError

def adicionar_usuario(request):
    if not acoes.checar_tipo_requisicao(request, 'POST'):
        return acoes.resposta_json(status='erro', mensagem='Requisição inválida.', dados=None)

    try:
        id_campus = acoes.obter_id_campus(request.user.email)
        id_servidor = request.POST.get('servidor')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmacao = request.POST.get('confirmacaoSenha')
        tipo = request.POST.get('tipo') 

        if not all([id_servidor, email, senha, confirmacao]):
            return acoes.resposta_json(status='erro', mensagem='Todos os campos obrigatórios devem ser preenchidos.', dados=None)

        if senha != confirmacao:
            return acoes.resposta_json(status='erro', mensagem='As senhas não coincidem.', dados=None)

        if User.objects.filter(email=email).exists():
            return acoes.resposta_json(status='erro', mensagem='Este e-mail já está em uso.', dados=None)

        serv = Servidor.objects.get(id=id_servidor)

        if not serv:
            return acoes.resposta_json(status='erro', mensagem='Servidor não encontrado.', dados=None)

        if User.objects.filter(username=serv.nome).exists():
            return acoes.resposta_json(status='erro', mensagem='Já existe um usuário com este nome de usuário.', dados=None)

        tipo_bool = str(tipo).strip() == '1' 

        # Transação atômica
        with transaction.atomic():
            user = User.objects.create_user(
                username=serv.nome,
                email=email,
                password=senha,
                first_name=serv.nome
            )
            user.is_superuser = tipo_bool
            user.save()

            usuario = Usuario.objects.create(
                user=user,
                campus_id=id_campus,
                servidor=serv
            )

            # Vincula o usuário ao servidor
            serv.usuario = usuario
            serv.save()

        return acoes.resposta_json(
            status='sucesso',
            mensagem='Cadastro realizado com sucesso.',
            dados=None
        )

    except (ObjectDoesNotExist, ValidationError, IntegrityError) as ex:
        return acoes.resposta_json(
            status='erro',
            mensagem=acoes.interpretar_erro_mysql(ex),
            dados=None
        )
    except Exception as ex:
        return acoes.resposta_json(
            status='erro',
            mensagem='Erro inesperado: ' + str(ex),
            dados=None
        )


        




    