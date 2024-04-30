from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone, dateformat
import json
from datetime import datetime
from django.utils.timezone import make_aware
import ast

from .models import (Apropiacion, Articulos, Capitulos, Consultoria, Contenido,
                     Contrato, EntidadPostulo, EstadoProyecto,
                     Estudiantes, Eventos, Financiacion, Industrial, ConfiguracionEntregableProducto, ConfiguracionEntregableProyecto, 
                     Investigador, Libros, Licencia, ListaProducto, Maestria, AvanceEntregableProducto, AvanceEntregableProyecto,
                     PregFinalizadoyCurso, Producto, Proyecto, Reconocimientos,
                     Software, Transacciones, UbicacionProyecto, ParticipantesExternos, EstadoProducto,
                     CategoriaMinciencias,CuartilEsperado,TipoEventos)
from .serializer import (investigadorSerializer, productoSerializer,
                         proyectoSerializer)


class CustomAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('correo')
        password = request.data.get('contrasena')

        try:
            investigador = Investigador.objects.get(correo=email)
        except Investigador.DoesNotExist:
            print("Investigador no encontrado")
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar la contraseña
        print("Contraseña almacenada en la base de datos:", investigador.contrasena)
        if not check_password(password, investigador.contrasena):
            print("Contraseña incorrecta")
            print("Contraseña almacenada en la base de datos:", investigador.contrasena)
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generar tokens
        refresh = RefreshToken.for_user(investigador)
        access_token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'numerodocumento': investigador.numerodocumento,
            'rolinvestigador': investigador.rolinvestigador,
            'estado': investigador.estado
        }

        # Obtener y devolver datos del usuario
        user_data = {
            'nombre': investigador.nombre,
            'apellidos': investigador.apellidos,
            'correo': investigador.correo,
            'tipodocumento': investigador.tipodocumento,
            'numerodocumento': investigador.numerodocumento,
            'lineainvestigacion': investigador.lineainvestigacion,
            'escalofonodocente': investigador.escalofonodocente,
            'unidadacademica': investigador.unidadAcademica,
            'horariosformacion': investigador.horasformacion,
            'horariosestrictos': investigador.horasestricto,
            'tipPosgrado': {
                'id': investigador.tipPosgrado.id,
                'titulo': investigador.tipPosgrado.titulo,
                'fecha': investigador.tipPosgrado.fecha,
                'institucion': investigador.tipPosgrado.institucion,
                'tipo': investigador.tipPosgrado.tipo,
            },
            'tipPregrado': {
                'id': investigador.tipPregrado.id,
                'titulo': investigador.tipPregrado.titulo,
                'fecha': investigador.tipPregrado.fecha,
                'institucion': investigador.tipPregrado.institucion,
            },
        }
        return Response({'token': access_token, 'user_data': user_data}, status=status.HTTP_200_OK)

