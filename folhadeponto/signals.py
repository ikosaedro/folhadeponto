from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Usuario

@receiver(post_save, sender=User)
def criar_ou_salvar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Cria o perfil Usuario ao criar o User
        Usuario.objects.create(user=instance)
    else:
        # Salva o perfil Usuario se existir
        if hasattr(instance, 'usuario'):
            instance.usuario.save()