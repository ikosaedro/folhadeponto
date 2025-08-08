from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from django.contrib.auth.models import User


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

    TIPO_AFASTAMENTO_CHOICES = [
        ('1', 'Afastamento para Tratamento de Saúde'),
        ('2', 'Afastamento por Motivo de Doença em Pessoa da Família'),
        ('3', 'Afastamento para Serviço Militar'),
        ('4', 'Afastamento para Atividade Política'),
        ('5', 'Afastamento para Capacitação'),
        ('6', 'Afastamento para Pós-Graduação (Stricto Sensu)'),
        ('7', 'Afastamento para Missão ou Estudo no Exterior'),
        ('8', 'Afastamento para Atuar em Organismo Internacional'),
        ('9', 'Afastamento para Mandato Classista'),
        ('10', 'Afastamento por Prisão Preventiva ou Condenação Criminal'),
        ('11', 'Afastamento Preventivo em Processo Administrativo Disciplinar (PAD)'),
        ('12', 'Afastamento por Licença Maternidade, Paternidade ou Adoção'),
        ('13', 'Afastamento para Exercício de Mandato Eletivo'),]
 
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    setor = models.ForeignKey (
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
    tipo_afastamento = models.CharField(
        max_length=2,
        choices=TIPO_AFASTAMENTO_CHOICES,
        verbose_name="Tipo de Afastamento",
        null=True,  
        blank=True 
    )
    data_inicio_afastamento = models.DateField(null=True, blank=True)
    data_fim_afastamento = models.DateField(null=True, blank=True)
    
    TIPO_SERVIDOR = (
        ('EFETIVO', 'EFETIVO'),
        ('CONTRATADO', 'CONTRATADO'),
        )
    
    tipo = models.CharField(max_length=20, choices=TIPO_SERVIDOR, default='EFETIVO')
    em_afastamento = models.BooleanField(default=False)
    substituto = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        unique=True,
        null=True,
        blank=True,
        related_name='efetivo_substituido_por',
        limit_choices_to={'tipo': 'CONTRATADO'}
    )

    def clean(self):
        if self.substituto and self.substituto.tipo != 'CONTRATADO':
            raise ValidationError("O substituto deve ser um servidor do tipo CONTRATADO.")
        if self.tipo != 'EFETIVO' and self.substituto is not None:
            raise ValidationError("Somente servidores EFETIVOS podem ter substituto.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def pode_ter_substituto(self):
        return self.tipo == 'EFETIVO' and self.em_afastamento

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


class Contrato(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE, limit_choices_to={'tipo': 'CONTRATADO'}, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, default=None)
    data_inicio_contrato = models.DateField()
    data_fim_contrato = models.DateField()

    def __str__(self):
        return f"{self.servidor.nome}"

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