class ActualizarDatosUsuario(APIView):
    def put(self, request, *args, **kwargs):
        try:
            usuario = Investigador.objects.get(numerodocumento=request.data.get('numerodocumento'))
        except Investigador.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = investigadorSerializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CrearProyecto(APIView):

    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
        soporte = request.FILES.get('soporte')
        producto_data = request.data.get('producto')
        product_data_sale = json.loads(producto_data)

        producto_id = None
        if product_data_sale.get('id') != '':
            self.crearProductoPorProyecto(request)
            producto =  json.loads(request.data.get('producto'))
            producto_id = producto.get('id')        

        entidadPostulo_data= json.loads(request.data.get('entidadPostulo'))
        entidadPostulo_nombreIntitucion = entidadPostulo_data.get('nombreInstitucion')
        entidadPostulo_nombreGrupo = entidadPostulo_data.get('nombreGrupo')
        entidadPostulo,_=EntidadPostulo.objects.get_or_create(
            id=EntidadPostulo.objects.count()+1,
            nombreInstitucion=entidadPostulo_nombreIntitucion,
            nombreGrupo=entidadPostulo_nombreGrupo
        )
        
        financiacion_data = json.loads(request.data.get('financiacion'))
        financiacion_valorPropuestoFin = financiacion_data.get('valorPropuestoFin')
        financiacion_valorEjecutadoFin = financiacion_data.get('valorEjecutadoFin')
        financiacion,_=Financiacion.objects.get_or_create(
            id=Financiacion.objects.count()+1,
            valorPropuestoFin=financiacion_valorPropuestoFin,
            valorEjecutadoFin=financiacion_valorEjecutadoFin
        )

        transacciones_data = json.loads(request.data.get('transacciones'))
        transacciones_fecha=transacciones_data.get('fecha_transacciones')
        transacciones_acta=transacciones_data.get('acta')
        transacciones_descripcion=transacciones_data.get('descripcion')
        transacciones,_=Transacciones.objects.get_or_create(
            id=Transacciones.objects.count()+1,
            fecha=transacciones_fecha,
            acta=transacciones_acta,
            descripcion=transacciones_descripcion
        )

        ubicacionProyecto_data = json.loads(request.data.get('ubicacionProyecto'))
        ubicacionProyecto_instalacion= ubicacionProyecto_data.get('instalacion')
        ubicacionProyecto_municipio=ubicacionProyecto_data.get('municipio')
        ubicacionProyecto_pais=ubicacionProyecto_data.get('pais')
        ubicacionProyecto_departamento=ubicacionProyecto_data.get('departamento')
        ubicacionProyecto,_=UbicacionProyecto.objects.get_or_create(
            id=UbicacionProyecto.objects.count()+1,
            instalacion=ubicacionProyecto_instalacion,
            municipio=ubicacionProyecto_municipio,
            pais=ubicacionProyecto_pais,
            departamento=ubicacionProyecto_departamento
        )

        proyecto_data = {
            'codigo': request.data.get('codigo'),
            'fecha': make_aware(datetime.strptime(request.data.get('fecha'), "%Y-%m-%d")),
            'titulo': request.data.get('titulo'),
            'investigador': request.data.get('investigador'),
            'area': request.data.get('area'),
            'porcentajeEjecucionCorte': int(request.data.get('porcentajeEjecucionCorte')),
            'grupoInvestigacionPro': request.data.get('grupoInvestigacionPro'),
            'porcentajeEjecucionFinCorte': int(request.data.get('porcentajeEjecucionFinCorte')),
            'porcentajeAvance': int(request.data.get('porcentajeAvance')),
            'origen': request.data.get('origen'),
            'convocatoria': request.data.get('convocatoria'),
            'estado': EstadoProyecto.objects.get(pk=1),
            'modalidad': request.data.get('modalidadProyecto'),
            'nivelRiesgoEtico': request.data.get('nivelRiesgoEtico'),
            'lineaInvestigacion': request.data.get('lineaInvestigacion'),
            'estadoProceso': 'Espera',
            'unidadAcademica': request.data.get('unidadAcademica'),
            'producto': Producto.objects.get(pk=producto_id) if producto_id != None else None,
        }

        proyecto_data['entidadPostulo'] = entidadPostulo
        proyecto_data['financiacion'] = financiacion
        proyecto_data['transacciones'] = transacciones
        proyecto_data['ubicacionProyecto']=ubicacionProyecto

        proyecto = Proyecto.objects.create(**proyecto_data)  # Crea el objeto Proyecto con los datos relacionados

        # vinculación coinvestigadores
        coinvestigadores_base =request.data.get('coinvestigadores')
        coinvestigadores_proceso = str(coinvestigadores_base).split(',')

        coinvestigadores_ids = coinvestigadores_proceso
        coinvestigadores = Investigador.objects.filter(correo__in=coinvestigadores_ids)
        proyecto.coinvestigador.set(coinvestigadores)  # Asigna los coinvestigadores al proyecto usando set()     
        
        # vinculación estudiantes
        estudiantes_base =request.data.get('estudiantes')
        estudiantes_proceso = str(estudiantes_base).split(',')
        
        estudiantes_ids = estudiantes_proceso
        estudiantes = Estudiantes.objects.filter(numeroDocumento__in=estudiantes_ids)
        proyecto.estudiantes.set(estudiantes)
        
        # vinculación participantesExternos
        participantes_base =request.data.get('participantesExternos')
        participantes_proceso = str(participantes_base).split(',')

        participantesExternos_ids = participantes_proceso
        participantes_externos = ParticipantesExternos.objects.filter(numerodocumento__in=participantesExternos_ids)
        proyecto.participantesExternos.set(participantes_externos)

        if soporte:
            proyecto.Soporte = soporte
            proyecto.save()

        serializer = proyectoSerializer(proyecto)  # Serializa el proyecto creado

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def crearProductoPorProyecto(self, request):        
        soporte = request.data.get('soporteProducto')
        producto =  json.loads(request.data.get('producto'))
        list_producto = producto.get('listaProducto')

        coinvestiga_base =producto.get('coinvestigadoresProducto')
        items_coinvestiga = str(coinvestiga_base).replace("['", "").replace("']", "").replace("'", "").replace(" ", "")
        coinvestiga_fin = items_coinvestiga.split(',')
        
        estudiantes_base =producto.get('estudiantesProducto')
        items_estudiantes = str(estudiantes_base).replace("['", "").replace("']", "").replace("'", "").replace(" ", "")
        estudiantes_fin = items_estudiantes.split(',')

        participantes_base =producto.get('participantesExternosProducto')
        items_participantes = str(participantes_base).replace("['", "").replace("']", "").replace("'", "").replace(" ", "")
        participantes_fin = items_participantes.split(',')


        evento_data = list_producto.get('evento')
        evento = None
        if evento_data.get('fechainicio') != '':
            evento_fechainicio = evento_data.get('fechainicio')
            evento_fechafin = evento_data.get('fechafin')
            evento_numparticinerno = evento_data.get('numparticinerno')
            evento_numparticexterno = evento_data.get('numparticexterno')
            evento_tipoevento = evento_data.get('tipoevento')
            evento, _ = Eventos.objects.get_or_create(
                id=Eventos.objects.count() + 1,
                fechainicio=evento_fechainicio,
                fechafin=evento_fechafin,
                numparticinerno=evento_numparticinerno,
                numparticexterno=evento_numparticexterno,
                tipoevento=TipoEventos.objects.get(pk=int(evento_tipoevento))
            )

        articulo_data = list_producto.get('articulo')
        articulo = None
        if articulo_data.get('fuente') != '':
            articulo_fuente = articulo_data.get('fuente')
            articulo, _ = Articulos.objects.get_or_create(
                id=Articulos.objects.count() + 1,
                fuente=articulo_fuente
            )

        capitulo_data = list_producto.get('capitulo')
        capitulo = None
        if capitulo_data.get('nombrepublicacion') != '':
            capitulo_nombrepublicacion = capitulo_data.get('nombrepublicacion')
            capitulo_isbn = capitulo_data.get('isbn')
            capitulo_fecha = capitulo_data.get('fecha')
            capitulo_editorial = capitulo_data.get('editorial')
            capitulo, _ = Capitulos.objects.get_or_create(
                id=Capitulos.objects.count() + 1,
                nombrepublicacion=capitulo_nombrepublicacion,
                isbn=capitulo_isbn,
                fecha=capitulo_fecha,
                editorial=capitulo_editorial
            )

        libro_data = list_producto.get('libro')
        libro = None
        if libro_data.get('isbn') != '':
            libro_isbn = libro_data.get('isbn')
            libro_fecha = libro_data.get('fecha')
            libro_editorial = libro_data.get('editorial')
            libro_luegarpublicacion = libro_data.get('luegarpublicacion')
            libro, _ = Libros.objects.get_or_create(
                id=Libros.objects.count() + 1,
                isbn=libro_isbn,
                fecha=libro_fecha,
                editorial=libro_editorial,
                luegarpublicacion=libro_luegarpublicacion
            )

        software_data = list_producto.get('software')
        software = None
        if software_data.get('tiporegistro') != '':
            software_tiporegistro = software_data.get('tiporegistro')
            software_numero = software_data.get('numero')
            software_fecha = software_data.get('fecha')
            software_pais = software_data.get('pais')
            software, _ = Software.objects.get_or_create(
                id=Software.objects.count() + 1,
                tiporegistro=software_tiporegistro,
                numero=software_numero,
                fecha=software_fecha,
                pais=software_pais
            )

        prototipoIndustrial_data = list_producto.get('prototipoIndustrial')
        prototipoIndustrial = None
        if prototipoIndustrial_data.get('fecha') !='' :
            prototipoIndustrial_fecha = prototipoIndustrial_data.get('fecha')
            prototipoIndustrial_pais = prototipoIndustrial_data.get('pais')
            prototipoIndustrial_insitutofinanciador = prototipoIndustrial_data.get('insitutofinanciador')
            prototipoIndustrial, _ = Industrial.objects.get_or_create(
                id=Industrial.objects.count() + 1,
                fecha=prototipoIndustrial_fecha,
                pais=prototipoIndustrial_pais,
                insitutofinanciador=prototipoIndustrial_insitutofinanciador
            )

        reconocimiento_data = list_producto.get('reconocimiento')
        reconocimiento = None
        if reconocimiento_data.get('fecha') != '':
            reconocimiento_fecha = reconocimiento_data.get('fecha')
            reconocimiento_nombentidadotorgada = reconocimiento_data.get('nombentidadotorgada')
            reconocimiento, _ = Reconocimientos.objects.get_or_create(
                id=Reconocimientos.objects.count() + 1,
                fecha=reconocimiento_fecha,
                nombentidadotorgada=reconocimiento_nombentidadotorgada
            )

        consultoria_data = list_producto.get('consultoria')
        contrato = None
        consultoria = None
        if consultoria_data.get('año') != '':
            contrato_data = consultoria_data.get('contrato', {})
            contrato = None
            if contrato_data.get('nombre') != '':
                contrato_nombre = contrato_data.get('nombre')
                contrato_numero = contrato_data.get('numero')
                contrato, _ = Contrato.objects.get_or_create(
                    id=Contrato.objects.count() + 1,
                    nombre=contrato_nombre,
                    numero=contrato_numero
                )
            consultoria_ano = consultoria_data.get('año')
            consultoria_nombreEntidad = consultoria_data.get('nombreEntidad')
            consultoria, _ = Consultoria.objects.get_or_create(
                id=Consultoria.objects.count() + 1,
                año=consultoria_ano,
                contrato=contrato,
                nombreEntidad=consultoria_nombreEntidad
            )

        apropiacion_data = list_producto.get('apropiacion')
        licencias = None
        apropiacion = None
        if apropiacion_data.get('fechainicio') != '':
            licencia_data = apropiacion_data.get('licencia', {})
            licencias = None
            if licencia_data.get('nombre') != '':
                licencia_nombre = licencia_data.get('nombre')
                licencias, _ = Licencia.objects.get_or_create(
                    id=Licencia.objects.count() + 1,
                    nombre=licencia_nombre
                    )
            apropiacion_fechainicio = apropiacion_data.get('fechainicio')
            apropiacion_fechaFin = apropiacion_data.get('fechaFin')
            apropiacion_formato = apropiacion_data.get('formato')
            apropiacion_medio = apropiacion_data.get('medio')
            apropiacion_nombreEntidad = apropiacion_data.get('nombreEntidad')
            apropiacion, _ = Apropiacion.objects.get_or_create(
                id=Apropiacion.objects.count() + 1,
                fechainicio=apropiacion_fechainicio,
                fechaFin=apropiacion_fechaFin,
                licencia=licencias,
                formato=apropiacion_formato,
                medio=apropiacion_medio,
                nombreEntidad=apropiacion_nombreEntidad
                )

        contenido_data = list_producto.get('contenido')
        contenido = None
        if contenido_data.get('paginaWeb') != '':
            contenido_nombreEntidad = contenido_data.get('nombreEntidad')
            contenido_paginaWeb = contenido_data.get('paginaWeb')
            contenido, _ = Contenido.objects.get_or_create(
                id=Contenido.objects.count() + 1,
                nombreEntidad=contenido_nombreEntidad,
                paginaWeb=contenido_paginaWeb
            )

        pregFinalizadoyCurso_data = list_producto.get('pregFinalizadoyCurso')
        pregFinalizadoyCurso= None
        if pregFinalizadoyCurso_data.get('fechaInicio') != '':
            pregFinalizadoyCurso_fechaInicio= pregFinalizadoyCurso_data.get('fechaInicio')
            pregFinalizadoyCurso_reconocimientos= pregFinalizadoyCurso_data.get('reconocimientos')
            pregFinalizadoyCurso_numeroPaginas= pregFinalizadoyCurso_data.get('numeroPaginas')
            pregFinalizadoyCurso, _ = PregFinalizadoyCurso.objects.get_or_create(
                id=PregFinalizadoyCurso.objects.count() + 1,
                fechaInicio=pregFinalizadoyCurso_fechaInicio,
                reconocimientos=pregFinalizadoyCurso_reconocimientos,
                numeroPaginas=pregFinalizadoyCurso_numeroPaginas
            )   

        maestria_data = list_producto.get('maestria')
        maestria = None
        if maestria_data.get('fechaInicio') != '':
            maestria_fechaInicio = maestria_data.get('fechaInicio')
            maestria_institucion = maestria_data.get('institucion')
            maestria, _ = Maestria.objects.get_or_create(
                id=Maestria.objects.count() + 1,
                fechaInicio=maestria_fechaInicio,
                institucion=maestria_institucion
            )

        # Crear o obtener el objeto ListaProducto
        lista_producto_proyectoCursoProducto = list_producto.get('proyectoCursoProducto')
        lista_producto_proyectoFormuladoProducto = list_producto.get('proyectoFormuladoProducto')
        lista_producto_proyectoRSUProducto= list_producto.get('proyectoRSUProducto')
        lista_producto, _ = ListaProducto.objects.get_or_create(
            id=ListaProducto.objects.count() + 1,
            evento=evento,
            articulo=articulo,
            capitulo=capitulo,
            libro=libro,
            software=software,
            prototipoIndustrial=prototipoIndustrial,
            reconocimiento=reconocimiento,
            consultoria=consultoria,
            contenido=contenido,
            pregFinalizadoyCurso=pregFinalizadoyCurso,
            apropiacion=apropiacion,
            maestria=maestria,
            proyectoCursoProducto=lista_producto_proyectoCursoProducto,
            proyectoFormuladoProducto=lista_producto_proyectoFormuladoProducto,
            proyectoRSUProducto=lista_producto_proyectoRSUProducto
            )
        
        producto_data = {
            'id': producto.get('id'),
            'tituloProducto': producto.get('tituloProducto'),
            'investigador': producto.get('investigador'),
            'publicacion': producto.get('publicacion'),
            'porcentanjeAvanFinSemestre': producto.get('porcentanjeAvanFinSemestre'),
            'observaciones': producto.get('observaciones'),
            'estadoProducto': EstadoProducto.objects.get(pk=1),
            'estadoProceso': 'Espera',
            'porcentajeComSemestral': producto.get('porcentajeComSemestral'),
            'porcentajeRealMensual': producto.get('porcentajeRealMensual'),
            'fecha':  make_aware(datetime.strptime(producto.get('fecha'), "%Y-%m-%d")),
            'origen': producto.get('origen'),
            'categoriaMinciencias': CategoriaMinciencias.objects.get(pk=1),
            'cuartilEsperado': CuartilEsperado.objects.get(pk=1),
        }
        producto_data['listaProducto'] = lista_producto

        producto = Producto.objects.create(**producto_data) 
        # vinculación coinvestigadores
        coinvestigadores_ids = coinvestiga_fin
        coinvestigadores = Investigador.objects.filter(correo__in=coinvestigadores_ids)
        producto.coinvestigador.set(coinvestigadores)  # Asigna los coinvestigadores al proyecto usando set()     
        # vinculación estudiantes
        estudiantes_ids = estudiantes_fin
        estudiantes = Estudiantes.objects.filter(numeroDocumento__in=estudiantes_ids)
        producto.estudiantes.set(estudiantes)
        # vinculación participantesExternos
        participantesExternos_ids = participantes_fin
        participantes_externos = ParticipantesExternos.objects.filter(numerodocumento__in=participantesExternos_ids)
        producto.participantesExternos.set(participantes_externos)
        
        if soporte:
            producto.Soporte = soporte
            producto.save()
        
        serializer = productoSerializer(producto)
        
        return True

