from django.contrib.auth.models import User
from social_core.exceptions import AuthForbidden

def verifica_usuario_existente(strategy, details, backend, uid, user=None, *args, **kwargs):
    email = details.get('email')
    print("📧 E-MAIL recebido:", email)

    if not email:
        print("⚠️ Email não fornecido.")
        raise AuthForbidden(backend)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        print("⛔ Usuário não encontrado no banco:", email)
        raise AuthForbidden(backend)

    print("✅ Usuário autorizado:", user.username)
    return {'user': user}
