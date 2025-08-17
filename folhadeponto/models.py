from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from django.contrib.auth.models import User
from folhadeponto.utilitarios.acoes import validar_arquivo_imagens


class Campus(models.Model):
    
    nome = models.CharField(max_length=191, unique=True)
    sigla = models.CharField(max_length=191, unique=True)
    logo = models.FileField(upload_to='logoscampi/', null=True, blank=True)
    data_cadastro = models.DateTimeField(default=now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        return self.nome

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null= True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null= True, blank=True)
    data_cadastro = models.DateTimeField(default=now, null=True)

    def __str__(self):
        return self.user.username
      
       
class Carreira(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=191, null=False, unique=True)
    data_cadastro = models.DateTimeField(default=now)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        return self.nome

class Area(models.Model):
     
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=191, null=False, unique=True)
    data_cadastro = models.DateTimeField(default=now)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        return self.nome
    
class Cargo(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT, null=True, blank=True)
    carreira = models.ForeignKey(Carreira, on_delete=models.PROTECT, null= False)
    nome = models.CharField(max_length=191, null=False, unique=False)
    nivel = models.CharField(max_length=191, null=False)
    data_cadastro = models.DateTimeField(default=now)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        return self.nome

class Funcao(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=191, null=False, unique=True)
    sigla = models.CharField(max_length=30, null=True, blank=True, unique=False)
    data_cadastro = models.DateTimeField(default=now)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        return self.nome
    
class Data(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=191, null=False)
    data  = models.DateField(max_length=191, null=False, unique=True)
    tipo = models.CharField(max_length=191)
    abrangencia = models.CharField(max_length=191, null=True, blank=True)
    data_cadastro = models.DateTimeField(default=now)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        return f"{self.data.strftime("%d/%m/%y")} - {self.nome}"

class Servidor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    setor = models.ForeignKey(
        'Setor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='servidores' 
    )
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    funcao = models.ForeignKey(Funcao, on_delete=models.SET_NULL, blank=True, null=True)
    nome = models.CharField(max_length=191)
    matricula = models.CharField(max_length=191, unique=True)
    situacao = models.BooleanField(default=True)
    em_pgd = models.BooleanField(default=False)
    data_exercicio = models.DateField()
    data_cadastro = models.DateTimeField(default=now)

    def __str__(self):
        return self.nome

class Setor(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    responsavel = models.ForeignKey(
        Servidor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='setores_que_coordena'  
    )
    nome = models.CharField(max_length=191, unique=True)
    sigla = models.CharField(max_length=191, unique=True)
    data_cadastro = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


    
class Folha(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    mes_ano = models.CharField(max_length=50)
    dados = models.TextField(null=False)
    setor_mes_ano = models.CharField(max_length=191, editable=False, unique=True)
    data_cadastro = models.DateTimeField(default=now)
 
    def save(self, *args, **kwargs):
        self.setor_mes_ano = f"{self.setor.nome} - {self.mes_ano}"
        super().save(*args, **kwargs)