class CrearNuevoProducto(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        soporte = request.FILES.get('Soporte')
        lista_producto = json.loads(request.data.get('listaProducto'))
        data_general = lista_producto
        capitulo_data = data_general.get('capitulo')

        # Crear o obtener otros objetos relacionados según sea necesario
        # Crear o obtener objetos relacionados según sea necesario
        evento_data = data_general.get('evento')
        evento = None
        if evento_data.get('fechainicio') != '':
            evento_fechainicio = evento_data.get('fechainicio')
            evento_fechafin = evento_data.get('fechafin')
            evento_numparticinerno = evento_data.get('numparticinerno')
            evento_numparticexterno = evento_data.get('numparticexterno')
            evento_tipoevento = evento_data.get('tipoevento')
            evento, _ = Eventos.objects.get_or_create(
                id=Eventos.objects.count() + 1,
                fechainicio=evento_fechainicio,
                fechafin=evento_fechafin,
                numparticinerno=evento_numparticinerno,
                numparticexterno=evento_numparticexterno,
                tipoevento=TipoEventos.objects.get(pk=int(evento_tipoevento))
            )

        articulo_data = data_general.get('articulo')
        articulo = None
        if articulo_data.get('fuente') != '':
            articulo_fuente = articulo_data.get('fuente')
            articulo, _ = Articulos.objects.get_or_create(
                id=Articulos.objects.count() + 1,
                fuente=articulo_fuente
            )

        capitulo_data = data_general.get('capitulo')
        capitulo = None
        if capitulo_data.get('nombrepublicacion') != '':
            capitulo_nombrepublicacion = capitulo_data.get('nombrepublicacion')
            capitulo_isbn = capitulo_data.get('isbn')
            capitulo_fecha = capitulo_data.get('fecha')
            capitulo_editorial = capitulo_data.get('editorial')
            capitulo, _ = Capitulos.objects.get_or_create(
                id=Capitulos.objects.count() + 1,
                nombrepublicacion=capitulo_nombrepublicacion,
                isbn=capitulo_isbn,
                fecha=capitulo_fecha,
                editorial=capitulo_editorial
            )

        libro_data = data_general.get('libro')
        libro = None
        if libro_data.get('isbn') != '':
            libro_isbn = libro_data.get('isbn')
            libro_fecha = libro_data.get('fecha')
            libro_editorial = libro_data.get('editorial')
            libro_luegarpublicacion = libro_data.get('luegarpublicacion')
            libro, _ = Libros.objects.get_or_create(
                id=Libros.objects.count() + 1,
                isbn=libro_isbn,
                fecha=libro_fecha,
                editorial=libro_editorial,
                luegarpublicacion=libro_luegarpublicacion
            )

        software_data = data_general.get('software')
        software = None
        if software_data.get('tiporegistro') != '':
            software_tiporegistro = software_data.get('tiporegistro')
            software_numero = software_data.get('numero')
            software_fecha = software_data.get('fecha')
            software_pais = software_data.get('pais')
            software, _ = Software.objects.get_or_create(
                id=Software.objects.count() + 1,
                tiporegistro=software_tiporegistro,
                numero=software_numero,
                fecha=software_fecha,
                pais=software_pais
            )

        prototipoIndustrial_data = data_general.get('prototipoIndustrial')
        prototipoIndustrial = None
        if prototipoIndustrial_data.get('fecha') !='' :
            prototipoIndustrial_fecha = prototipoIndustrial_data.get('fecha')
            prototipoIndustrial_pais = prototipoIndustrial_data.get('pais')
            prototipoIndustrial_insitutofinanciador = prototipoIndustrial_data.get('insitutofinanciador')
            prototipoIndustrial, _ = Industrial.objects.get_or_create(
                id=Industrial.objects.count() + 1,
                fecha=prototipoIndustrial_fecha,
                pais=prototipoIndustrial_pais,
                insitutofinanciador=prototipoIndustrial_insitutofinanciador
            )

        reconocimiento_data = data_general.get('reconocimiento')
        reconocimiento = None
        if reconocimiento_data.get('fecha') != '':
            reconocimiento_fecha = reconocimiento_data.get('fecha')
            reconocimiento_nombentidadotorgada = reconocimiento_data.get('nombentidadotorgada')
            reconocimiento, _ = Reconocimientos.objects.get_or_create(
                id=Reconocimientos.objects.count() + 1,
                fecha=reconocimiento_fecha,
                nombentidadotorgada=reconocimiento_nombentidadotorgada
            )

        consultoria_data = data_general.get('consultoria')
        contrato = None
        consultoria = None
        if consultoria_data.get('año') != '':
            contrato_data = consultoria_data.get('contrato', {})
            contrato = None
            if contrato_data.get('nombre') != '':
                contrato_nombre = contrato_data.get('nombre')
                contrato_numero = contrato_data.get('numero')
                contrato, _ = Contrato.objects.get_or_create(
                    id=Contrato.objects.count() + 1,
                    nombre=contrato_nombre,
                    numero=contrato_numero
                )
            consultoria_ano = consultoria_data.get('año')
            consultoria_nombreEntidad = consultoria_data.get('nombreEntidad')
            consultoria, _ = Consultoria.objects.get_or_create(
                id=Consultoria.objects.count() + 1,
                año=consultoria_ano,
                contrato=contrato,
                nombreEntidad=consultoria_nombreEntidad
            )

        apropiacion_data = data_general.get('apropiacion')
        licencias = None
        apropiacion = None
        if apropiacion_data.get('fechainicio') != '':
            licencia_data = apropiacion_data.get('licencia', {})
            licencias = None
            if licencia_data.get('nombre') != '':
                licencia_nombre = licencia_data.get('nombre')
                licencias, _ = Licencia.objects.get_or_create(
                    id=Licencia.objects.count() + 1,
                    nombre=licencia_nombre
                    )
            apropiacion_fechainicio = apropiacion_data.get('fechainicio')
            apropiacion_fechaFin = apropiacion_data.get('fechaFin')
            apropiacion_formato = apropiacion_data.get('formato')
            apropiacion_medio = apropiacion_data.get('medio')
            apropiacion_nombreEntidad = apropiacion_data.get('nombreEntidad')
            apropiacion, _ = Apropiacion.objects.get_or_create(
                id=Apropiacion.objects.count() + 1,
                fechainicio=apropiacion_fechainicio,
                fechaFin=apropiacion_fechaFin,
                licencia=licencias,
                formato=apropiacion_formato,
                medio=apropiacion_medio,
                nombreEntidad=apropiacion_nombreEntidad
                )

        contenido_data = data_general.get('contenido')
        contenido = None
        if contenido_data.get('paginaWeb') != '':
            contenido_nombreEntidad = contenido_data.get('nombreEntidad')
            contenido_paginaWeb = contenido_data.get('paginaWeb')
            contenido, _ = Contenido.objects.get_or_create(
                id=Contenido.objects.count() + 1,
                nombreEntidad=contenido_nombreEntidad,
                paginaWeb=contenido_paginaWeb
            )

        pregFinalizadoyCurso_data = data_general.get('pregFinalizadoyCurso')
        pregFinalizadoyCurso= None
        if pregFinalizadoyCurso_data.get('fechaInicio') != '':
            pregFinalizadoyCurso_fechaInicio= pregFinalizadoyCurso_data.get('fechaInicio')
            pregFinalizadoyCurso_reconocimientos= pregFinalizadoyCurso_data.get('reconocimientos')
            pregFinalizadoyCurso_numeroPaginas= pregFinalizadoyCurso_data.get('numeroPaginas')
            pregFinalizadoyCurso, _ = PregFinalizadoyCurso.objects.get_or_create(
                id=PregFinalizadoyCurso.objects.count() + 1,
                fechaInicio=pregFinalizadoyCurso_fechaInicio,
                reconocimientos=pregFinalizadoyCurso_reconocimientos,
                numeroPaginas=pregFinalizadoyCurso_numeroPaginas
            )      

        maestria_data = data_general.get('maestria')
        maestria = None
        if maestria_data.get('fechaInicio') != '':
            maestria_fechaInicio = maestria_data.get('fechaInicio')
            maestria_institucion = maestria_data.get('institucion')
            maestria, _ = Maestria.objects.get_or_create(
                id=Maestria.objects.count() + 1,
                fechaInicio=maestria_fechaInicio,
                institucion=maestria_institucion
            )

        # Crear o obtener el objeto ListaProducto
        lista_producto_proyectoCursoProducto = data_general.get('proyectoCursoProducto')
        lista_producto_proyectoFormuladoProducto = data_general.get('proyectoFormuladoProducto')
        lista_producto_proyectoRSUProducto= data_general.get('proyectoRSUProducto')
        lista_producto, _ = ListaProducto.objects.get_or_create(
            id=ListaProducto.objects.count() + 1,
            evento=evento,
            articulo=articulo,
            capitulo=capitulo,
            libro=libro,
            software=software,
            prototipoIndustrial=prototipoIndustrial,
            reconocimiento=reconocimiento,
            consultoria=consultoria,
            contenido=contenido,
            pregFinalizadoyCurso=pregFinalizadoyCurso,
            apropiacion=apropiacion,
            maestria=maestria,
            proyectoCursoProducto=lista_producto_proyectoCursoProducto,
            proyectoFormuladoProducto=lista_producto_proyectoFormuladoProducto,
            proyectoRSUProducto=lista_producto_proyectoRSUProducto
            )
        

        producto_data = {
            'id': request.data.get('id'),
            'tituloProducto': request.data.get('tituloProducto'),
            'investigador': request.data.get('investigador'),
            'publicacion': request.data.get('publicacion'),
            'porcentanjeAvanFinSemestre': request.data.get('porcentanjeAvanFinSemestre'),
            'observaciones': request.data.get('observaciones'),
            'estadoProducto': EstadoProducto.objects.get(pk=1),
            'estadoProceso': 'Espera',
            'porcentajeComSemestral': request.data.get('porcentajeComSemestral'),
            'porcentajeRealMensual': request.data.get('porcentajeRealMensual'),
            'fecha':  make_aware(datetime.strptime(request.data.get('fecha'), "%Y-%m-%d")),
            'origen': request.data.get('origen'),
            'categoriaMinciencias': CategoriaMinciencias.objects.get(pk=1),
            'cuartilEsperado': CuartilEsperado.objects.get(pk=1),
        }
        producto_data['listaProducto'] = lista_producto

        producto = Producto.objects.create(**producto_data) 
        # vinculación coinvestigadores
        coinvestigadores_base =request.data.get('coinvestigadoresProducto')
        coinvestigadores_proceso = str(coinvestigadores_base).split(',')
        coinvestigadores_ids = coinvestigadores_proceso
        coinvestigadores = Investigador.objects.filter(correo__in=coinvestigadores_ids)
        producto.coinvestigador.set(coinvestigadores)  # Asigna los coinvestigadores al proyecto usando set()     
        # vinculación estudiantes
        estudiantes_base =request.data.get('estudiantesProducto')
        estudiantes_proceso = str(estudiantes_base).split(',')
        estudiantes_ids = estudiantes_proceso
        estudiantes = Estudiantes.objects.filter(numeroDocumento__in=estudiantes_ids)
        producto.estudiantes.set(estudiantes)
        # vinculación participantesExternos
        participantes_base =request.data.get('participantesExternosProducto')
        participantes_proceso = str(participantes_base).split(',')
        participantesExternos_ids = participantes_proceso
        participantes_externos = ParticipantesExternos.objects.filter(numerodocumento__in=participantesExternos_ids)
        producto.participantesExternos.set(participantes_externos)
        
        if soporte:
            producto.Soporte = soporte
            producto.save()
        
        serializer = productoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MostrarInvestigadores(APIView):
    def get(self, request, *args, **kwargs):
        investigadores = Investigador.objects.all()

        data = []
        for investigador in investigadores:
            proyectos = investigador.proyecto_set.all()
            productos = investigador.producto_set.all()
            
            proyectos_data = [{
                'codigo': proyecto.codigo,
                'fecha': proyecto.fecha,
                'titulo': proyecto.titulo,
                # otros campos del proyecto si los hay
            } for proyecto in proyectos]

            productos_data = [{
                'id': producto.id,
                'tituloProducto': producto.tituloProducto,
                # otros campos del producto si los hay
            } for producto in productos]
            
            investigador_data = {
                'nombre': investigador.nombre,
                'apellidos': investigador.apellidos,
                'correo': investigador.correo,
                'numerodocumento': investigador.numerodocumento,
                'Grupoinvestigacion':investigador.grupoinvestigacion.nombre,
                'created_at':investigador.created_at,
                'proyectos': proyectos_data,
                'productos': productos_data
                # otros campos del investigador si los hay
            }
            data.append(investigador_data)

        return JsonResponse(data, safe=False)
    

class MostrarProductos(APIView):
    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        data = []

        for producto in productos:
            # Información relacionada
            lista_producto = producto.listaProducto
            investigador = producto.investigador
            estudiantes = producto.estudiantes

            # Obtener información de la lista de productos
            articulo = lista_producto.articulo
            capitulo = lista_producto.capitulo
            software = lista_producto.software
            libro = lista_producto.libro
            prototipo_industrial = lista_producto.prototipoIndustrial
            evento = lista_producto.evento
            reconocimiento = lista_producto.reconocimiento
            consultoria = lista_producto.consultoria
            contenido = lista_producto.contenido
            preg_finalizado_curso = lista_producto.pregFinalizadoyCurso
            apropiacion = lista_producto.apropiacion
            maestria = lista_producto.maestria

            # Construir datos del producto y la información relacionada
            producto_data = {
                'id': producto.id,
                'titulo_producto': producto.tituloProducto,
                'publicacion': producto.publicacion,
                'estado_producto': producto.estadoProducto,
                'fecha': producto.fecha,
                #'soporte': producto.Soporte,
                'observaciones': producto.observaciones,
                'porcentanjeAvanFinSemestre': producto.porcentanjeAvanFinSemestre,
                'porcentaje_com_semestral': producto.porcentajeComSemestral,
                'porcentaje_real_mensual': producto.porcentajeRealMensual,
                'origen': producto.origen,
                'etapa': producto.etapa,
                'investigador': {
                    'nombre': investigador.nombre,
                    'apellidos': investigador.apellidos,
                    'numerodocumento': investigador.numerodocumento,
                    'Grupoinvestigacion': investigador.grupoinvestigacion.nombre,
                },
                'lista_producto': {
                    'proyectoCursoProducto': lista_producto.proyectoCursoProducto,
                    'proyectoFormuladoProducto': lista_producto.proyectoFormuladoProducto,
                    'proyectoRSUProducto': lista_producto.proyectoRSUProducto,
                    'articulo': {
                        'id': articulo.id,
                        'fuente': articulo.fuente,
                    } if articulo else None,
                    'capitulo': {
                        'id': capitulo.id,
                        'nombre_publicacion': capitulo.nombrepublicacion,
                        'isbn': capitulo.isbn,
                        'fecha': capitulo.fecha,
                        'editorial': capitulo.editorial,
                    } if capitulo else None,
                    'software': {
                        'id': software.id,
                        'tiporegistro': software.tiporegistro,
                        'numero': software.numero,
                        'fecha': software.fecha,
                        'pais': software.pais,
                    } if software else None,
                    'libro': {
                        'id': libro.id,
                        'isbn': libro.isbn,
                        'fecha': libro.fecha,
                        'editorial': libro.editorial,
                        'luegarpublicacion': libro.luegarpublicacion,
                    } if libro else None,
                    'prototipo_industrial': {
                        'id': prototipo_industrial.id,
                        'fecha': prototipo_industrial.fecha,
                        'pais': prototipo_industrial.pais,
                        'insitutofinanciador': prototipo_industrial.insitutofinanciador,
                    } if prototipo_industrial else None,
                    'evento': {
                        'id': evento.id,
                        'fechainicio': evento.fechainicio,
                        'fechafin': evento.fechafin,
                        'numparticinerno': evento.numparticinerno,
                        'numparticexterno': evento.numparticexterno,
                        'tipoevento': evento.tipoevento,
                    } if evento else None,
                    'reconocimiento': {
                        'id': reconocimiento.id,
                        'fecha': reconocimiento.fecha,
                        'nombentidadotorgada': reconocimiento.nombentidadotorgada,
                    } if reconocimiento else None,
                    'consultoria': {
                        'id': consultoria.id,
                        'ano': consultoria.año,
                        'contrato': {
                            'id': consultoria.contrato.id,
                            'nombre': consultoria.contrato.nombre,
                            'numero': consultoria.contrato.numero,
                        },
                        'nombre_entidad': consultoria.nombreEntidad,
                    } if consultoria else None,
                    'contenido': {
                        'id': contenido.id,
                        'nombre_entidad': contenido.nombreEntidad,
                        'pagina_web': contenido.paginaWeb,
                    } if contenido else None,
                    'preg_finalizado_curso': {
                        'id': preg_finalizado_curso.id,
                        'fecha_inicio': preg_finalizado_curso.fechaInicio,
                        'reconocimientos': preg_finalizado_curso.reconocimientos,
                        'numero_paginas': preg_finalizado_curso.numeroPaginas,
                    } if preg_finalizado_curso else None,
                    'apropiacion': {
                        'id': apropiacion.id,
                        'fechainicio': apropiacion.fechainicio,
                        'fecha_fin': apropiacion.fechaFin,
                        'licencia': {
                            'id': apropiacion.licencia.id,
                            'nombre': apropiacion.licencia.nombre,
                        },
                        'formato': apropiacion.formato,
                        'medio': apropiacion.medio,
                        'nombre_entidad': apropiacion.nombreEntidad,
                    } if apropiacion else None,
                    'maestria': {
                        'id': maestria.id,
                        'fecha_inicio': maestria.fechaInicio,
                        'institucion': maestria.institucion,
                    } if maestria else None,
                },
                'estudiantes': {
                    'nombres': estudiantes.nombres,
                    'apellidos': estudiantes.apellidos,
                    'semestre': estudiantes.semestre,
                    'fecha_grado': estudiantes.fechaGrado,
                    'codigo_grupo': estudiantes.codigoGrupo,
                    'tipo_documento': estudiantes.tipoDocumento,
                    'numero_documento': estudiantes.numeroDocumento,
                }
            }

            data.append(producto_data)

        return Response(data)
