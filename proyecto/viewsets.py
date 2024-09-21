import statistics
from dateutil import parser
import uuid

from http.client import responses
from telnetlib import STATUS
from urllib import response
from .utils import send_registration_email
from django.utils import timezone

from django.forms import ValidationError
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser


from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render
import logging
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.viewsets import ViewSet
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from .tokens_Inves import InvestigadorTokenGenerator


from .models import (Apropiacion, Articulos, AvanceProyecto, Notificaciones, Capitulos,
                     CategoriaMinciencias, Consultoria, Contenido, Contrato,
                     CuartilEsperado, EntidadPostulo, AvanceEntregableProducto ,  AvanceEntregableProyecto , 
                     EstadoProducto, EstadoProyecto, Estudiantes, Eventos, ConfiguracionEntregableProducto, ConfiguracionEntregableProyecto,
                     Financiacion, Grupoinvestigacion, Imagen, Industrial,
                     Investigador, Libros, Licencia, ListaProducto, Maestria,
                     ParticipantesExternos, Posgrado, PregFinalizadoyCurso,
                     Pregrado, Producto, Proyecto, Reconocimientos, Software,
                     TipoEventos, Transacciones, Ubicacion, UbicacionProyecto, PlanTrabajo,ConfiguracionPlanTrabajo)
from .serializer import (apropiacionSerializer, articulosSerializer,
                         avanceProyectoSerializer, notificacionesSerializer,capitulosSerializer,
                         categoriaMincienciasSerializer, consultoriaSerializer,
                         contenidoSerializer, contratoSerializer,
                         cuartilEsperadoSerializer, entidadPostuloSerializer, avanceEntregableProductoSerializer, avanceEntregableProyectoSerializer, 
                         estadoProductoSerializer, estadoProyecotSerializer, configuracionEntregableProductoSerializer, configuracionEntregableProyectoSerializer,
                         estudiantesSerializer, eventosSerializer,
                         financiacionSerializer, grupoinvestigacionSerializer,
                         imagenSerializer, industrialSerializer,
                         investigadorSerializer, librosSerializer,
                         licenciaSerializer, listaProductoSerializer,
                         maestriaSerializer, participantesExternosSerializer,
                         posgradoSerializer, pregFinalizadoyCursoSerializer,
                         pregradoSerializer, productoSerializer,
                         proyectoSerializer, reconocimientosSerializer,
                         softwareSerializer, tipoEventoSerializer,
                         transaccionesSerializer, ubicacionProyectoSerializer,
                         ubicacionSerializer, planTrabajoSerializer,configuracionPlanTrabajoSerializer)

#------------------------ investigador ------------------------

class investigadorList(generics.ListCreateAPIView):
    queryset = Investigador.objects.all()
    serializer_class = investigadorSerializer

   # Método que se llama cuando se crea un nuevo objeto Investigador
    def perform_create(self, serializer):
        # Guarda el nuevo objeto Investigador en la base de datos
        investigador = serializer.save()
        
        # Envía un correo de registro exitoso al investigador
        send_registration_email(investigador)
        
class imagenList(generics.ListCreateAPIView):
    queryset = Imagen.objects.all()
    serializer_class = imagenSerializer

class grupoInvestigacionList(generics.ListCreateAPIView):
    queryset = Grupoinvestigacion.objects.all()
    serializer_class = grupoinvestigacionSerializer

class posgradoList(generics.ListCreateAPIView):
    queryset = Posgrado.objects.all()
    serializer_class = posgradoSerializer
    
    def post(self, request, *args, **kwargs):
        data = {
            'Investigador_id': Investigador.objects.get(pk=request.data.get('investigadorId')),
            'institucion': request.data.get('institucion2'),
            'fecha': request.data.get('fecha2'),
            'titulo': request.data.get('titulo2'),
            'tipo': request.data.get('tipo2')
        }
        pregrado = Posgrado.objects.create(**data)
        serializer = posgradoSerializer(pregrado) 

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class pregradoList(generics.ListCreateAPIView):
    queryset = Pregrado.objects.all()
    serializer_class = pregradoSerializer
    
    def post(self, request, *args, **kwargs):
        data = {
            'Investigador_id': Investigador.objects.get(pk=request.data.get('investigadorId')),
            'institucion': request.data.get('institucion'),
            'fecha': request.data.get('fecha'),
            'titulo': request.data.get('titulo'),
        }
        pregrado = Pregrado.objects.create(**data)
        serializer = pregradoSerializer(pregrado) 

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ubicacionList(generics.ListCreateAPIView):
    queryset = Ubicacion.objects.all()
    serializer_class = ubicacionSerializer

class investigadorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Investigador.objects.all()
    serializer_class = investigadorSerializer
    
    def put(self, request, *args, **kwargs):
        obj = Investigador.objects.get(pk=request.data.get('numerodocumento'))
        obj.apellidos = request.data.get('apellidos')
        obj.correo = request.data.get('correo')
        obj.escalofonodocente = request.data.get('escalofonodocente')
        obj.horasestricto = 0 if request.data.get('horariosestrictos') is None else request.data.get('horariosestrictos')
        obj.horasformacion = 0 if request.data.get('horariosformacion') is None else request.data.get('horariosformacion')
        obj.lineainvestigacion = request.data.get('lineainvestigacion')
        obj.nombre = request.data.get('nombre')
        obj.tipodocumento = request.data.get('tipodocumento')
        obj.unidadAcademica = 'N/A' if request.data.get('unidadacademica') is None else request.data.get('unidadacademica')
        if request.data.get('estado') != None:
            obj.estado = request.data.get('estado')
        if request.data.get('rolinvestigador') != None:
            obj.rolinvestigador = request.data.get('rolinvestigador')
        obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class imagenRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Imagen.objects.all()
    serializer_class = imagenSerializer

class grupoInvestigacionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grupoinvestigacion.objects.all()
    serializer_class = grupoinvestigacionSerializer

class posgradoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posgrado.objects.all()
    serializer_class = posgradoSerializer

class pregradoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pregrado.objects.all()
    serializer_class = pregradoSerializer

class ubicacionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ubicacion.objects.all()
    serializer_class = ubicacionSerializer


#---------------------------- PRODUCTOS ----------------------------

class eventosList(generics.ListCreateAPIView):
    queryset = Eventos.objects.all()
    serializer_class = eventosSerializer

class articulosList(generics.ListCreateAPIView):
    queryset = Articulos.objects.all()
    serializer_class = articulosSerializer

class capitulosList(generics.ListCreateAPIView):
    queryset = Capitulos.objects.all()
    serializer_class = capitulosSerializer

class librosList(generics.ListCreateAPIView):
    queryset = Libros.objects.all()
    serializer_class = librosSerializer

class softwareList(generics.ListCreateAPIView):
    queryset = Software.objects.all()
    serializer_class = softwareSerializer

class industrialList(generics.ListCreateAPIView):
    queryset = Industrial.objects.all()
    serializer_class = industrialSerializer

class reconocimientosList(generics.ListCreateAPIView):
    queryset = Reconocimientos.objects.all()
    serializer_class = reconocimientosSerializer

class licenciaList(generics.ListCreateAPIView):
    queryset = Licencia.objects.all()
    serializer_class = licenciaSerializer

class apropiacionList(generics.ListCreateAPIView):
    queryset = Apropiacion.objects.all()
    serializer_class = apropiacionSerializer

class contratoList(generics.ListCreateAPIView):
    queryset = Contrato.objects.all()
    serializer_class = contratoSerializer

class consultoriaList(generics.ListCreateAPIView):
    queryset = Consultoria.objects.all()
    serializer_class = consultoriaSerializer

class contenidoList(generics.ListCreateAPIView):
    queryset = Contenido.objects.all()
    serializer_class = contenidoSerializer

class pregFinalizadoyCursoList(generics.ListCreateAPIView):
    queryset = PregFinalizadoyCurso.objects.all()
    serializer_class = pregFinalizadoyCursoSerializer

class maeestriaList(generics.ListCreateAPIView):
    queryset = Maestria.objects.all()
    serializer_class = maestriaSerializer

class listaProductoList(generics.ListCreateAPIView):
    queryset = ListaProducto.objects.all()
    serializer_class = listaProductoSerializer

class estudiantesList(generics.ListCreateAPIView):
    queryset = Estudiantes.objects.all()
    serializer_class = estudiantesSerializer

class productoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = productoSerializer

class participantesExternosList(generics.ListCreateAPIView):
    queryset = ParticipantesExternos.objects.all()
    serializer_class = participantesExternosSerializer

class tipoEventoList(generics.ListCreateAPIView):
    queryset = TipoEventos.objects.all()
    serializer_class = tipoEventoSerializer

