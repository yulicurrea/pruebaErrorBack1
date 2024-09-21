from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_registration_email(user):
    # Define el asunto del correo electrónico
    subject = 'Registro exitoso'
    
    # Contexto para renderizar la plantilla
    context = {
        'nombre': user.nombre, 
        'apellidos': user.apellidos,
        'correo': user.correo,
    }
    
    # Renderiza el contenido HTML del correo utilizando la plantilla y el contexto
    html_content = render_to_string('registration_email.html', context)
    
    # Extrae el contenido de texto sin formato del HTML
    text_content = strip_tags(html_content)

    # Crea el correo electrónico con contenido alternativo
    correo = EmailMultiAlternatives(subject, text_content, to=[user.correo])
    
    # Adjunta el contenido HTML al correo
    correo.attach_alternative(html_content, "text/html")
    
    # Envía el correo
    correo.send()
