from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_registration_email(user):
    subject = 'Registro exitoso'
    context = {
        'nombre': user.nombre, 
        'apellidos': user.apellidos,
        'correo': user.correo,
    }
    html_content = render_to_string('registration_email.html', context)
    text_content = strip_tags(html_content)  # Elimina las etiquetas HTML para obtener texto sin formato

    correo = EmailMultiAlternatives(subject, text_content, to=[user.correo])
    correo.attach_alternative(html_content, "text/html")  # Adjunta el contenido HTML
    correo.send()