class categoriaMincienciasList(generics.ListCreateAPIView):
    queryset = CategoriaMinciencias.objects.all()
    serializer_class = categoriaMincienciasSerializer

class cuartilEsperadoList(generics.ListCreateAPIView):
    queryset = CuartilEsperado.objects.all()
    serializer_class = cuartilEsperadoSerializer

class estadoProductoList(generics.ListCreateAPIView):
    queryset = EstadoProducto.objects.all()
    serializer_class = estadoProductoSerializer

class eventoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Eventos.objects.all()
    serializer_class = eventosSerializer

class articuloRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulos.objects.all()
    serializer_class = articulosSerializer

class capituloRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Capitulos.objects.all()
    serializer_class = capitulosSerializer

class libroRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libros.objects.all()
    serializer_class = librosSerializer

class softwareRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Software.objects.all()
    serializer_class = softwareSerializer

class industrialRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Industrial.objects.all()
    serializer_class = industrialSerializer

class reconocimientoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reconocimientos.objects.all()
    serializer_class = reconocimientosSerializer

class licenciaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Licencia.objects.all()
    serializer_class = licenciaSerializer

class apropiacionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Apropiacion.objects.all()
    serializer_class = apropiacionSerializer

class contratoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contrato.objects.all()
    serializer_class = contratoSerializer

class consultoriaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consultoria.objects.all()
    serializer_class = consultoriaSerializer

class contenidoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contenido.objects.all()
    serializer_class = contenidoSerializer

class pregFinalizadoyCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PregFinalizadoyCurso.objects.all()
    serializer_class = pregFinalizadoyCursoSerializer

class maeestriaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maestria.objects.all()
    serializer_class = maestriaSerializer

class listaProductoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ListaProducto.objects.all()
    serializer_class = listaProductoSerializer

class estudiantesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Estudiantes.objects.all()
    serializer_class = estudiantesSerializer

class productoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = productoSerializer
    
    def put(self, request, *args, **kwargs):
        obj = Producto.objects.get(pk=request.data.get('id'))
        if request.data.get('estadoProducto'):
            obj.estadoProducto = EstadoProducto.objects.get(pk=request.data.get('estadoProducto'))
        elif request.data.get('estado'):
            obj.estadoProducto = EstadoProducto.objects.get(pk=request.data.get('estado'))
        obj.estadoProceso = request.data.get('estadoProceso')
        obj.observacion = request.data.get('observacion')
        if request.data.get('type'):
            obj.tituloProducto = request.data.get('tituloProducto')
            obj.publicacion = request.data.get('publicacion')
            obj.cuartilEsperado = CuartilEsperado.objects.get(pk=request.data.get('cuartilEsperado'))
            obj.fecha = request.data.get('fechaProducto')
            obj.observaciones = request.data.get('observaciones')
            obj.origen = request.data.get('origenProyecto')
            obj.porcentajeComSemestral = request.data.get('porcentajeComSemestral')
            obj.porcentajeRealMensual = request.data.get('porcentajeRealMensual')
            obj.porcentanjeAvanFinSemestre = request.data.get('porcentanjeAvanFinSemestre')
            #coinvestigadores
            coinvestigadores_ids = request.data.get('coinvestigador')
            coinvestigadores = Investigador.objects.filter(numerodocumento__in=coinvestigadores_ids)
            obj.coinvestigador.set(coinvestigadores)  
            
            #estudiantes
            estudiantes_ids = request.data.get('estudiantes')
            estudiantes = Estudiantes.objects.filter(numeroDocumento__in=estudiantes_ids)
            obj.estudiantes.set(estudiantes)  
            
            #participantesExternos
            participantesExternos_ids = request.data.get('participantesExternosProducto')
            participantes_externos = ParticipantesExternos.objects.filter(numerodocumento__in=participantesExternos_ids)
            obj.participantesExternos.set(participantes_externos)  
            productoSerializer(obj)
        
        obj.save()
            
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------- PROYECTOS ----------------------------


class entidadPostuloList(generics.ListCreateAPIView):
    queryset = EntidadPostulo.objects.all()
    serializer_class = entidadPostuloSerializer
    
