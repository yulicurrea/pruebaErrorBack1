import statistics
from http.client import responses
from telnetlib import STATUS
from urllib import response

from django.forms import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from .models import (Apropiacion, Articulos, AvanceProyecto, Notificaciones, Capitulos,
                     CategoriaMinciencias, Consultoria, Contenido, Contrato,
                     CuartilEsperado, EntidadPostulo, AvanceEntregableProducto ,  AvanceEntregableProyecto , 
                     EstadoProducto, EstadoProyecto, Estudiantes, Eventos, ConfiguracionEntregableProducto, ConfiguracionEntregableProyecto,
                     Financiacion, Grupoinvestigacion, Imagen, Industrial,
                     Investigador, Libros, Licencia, ListaProducto, Maestria,
                     ParticipantesExternos, Posgrado, PregFinalizadoyCurso,
                     Pregrado, Producto, Proyecto, Reconocimientos, Software,
                     TipoEventos, Transacciones, Ubicacion, UbicacionProyecto)
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
                         ubicacionSerializer)

#------------------------ investigador ------------------------

class investigadorList(generics.ListCreateAPIView):
    queryset = Investigador.objects.all()
    serializer_class = investigadorSerializer
    
class imagenList(generics.ListCreateAPIView):
    queryset = Imagen.objects.all()
    serializer_class = imagenSerializer

class grupoInvestigacionList(generics.ListCreateAPIView):
    queryset = Grupoinvestigacion.objects.all()
    serializer_class = grupoinvestigacionSerializer

class posgradoList(generics.ListCreateAPIView):
    queryset = Posgrado.objects.all()
    serializer_class = posgradoSerializer

class pregradoList(generics.ListCreateAPIView):
    queryset = Pregrado.objects.all()
    serializer_class = pregradoSerializer

class ubicacionList(generics.ListCreateAPIView):
    queryset = Ubicacion.objects.all()
    serializer_class = ubicacionSerializer

class investigadorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Investigador.objects.all()
    serializer_class = investigadorSerializer

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
        if request.data.get('EstadoProducto'):
            obj.estadoProducto = EstadoProducto.objects.get(pk=request.data.get('EstadoProducto'))
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
        notification_data = {
            'id': Notificaciones.objects.count() + 1,
            'asunto': request.data.get('asunto'),
            'remitente': request.data.get('remitente'),
            'destinatario': request.data.get('destinatario'),
            'mensaje': request.data.get('mensaje')
        }
        admin = Notificaciones.objects.create(**notification_data)
        serializer = notificacionesSerializer(admin) 

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class configuracionEntregableProductoList(generics.ListCreateAPIView):
    queryset = ConfiguracionEntregableProducto.objects.all()
    serializer_class = configuracionEntregableProductoSerializer
    
    def post(self, request, *args, **kwargs):
        admin_data = {
            'descripcion': request.data.get('descripcion'),
            'fecha': request.data.get('fecha'),
            'estado': request.data.get('estado'),
            'estadoProceso': request.data.get('estadoProceso'),
            'observacion': request.data.get('observacion'),
            'producto_id': Producto.objects.get(pk=request.data.get('producto_id_id')),
        }
        admin = ConfiguracionEntregableProducto.objects.create(**admin_data)
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
        obj = Notificaciones.objects.get(pk=request.data.get('id'))
        obj.estado = False
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
