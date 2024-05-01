import datetime

from django.contrib.auth.hashers import make_password
from django.db import models, transaction
from rest_framework.authtoken.models import Token
from django.utils import timezone

# Se crean las clases para los modelos
# colocamos los atributos de la clase
# ----------------------- INVESTIGADOR -----------------------

class Grupoinvestigacion(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50)
    class Meta:
        db_table = 'proyecto_Grupoinvestigacion'

class Ubicacion(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    ciudad = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    class Meta:
        db_table = 'proyecto_Ubicacion'

class Imagen(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    imagen = models.ImageField(upload_to='uploads/', blank=True)
    class Meta:
        db_table = 'proyecto_Imagen'

class Investigador(models.Model):
    numerodocumento = models.CharField(max_length=50, primary_key=True)
    contrasena = models.CharField(max_length=128)  # se aumenta la longitud para almacenar la contraseña encriptada
    correo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    estado = models.BooleanField(default=False)
    imagen = models.ForeignKey(Imagen,null=False,blank=False,on_delete=models.CASCADE)
    apellidos = models.CharField(max_length=50)
    tipodpcumento = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('RC', 'Registro civil'),
        ('PA', 'Pasaporte'),
    ]
    tipodocumento = models.CharField(max_length=2, choices=tipodpcumento, default='CC')
    horasestricto = models.IntegerField(default=0)
    horasformacion = models.IntegerField(default=0)
    unidadAcademica = models.CharField(max_length=50)
    grupoinvestigacion = models.ForeignKey(Grupoinvestigacion,null=False,blank=False,on_delete=models.CASCADE)
    categoriaminciencias = [
        ("Emérito", "Eméritos"),
        ("Asociado", "Asociados"),
        ("Senior", "Senior"),
        ("Junior", "Junior"),
    ]
    categoriaminciencias = models.CharField(max_length=10, choices=categoriaminciencias, default='Junior')
    escalofonodocente = models.CharField(max_length=50)
    rolinvestigador = [
        ("Investigador", "Investigador"),
        ("Administrador", "Administrador"),
        ("Estudiante", "Estudiante"),
    ]
    rolinvestigador = models.CharField(max_length=50, choices=rolinvestigador, default='Investigador')
    lineainvestigacion = models.CharField(max_length=50)
    ies = models.CharField(max_length=50)
    ubicacion = models.ForeignKey(Ubicacion,null=False,blank=False,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def save(self, *args, **kwargs):
        if Investigador.objects.filter(pk=self.numerodocumento).exists():
            super().save(*args, **kwargs)        
        else:
            # Encriptar la contraseña antes de guardar el objeto Investigador
            self.contrasena = make_password(self.contrasena)    
            super().save(*args, **kwargs)

    def generate_token(self):
        token, created = Token.objects.get_or_create(user=self)  # Genera o recupera el token para este investigador
        return token.key 
    def deferred_setup():
        from rest_framework.authtoken.models import Token
    deferred_setup()
    class Meta:
        db_table = 'proyecto_Investigador'
        
class Posgrado(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    fecha = models.DateField(max_length=50)
    institucion = models.CharField(max_length=50)
    tipo = [
        ('Especialización', 'Especialización'),
        ('Maestría', 'Maestría'),
        ('Doctorado', 'Doctorado'),
        ('NA', 'No aplica')
    ]
    tipo = models.CharField(max_length=50, choices=tipo, default='NA')
    Investigador_id = models.ForeignKey(Investigador,null=False,blank=False,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_Posgrado'

class Pregrado(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    fecha = models.DateField(max_length=50)
    institucion = models.CharField(max_length=50)
    Investigador_id = models.ForeignKey(Investigador,null=False,blank=False,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_Pregrado'

#---------------------------------------------------------------------------------------
# ----------------------------------------------------- Producto -----------------------
#---------------------------------------------------------------------------------------

class TipoEventos(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField( max_length=150)
    class Meta:
        db_table = 'proyecto_TipoEventos'
    
class Eventos(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fechainicio = models.DateTimeField(default=datetime.datetime.now)
    fechafin = models.DateTimeField(default=datetime.datetime.now)
    numparticinerno = models.IntegerField(default=0)
    numparticexterno = models.IntegerField(default=0)
    tipoevento = models.ForeignKey(TipoEventos,null=False,blank=False,on_delete=models.CASCADE)
    class Meta:
        db_table = 'proyecto_Eventos'

class Articulos(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fuente = [
       ("Electronico", "Electronico"),
        ("Impreso", "Impreso"), 
    ]
    fuente = models.CharField(max_length=50, choices=fuente, default='Electronico')
    class Meta:
        db_table = 'proyecto_Articulos'
   
class Capitulos(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nombrepublicacion = models.CharField(max_length=50,default='NA')
    isbn = models.CharField(max_length=50,default='NA')
    fecha = models.DateTimeField(default=datetime.datetime.now)
    editorial = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Capitulos'

class Libros(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    isbn = models.CharField(max_length=50,default='NA')
    fecha = models.DateTimeField(default=datetime.datetime.now)
    editorial = models.CharField(max_length=50,default='NA')
    luegarpublicacion = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Libros'

class Software(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    tiporegistro = models.CharField(max_length=50,default='NA')
    numero = models.CharField(max_length=50,default='NA')
    fecha = models.DateTimeField(default=datetime.datetime.now)
    pais = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Software'

class Industrial(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fecha = models.DateTimeField(default=datetime.datetime.now)
    pais = models.CharField(max_length=50,default='NA')
    insitutofinanciador = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Industrial'

class Reconocimientos(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fecha = models.DateTimeField(default=datetime.datetime.now)
    nombentidadotorgada = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Reconocimientos'

class Licencia(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Licencia'

class Apropiacion(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fechainicio = models.DateTimeField(default=datetime.datetime.now)
    fechaFin = models.DateTimeField(default=datetime.datetime.now)
    licencia = models.ForeignKey(Licencia,null=False,blank=False,on_delete=models.CASCADE)
    formato = models.CharField(max_length=50,default='NA')
    medio = models.CharField(max_length=50,default='NA')
    nombreEntidad = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Apropiacion'

class Contrato(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=50,default='NA')
    numero = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Contrato'

class Consultoria(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    año = models.CharField(max_length=50,default='NA')
    contrato = models.ForeignKey(Contrato,null=False,blank=False,on_delete=models.CASCADE)
    nombreEntidad = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Consultoria'

class Contenido(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nombreEntidad = models.CharField(max_length=50,default='NA')
    paginaWeb = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Contenido'

class PregFinalizadoyCurso(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fechaInicio = models.DateTimeField(default=datetime.datetime.now)
    reconocimientos = models.CharField(max_length=50, blank=True,default='NA')
    numeroPaginas = models.IntegerField(blank=True,default='NA')
    class Meta:
        db_table = 'proyecto_Pregfinalizadoycurso'

class Maestria(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fechaInicio = models.DateTimeField(default=datetime.datetime.now)
    institucion = models.CharField(max_length=50,default='NA')
    class Meta:
        db_table = 'proyecto_Maestria'

class ListaProducto(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    articulo = models.ForeignKey(Articulos, null=True, blank=True, on_delete=models.CASCADE)
    capitulo = models.ForeignKey(Capitulos, null=True, blank=True, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, null=True, blank=True, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libros, null=True, blank=True, on_delete=models.CASCADE)
    prototipoIndustrial = models.ForeignKey(Industrial, null=True, blank=True, on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventos, null=True, blank=True, on_delete=models.CASCADE)
    reconocimiento = models.ForeignKey(Reconocimientos, null=True, blank=True, on_delete=models.CASCADE)
    consultoria = models.ForeignKey(Consultoria, null=True, blank=True, on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido, null=True, blank=True, on_delete=models.CASCADE)
    pregFinalizadoyCurso = models.ForeignKey(PregFinalizadoyCurso, null=True, blank=True, on_delete=models.CASCADE)
    apropiacion = models.ForeignKey(Apropiacion, null=True, blank=True, on_delete=models.CASCADE)
    maestria = models.ForeignKey(Maestria, null=True, blank=True, on_delete=models.CASCADE)
    proyectoCursoProducto = models.CharField(max_length=50, blank=True, null=True)
    proyectoFormuladoProducto = models.CharField(max_length=50, blank=True, null=True)
    proyectoRSUProducto = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'proyecto_Listaproducto'

class Estudiantes(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    semestre = models.IntegerField()
    fechaGrado = models.DateTimeField(default=datetime.datetime.now)
    codigoGrupo = models.CharField(max_length=50)
    tipoDocumento = [
        ("CC", "Cédula de ciudadanía"),
        ("TI", "Tarjeta de identidad"),
        ("CE", "Cédula de extranjería"),
        ("RC", "Registro civil"),
        ("PA", "Pasaporte"),
    ]
    tipoDocumento = models.CharField(max_length=50, choices=tipoDocumento, default='CC')
    numeroDocumento = models.CharField(max_length=50, primary_key=True)
    class Meta:
        db_table = 'proyecto_Estudiantes'

class ParticipantesExternos(models.Model):
    numerodocumento = models.CharField(max_length=50,primary_key=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    institucion = models.CharField(max_length=150)
    class Meta:
        db_table = 'proyecto_ParticipantesExternos'

class EstadoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=150)
    class Meta:
        db_table = 'proyecto_EstadoProducto'

class CategoriaMinciencias(models.Model):
    id = models.AutoField(primary_key=True)
    categoria=models.CharField(max_length=150)
    class Meta:
        db_table = 'proyecto_CategoriaMinciencias'

class CuartilEsperado(models.Model):
    id = models.AutoField(primary_key=True)
    cuartil=models.CharField(max_length=150)
    class Meta:
        db_table = 'proyecto_CuartilEsperado'

class Producto(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    tituloProducto = models.CharField(max_length=50)
    investigador = models.CharField(max_length=50)
    coinvestigador = models.ManyToManyField(Investigador)
    listaProducto = models.ForeignKey(ListaProducto,null=False,blank=False,on_delete=models.CASCADE)
    publicacion = models.CharField(max_length=50)
    estudiantes = models.ManyToManyField(Estudiantes)
    porcentanjeAvanFinSemestre= models.IntegerField()
    observaciones = models.CharField(max_length=1500)
    estadoProducto = models.ForeignKey(EstadoProducto,null=False,blank=False,on_delete=models.CASCADE)
    porcentajeComSemestral = models.IntegerField()
    porcentajeRealMensual = models.IntegerField()
    fecha = models.DateTimeField(default=datetime.datetime.now)
    origen = models.CharField(max_length=5000)
    observacion = models.CharField(max_length=5000,default='')
    Soporte = models.FileField(upload_to ='uploadsProducto/',max_length=1000, blank=True)
    estadoProceso = [
        ("Aprobado","Aprobado"),
        ("Rechazado","Rechazado"),
        ("Corregir","Corregir"),
        ("Espera","Espera")
    ]
    estadoProceso=models.CharField(max_length=50, choices=estadoProceso, default='Espera')
    cuartilEsperado=models.ForeignKey(CuartilEsperado,null=False,blank=False,on_delete=models.CASCADE)
    categoriaMinciencias=models.ForeignKey(CategoriaMinciencias,null=False,blank=False,on_delete=models.CASCADE)
    participantesExternos = models.ManyToManyField(ParticipantesExternos)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_Producto'


class ConfiguracionEntregableProducto(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)
    fecha = models.DateField()
    estado = models.BooleanField(default=True)
    estadoProceso = [
        ("Aprobado","Aprobado"),
        ("Rechazado","Rechazado"),
        ("Corregir","Corregir"),
        ("Espera","Espera")
    ]
    observacion = models.CharField(max_length=5000,default='')
    estadoProceso=models.CharField(max_length=50, choices=estadoProceso, default='Espera')
    producto_id = models.ForeignKey(Producto,null=False,blank=False,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_ConfiguracionEntregableProducto'
        
class AvanceEntregableProducto(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=250,blank=True)
    soporte = models.FileField(upload_to ='uploadsAvancesProducto/',max_length=1000, blank=True)
    fecha = models.DateField()
    estado = models.BooleanField(default=True)
    configuracionEntregableProducto_id = models.ForeignKey(ConfiguracionEntregableProducto,null=False,blank=False,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_AvanceEntregableProducto'



#---------------------------------------------------------------------------------------------------------
#--------------------------------------------------------- Proyecto -----------------------
#---------------------------------------------------------------------------------------------------

class EntidadPostulo(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nombreInstitucion = models.CharField(max_length=50)
    nombreGrupo = models.CharField(max_length=50)
    class Meta:
        db_table = 'proyecto_Entidadpostulo'

class Financiacion(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    valorPropuestoFin = models.CharField(max_length=50)
    valorEjecutadoFin = models.CharField(max_length=50)
    class Meta:
        db_table = 'proyecto_Financiacion'

class Transacciones(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fecha = models.DateTimeField()
    acta = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    class Meta:
        db_table = 'proyecto_Transacciones'

class UbicacionProyecto(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    instalacion = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    class Meta:
        db_table = 'proyecto_Ubicacionproyecto'

class EstadoProyecto(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=150)
    class Meta:
        db_table = 'proyecto_EstadoProyecto'

class Proyecto(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    fecha = models.DateTimeField()
    titulo = models.CharField(max_length=500)
    investigador = models.CharField(max_length=50)
    unidadAcademica =  models.CharField(max_length=50)
    producto = models.ForeignKey(Producto,null=True,blank=True,on_delete=models.CASCADE)
    coinvestigador = models.ManyToManyField(Investigador)
    area = models.CharField(max_length=50)
    porcentajeEjecucionCorte = models.IntegerField()
    entidadPostulo = models.ForeignKey(EntidadPostulo,null=False,blank=False,on_delete=models.CASCADE)
    financiacion = models.ForeignKey(Financiacion,null=False,blank=False,on_delete=models.CASCADE)
    grupoInvestigacionPro =  models.CharField(max_length=50)
    porcentajeEjecucionFinCorte = models.IntegerField()
    porcentajeAvance = models.IntegerField()
    observacion = models.CharField(max_length=5000,default='')
    Soporte = models.FileField(upload_to ='uploadsProducto/',max_length=1000, blank=True)
    transacciones = models.ForeignKey(Transacciones,null=False,blank=False,on_delete=models.CASCADE)
    origen = [
        ("nacional", "nacional"),
        ("internacional", "internacional"),
    ]
    origen = models.CharField(max_length=50, choices=origen, default='nacional')
    convocatoria = models.CharField(max_length=50)
    ubicacionProyecto = models.ForeignKey(UbicacionProyecto,null=False,blank=False,on_delete=models.CASCADE)
    estado =models.ForeignKey(EstadoProyecto,null=False,blank=False,on_delete=models.CASCADE)
    modalidad = [
        ("general", "general"),
        ("clinical", "clinical"),
        ("creación", "creación"),
    ]
    modalidad = models.CharField(max_length=50, choices=modalidad, default='general')
    nivelRiesgoEtico  = [
        ("Alto", "Alto"),
        ("Medio", "Medio"),
        ("Bajo", "Bajo"),
        ("Sin riesgo", "Sin riesgo"),
    ]
    nivelRiesgoEtico = models.CharField(max_length=50, choices=nivelRiesgoEtico, default='Sin riesgo')
    lineaInvestigacion =models.CharField(max_length=50)
    estadoProceso = [
        ("Aprobado","Aprobado"),
        ("Rechazado","Rechazado"),
        ("Corregir","Corregir"),
        ("Espera","Espera")
    ]
    estadoProceso=models.CharField(max_length=50, choices=estadoProceso, default='Espera')
    estudiantes = models.ManyToManyField(Estudiantes)
    participantesExternos = models.ManyToManyField(ParticipantesExternos)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_Proyecto'

class ConfiguracionEntregableProyecto(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)
    fecha = models.DateField()
    estado = models.BooleanField(default=False)
    estadoProceso = [
        ("Aprobado","Aprobado"),
        ("Rechazado","Rechazado"),
        ("Corregir","Corregir"),
        ("Espera","Espera")
    ]
    observacion = models.CharField(max_length=5000,default='')
    estadoProceso=models.CharField(max_length=50, choices=estadoProceso, default='Espera')
    proyecto_id = models.ForeignKey(Proyecto,null=False,blank=False,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_ConfiguracionEntregableProyecto'
        
class AvanceEntregableProyecto(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=250,blank=True)
    soporte = models.FileField(upload_to ='uploadsAvanceProyecto/',max_length=1000, blank=True)
    fecha = models.DateField()
    estado = models.BooleanField(default=False)
    configuracionEntregableProyecto_id = models.ForeignKey(ConfiguracionEntregableProyecto,null=False,blank=False,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_AvanceEntregableProyecto'

#--------------------------Actividades o avances ----------
class AvanceProyecto(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    reporte = models.CharField(max_length=50)
    entregablesComprometidos = models.CharField(max_length=50)
    entregablesReal = models.CharField(max_length=50)
    class Meta:
        db_table = 'proyecto_Avanceproyecto'
        
        
class Notificaciones(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    asunto = models.CharField(max_length=150)
    remitente = models.CharField(max_length=150)
    destinatario = models.CharField(max_length=150)
    mensaje = models.CharField(max_length=500)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        db_table = 'proyecto_Notificaciones'