class avanceEntregableProductoList(generics.ListCreateAPIView):
    queryset = AvanceEntregableProducto.objects.all()
    serializer_class = avanceEntregableProductoSerializer
    parser_class = (FileUploadParser,)
    
    def post(self, request, *args, **kwargs):
        soporte = request.FILES.get('soporte')
        admin_data = {
            'url': request.data.get('url'),
            'fecha': request.data.get('fecha'),
            'estado': request.data.get('estado'),
            'configuracionEntregableProducto_id': ConfiguracionEntregableProducto.objects.get(pk=int(request.data.get('configuracionEntregableProducto_id_id'))),
        }
        avance = AvanceEntregableProducto.objects.create(**admin_data)
        if soporte:
            avance.soporte = soporte
            avance.save()

        serializer = avanceEntregableProductoSerializer(avance) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class avanceEntregableProyectoList(generics.ListCreateAPIView):
    queryset = AvanceEntregableProyecto.objects.all()
    serializer_class = avanceEntregableProyectoSerializer
    parser_class = (FileUploadParser,)
    
    def post(self, request, *args, **kwargs):
        soporte = request.FILES.get('soporte')
        admin_data = {
            'url': request.data.get('url'),
            'fecha': request.data.get('fecha'),
            'estado': request.data.get('estado'),
            'configuracionEntregableProyecto_id': ConfiguracionEntregableProyecto.objects.get(pk=int(request.data.get('configuracionEntregableProyecto_id_id'))),
        }
        avance = AvanceEntregableProyecto.objects.create(**admin_data)
        if soporte:
            avance.soporte = soporte
            avance.save()

        serializer = avanceEntregableProyectoSerializer(avance) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class financiacionList(generics.ListCreateAPIView):
    queryset = Financiacion.objects.all()
    serializer_class = financiacionSerializer

class transaccionesList(generics.ListCreateAPIView):
    queryset = Transacciones.objects.all()
    serializer_class = transaccionesSerializer

class ubicacionProyectoList(generics.ListCreateAPIView):
    queryset = UbicacionProyecto.objects.all()
    serializer_class = ubicacionProyectoSerializer

class avanceProyectoList(generics.ListCreateAPIView):
    queryset = AvanceProyecto.objects.all()
    serializer_class = avanceProyectoSerializer

class notificacionesList(generics.ListCreateAPIView):
    queryset = Notificaciones.objects.all()
    serializer_class = notificacionesSerializer
    
    def post(self, request, *args, **kwargs):
        # Preparar los datos de la nueva notificación
        notification_data = {
            'id': str(uuid.uuid4()),
            'asunto': request.data.get('asunto'),
            'remitente': request.data.get('remitente'),
            'destinatario': request.data.get('destinatario'),
            'mensaje': request.data.get('mensaje')
        }
        # Crear la nueva notificación
        admin = Notificaciones.objects.create(**notification_data)
        # Serializar la nueva notificación creada
        serializer = notificacionesSerializer(admin) 

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class configuracionEntregableProductoList(generics.ListCreateAPIView):
    queryset = ConfiguracionEntregableProducto.objects.all()
    serializer_class = configuracionEntregableProductoSerializer
    
    def post(self, request, *args, **kwargs):
        # Preparar los datos de la nueva configuración de entregable de producto
        admin_data = {
            'descripcion': request.data.get('descripcion'),
            'fecha': request.data.get('fecha'),
            'estado': request.data.get('estado'),
            'estadoProceso': request.data.get('estadoProceso'),
            'observacion': request.data.get('observacion'),
            'producto_id': Producto.objects.get(pk=request.data.get('producto_id_id')),
        }
        # Crear la nueva configuración de entregable de producto
        admin = ConfiguracionEntregableProducto.objects.create(**admin_data)
        # Serializar la nueva configuración creada
        serializer = configuracionEntregableProductoSerializer(admin) 

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class configuracionEntregableProductoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfiguracionEntregableProducto.objects.all()
    serializer_class =configuracionEntregableProductoSerializer
    
    def put(self, request, *args, **kwargs):
        obj = ConfiguracionEntregableProducto.objects.get(pk=request.data.get('id'))
        obj.estadoProceso = request.data.get('estadoProceso')
        obj.observacion = request.data.get('observacion')
        obj.estado = request.data.get('estado')
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class configuracionEntregableProyectoList(generics.ListCreateAPIView):
    queryset = ConfiguracionEntregableProyecto.objects.all()
    serializer_class = configuracionEntregableProyectoSerializer
    
    def post(self, request, *args, **kwargs):
        admin_data = {
            'descripcion': request.data.get('descripcion'),
            'fecha': request.data.get('fecha'),
            'estado': request.data.get('estado'),
            'estadoProceso': request.data.get('estadoProceso'),
            'observacion': request.data.get('observacion'),
            'proyecto_id': Proyecto.objects.get(pk=request.data.get('proyecto_id_id')),
        }
        admin = ConfiguracionEntregableProyecto.objects.create(**admin_data)
        serializer = configuracionEntregableProyectoSerializer(admin) 

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class configuracionEntregableProyectoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfiguracionEntregableProyecto.objects.all()
    serializer_class =configuracionEntregableProyectoSerializer
    
    def put(self, request, *args, **kwargs):
        obj = ConfiguracionEntregableProyecto.objects.get(pk=request.data.get('id'))
        obj.estadoProceso = request.data.get('estadoProceso')
        obj.observacion = request.data.get('observacion')
        obj.estado = request.data.get('estado')
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class estadoProyectoList(generics.ListCreateAPIView):
    queryset = EstadoProyecto.objects.all()
    serializer_class = estadoProyecotSerializer

