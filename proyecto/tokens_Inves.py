import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator # generar tokens de restablecimiento de contraseñas.
from .models import Investigador



class InvestigadorTokenGenerator(PasswordResetTokenGenerator):
    #Crea un valor hash único para el token usando el ID del investigador, su contraseña y tiempo.
    def _make_hash_value(self, investigador, timestamp):
        return six.text_type(investigador.pk) + investigador.contrasena + six.text_type(timestamp)

# Instancia del generador de tokens
token_generator = InvestigadorTokenGenerator()