class proyectoList(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = proyectoSerializer

class entidadPostuloRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntidadPostulo.objects.all()
    serializer_class = entidadPostuloSerializer

class financiacionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Financiacion.objects.all()
    serializer_class = financiacionSerializer

class transaccionesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transacciones.objects.all()
    serializer_class = transaccionesSerializer

class ubicacionProyectoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = UbicacionProyecto.objects.all()
    serializer_class = ubicacionProyectoSerializer

class avanceProyectoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AvanceProyecto.objects.all()
    serializer_class = avanceProyectoSerializer

class notificacionesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notificaciones.objects.all()
    serializer_class = notificacionesSerializer
    
    def put(self, request, *args, **kwargs):
         # Obtener el ID de la solicitud
        notification_id = kwargs.get('pk')

        try:
            # Obtener la notificación a actualizar usando el ID proporcionado en la solicitud
            obj = Notificaciones.objects.get(pk=notification_id)
        except Notificaciones.DoesNotExist:
            return Response({'detail': 'Notificación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar los datos de la notificación con el serializer
        serializer = self.serializer_class(obj, data=request.data, partial=True)  # partial=True permite actualizaciones parciales

        if serializer.is_valid():
            serializer.save()  # Guarda los cambios
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class avanceEntregableProductoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AvanceEntregableProducto.objects.all()
    serializer_class = avanceEntregableProductoSerializer
    
class avanceEntregableProyectoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AvanceEntregableProyecto.objects.all()
    serializer_class = avanceEntregableProyectoSerializer

class proyectoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = proyectoSerializer
    def put(self, request, *args, **kwargs):        
        obj = Proyecto.objects.get(pk=request.data.get('codigo'))
        obj.estadoProceso = request.data.get('estadoProceso')
        obj.estado = EstadoProyecto.objects.get(pk=request.data.get('estado'))
        obj.observacion = request.data.get('observacion')
        if request.data.get('type'):
            obj.titulo = request.data.get('titulo')
            obj.area = request.data.get('area')
            obj.convocatoria = request.data.get('convocatoria')
            obj.fecha = request.data.get('fecha')
            obj.grupoInvestigacionPro = request.data.get('grupoInvestigacionPro')
            obj.lineaInvestigacion = request.data.get('lineaInvestigacion')
            obj.modalidad = request.data.get('modalidad')
            obj.nivelRiesgoEtico = request.data.get('nivelRiesgoEtico')
            obj.origen = request.data.get('origen')
            obj.porcentajeAvance = request.data.get('porcentajeAvance')
            obj.porcentajeEjecucionCorte = request.data.get('porcentajeEjecucionCorte')
            obj.porcentajeEjecucionFinCorte = request.data.get('porcentajeEjecucionFinCorte')
            #coinvestigadores
            coinvestigadores_ids = request.data.get('coinvestigador')
            coinvestigadores = Investigador.objects.filter(numerodocumento__in=coinvestigadores_ids)
            obj.coinvestigador.set(coinvestigadores)  
            
            #estudiantes
            estudiantes_ids = request.data.get('estudiantesProyecto')
            estudiantes = Estudiantes.objects.filter(numeroDocumento__in=estudiantes_ids)
            obj.estudiantes.set(estudiantes)  
            
            #participantesExternos
            participantesExternos_ids = request.data.get('participantesExternos')
            participantes_externos = ParticipantesExternos.objects.filter(numerodocumento__in=participantesExternos_ids)
            obj.participantesExternos.set(participantes_externos)  
            productoSerializer(obj)
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--
logger = logging.getLogger(__name__)

token_generator = InvestigadorTokenGenerator()
class ResetPasswordSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    # Método de validación que verifica si el correo existe en la base de datos.
    def validate_correo(self, value):
        investigador = Investigador.objects.filter(correo=value).first()
        if not investigador:
            raise serializers.ValidationError('No se encontró un usuario con ese correo electrónico.')
        return value

class ResetPasswordViewSet(ViewSet):
    serializer_class = ResetPasswordSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        #Se obtiene el correo electronico proporcionado en la solicitud 
        correo = serializer.validated_data['correo']
        # Busca en la base de datos un usuario que tenga el correo electrónico proporcionado
        investigador = Investigador.objects.filter(correo=correo).first()
        # Si no se encuentra ese correo electrónico, se devuelve un mensaje de error indicando que el correo electrónico no está registrado.
        if not investigador:
            return Response({'error': 'El correo electrónico no está registrado.'}, status=status.HTTP_400_BAD_REQUEST)
        #Se genera un código temporal único que permite restablecer la contraseña y
        #se guarda en la memoria temporal del servidor (caché) durante un día (86400 segundos)
        token_temporal = token_generator.make_token(investigador)
        cache.set(token_temporal, correo, timeout=86400)
        #Se crea una dirección que puede visitar para restablecer su contraseña.
        # Esta URL contiene el código temporal generado
        reset_password_form_url = request.build_absolute_uri(reverse('reset-password-form', kwargs={'token_temporal': token_temporal}))
        #Se envia la plantilla de correo
        email_body = render_to_string('reset_password_email.html', {
            'investigador': investigador,
            'reset_password_form_url': reset_password_form_url,
        })
        #Se envía el correo electrónico al usuario.
        #Si ocurre algún problema durante el envío, se devuelve un mensaje de error
        try:
            send_mail('Restablecer Contraseña', email_body, 'osirisbioaxis@gmail.com', [investigador.correo], html_message=email_body)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': True}, status=status.HTTP_200_OK)

class ResetPasswordConfirmViewSet(ViewSet):
    def create(self, request):
        #Se obtienen los datos enviados en la solicitud
        token_temporal = request.data.get('token') #el token recibido por correo electrónico
        nueva_contraseña = request.data.get('nueva_contraseña') 
        confirmar_contraseña = request.data.get('confirmar_contraseña')
        #Se registranlos datos recibidos para seguimiento y depuración
        #Esto ayuda a monitorear lo que sucede en el sistema
        logger.debug(f"Token temporal recibido: {token_temporal}")
        logger.debug(f"Nueva contraseña recibida: {nueva_contraseña}")
        logger.debug(f"Confirmación de contraseña recibida: {confirmar_contraseña}")
        #Se verifica si alguno de los datos necesarios no está presente en la solicitud.
        if not token_temporal or not nueva_contraseña or not confirmar_contraseña:
            logger.error("Datos faltantes o inválidos.")
            return Response({'error': 'Datos faltantes o inválidos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar el token temporal
        # identifica al usuario que solicitó el cambio de contraseña
        correo = cache.get(token_temporal)
        if not correo:
            logger.error("Token inválido o expirado.")
            return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        #Si no se encuentra ningún usuario con ese correo electrónico en la base de datos, 
        # se devuelve un error indicando que el usuario no está encontrado
        try:
            investigador = Investigador.objects.get(correo=correo)
        except Investigador.DoesNotExist:
            logger.warning("Usuario no encontrado.")
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        #Verifica si la nueva_contraseña y confirmar_contraseña coinciden.
        if nueva_contraseña != confirmar_contraseña:
            logger.warning("Las contraseñas no coinciden.")
            return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)

        #Si todas las verificaciones son exitosas, se actualiza la contraseña en la base de datos
        # la función make_password para cifrar la nueva contraseña antes de guardarla.
        investigador.contrasena = make_password(nueva_contraseña)
        investigador.save()

        # Eliminar el token temporal de la caché
        cache.delete(token_temporal)
        logger.info("Contraseña cambiada correctamente.")

        return Response({'success': True}, status=status.HTTP_200_OK)

class ResetPasswordFormViewSet(ViewSet):
    #Este método se activa cuando se realiza una solicitud GET para obtener 
    # y mostrar el formulario de restablecimiento de contraseña.
    def retrieve(self, request, token_temporal, format=None):
        context = {'token_temporal': token_temporal}
        return render(request, 'reset_password_form.html', context)

class planTrabajoList(generics.ListCreateAPIView):
    queryset = PlanTrabajo.objects.all()
    serializer_class = planTrabajoSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)

        created_items = []
        for item in data:
            try:
                # Create new PlanTrabajo
                new_id = PlanTrabajo.objects.count() + 1
                admin_data = {
                    'id': str(new_id),
                    'rol': item.get('rol'),
                    'horasestricto': item.get('horasEstricto') or 0,
                    'investigador': Investigador.objects.get(pk=item.get('investigadorId')),
                    'proyecto': Proyecto.objects.get(pk=item.get('proyectoId')),
                    'producto': Producto.objects.get(pk=item.get('productoId')) if item.get('productoId') else None,
                }
                admin = PlanTrabajo.objects.create(**admin_data)
                serializer = planTrabajoSerializer(admin)
                created_items.append(serializer.data)
                
                # Get ConfiguracionPlanTrabajo and update it
                config_plan_id = item.get('configPlanTrabajoId')
                if config_plan_id:
                    config_plan = ConfiguracionPlanTrabajo.objects.get(pk=config_plan_id)
                    config_plan.planTrabajo.add(admin)
                    config_plan.save()

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_items, status=status.HTTP_201_CREATED)
    
    
    
class planTrabajoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanTrabajo.objects.all()
    serializer_class = planTrabajoSerializer

    def put(self, request, *args, **kwargs):
        obj = PlanTrabajo.objects.get(pk=kwargs['pk'])
        obj.rol = request.data.get('rol')
        obj.horasestricto = request.data.get('horasestricto')
        obj.save()
        return Response({"message": "Plan de trabajo actualizado correctamente."}, status=status.HTTP_200_OK)

class configuracionPlanTrabajoList(generics.ListCreateAPIView):
    queryset = ConfiguracionPlanTrabajo.objects.all()
    serializer_class = configuracionPlanTrabajoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        for config in queryset:
            if config.fecha < timezone.now().date():
                config.estado_fecha = False
                config.save()
        return queryset
    
    def post(self, request, *args, **kwargs):
        new_id = ConfiguracionPlanTrabajo.objects.count() + 1

        # Crear el objeto ConfiguracionPlanTrabajo sin el campo ManyToMany
        admin_data = {
            'id': str(new_id),
            'titulo': request.data.get('titulo'),
            'fecha': request.data.get('fecha'),
            'estado_manual': True,
            'estado_fecha': True,
        }
        admin = ConfiguracionPlanTrabajo.objects.create(**admin_data)
        
        # Agregar instancias de PlanTrabajo al campo ManyToMany
        plan_trabajos_ids = request.data.get('planTrabajo')
        if plan_trabajos_ids:
            for pt_id in plan_trabajos_ids:
                plan_trabajo = PlanTrabajo.objects.get(pk=pt_id)
                admin.planTrabajo.add(plan_trabajo)
        
        serializer = configuracionPlanTrabajoSerializer(admin)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class configuracionPlanTrabajoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfiguracionPlanTrabajo.objects.all()
    serializer_class = configuracionPlanTrabajoSerializer

    def get_object(self):
        obj = super().get_object()
        obj.actualizar_estado_fecha()
        return obj
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'estado_manual' in request.data:
            instance.estado_manual = request.data.get('estado_manual')
        
        # Actualiza solo los campos proporcionados
        if 'titulo' in request.data:
            instance.titulo = request.data.get('titulo')

        if 'fecha' in request.data:
            fecha_str = request.data.get('fecha')
            try:
                fecha_date = parser.parse(fecha_str).date()
                instance.fecha = fecha_date
                instance.actualizar_estado_fecha()
            except ValueError:
                return Response({"error": "Formato de fecha inválido"}, status=status.HTTP_400_BAD_REQUEST)

        instance.save()
        # Solo actualiza la relación ManyToMany si se proporciona una lista de IDs
        plan_trabajo_ids = request.data.get('planTrabajo', None)
        if plan_trabajo_ids is not None:
            instance.planTrabajo.set(plan_trabajo_ids)
        
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)





