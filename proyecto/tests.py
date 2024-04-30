from django.test import TestCase


# Create your tests here.
class CrearNuevoProducto(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        soporte = request.FILES.get('Soporte')
        data = request.data.get('producto')
        print("Datos resividos",data)

        # Extraer los datos de listaProducto
        lista_producto_data = data.get('listaProducto')
        

        # Crear o obtener otros objetos relacionados según sea necesario
        evento_data = lista_producto_data.get('evento', {})
        evento_id = evento_data.get('id')
        evento_fechainicio = evento_data.get('fechainicio')
        evento_fechafin = evento_data.get('fechafin')
        evento_numparticinerno = evento_data.get('numparticinerno')
        evento_numparticexterno = evento_data.get('numparticexterno')
        evento_tipoevento= evento_data.get('tipoevento')
        evento, _ = Eventos.objects.get_or_create(
            id=evento_id,
            fechainicio =evento_fechainicio,
            fechafin = evento_fechafin,
            numparticinerno = evento_numparticinerno,
            numparticexterno =evento_numparticexterno,
            tipoevento = evento_tipoevento
            )


        articulo_data = lista_producto_data.get('articulo', {})
        articulo_id = articulo_data.get('id')
        articulo_fuente = articulo_data.get('fuente')
        articulo, _ = Articulos.objects.get_or_create(
            id=articulo_id,
            fuente = articulo_fuente
            )
        
        capitulo_data = lista_producto_data.get('capitulo', {})
        capitulo_id = capitulo_data.get('id')
        capitulo_nombrepublicacion = capitulo_data.get('nombrepublicacion')
        capitulo_isbn = capitulo_data.get('isbn')
        capitulo_fecha = capitulo_data.get('fecha')
        capitulo_editorial = capitulo_data.get('editorial')
        capitulo,_= Capitulos.objects.get_or_create(
            id= capitulo_id,
            nombrepublicacion=capitulo_nombrepublicacion,
            isbn = capitulo_isbn,
            fecha = capitulo_fecha,
            editorial = capitulo_editorial
        )

        libro_data = lista_producto_data.get('libro', {})
        libro_id = libro_data.get('id')
        libro_isbn = libro_data.get('isbn')
        libro_fecha = libro_data.get('fecha')
        libro_editorial = libro_data.get('editorial')
        libro_luegarpublicacion = libro_data.get('luegarpublicacion')
        libro, _ = Libros.objects.get_or_create(
            id=libro_id,
            isbn=libro_isbn,
            fecha=libro_fecha,
            editorial=libro_editorial,
            luegarpublicacion=libro_luegarpublicacion
        )


        software_data = lista_producto_data.get('software', {})
        software_id = software_data.get('id')
        software_tiporegistro = software_data.get('tiporegistro')
        software_numero = software_data.get('numero')
        software_fecha = software_data.get('fecha')
        software_pais = software_data.get('pais')
        software, _ = Software.objects.get_or_create(
            id=software_id,
            tiporegistro=software_tiporegistro,
            numero=software_numero,
            fecha=software_fecha,
            pais=software_pais
            )


        prototipoIndustrial_data = lista_producto_data.get('prototipoIndustrial', {})
        prototipoIndustrial_id = prototipoIndustrial_data.get('id')
        prototipoIndustrial_fecha=prototipoIndustrial_data.get('fecha')
        prototipoIndustrial_pais=prototipoIndustrial_data.get('pais')
        prototipoIndustrial_insitutofinanciador=prototipoIndustrial_data.get('insitutofinanciador')
        prototipoIndustrial, _ = Industrial.objects.get_or_create(
            id=prototipoIndustrial_id,
            fecha=prototipoIndustrial_fecha,
            pais=prototipoIndustrial_pais,
            insitutofinanciador=prototipoIndustrial_insitutofinanciador
            )
        
        reconocimiento_data = lista_producto_data.get('reconocimiento', {})
        reconocimiento_id = reconocimiento_data.get('id')
        reconocimiento_fecha = reconocimiento_data.get('fecha')
        reconocimiento_nombentidadotorgada = reconocimiento_data.get('nombentidadotorgada')
        reconocimiento, _ = Reconocimientos.objects.get_or_create(
            id=reconocimiento_id,
            fecha=reconocimiento_fecha,
            nombentidadotorgada= reconocimiento_nombentidadotorgada
            )
       
        consultoria_data = lista_producto_data.get('consultoria', {})
        contrato_data = consultoria_data.get('contrato', {})
        contrato_id = contrato_data.get('id')
        contrato_nombre = contrato_data.get('nombre')
        contrato_numero = contrato_data.get('numero')
        contratos, _ = Contrato.objects.get_or_create(
            id=contrato_id,
            nombre=contrato_nombre,
            numero=contrato_numero
            )
        
        consultoria_id=consultoria_data.get('id')
        consultoria_ano= consultoria_data.get('año')
        consultoria_nombreEntidad = consultoria_data.get('nombreEntidad')
        consultoria, _ =Consultoria.objects.get_or_create(
            id=consultoria_id,
            año=consultoria_ano,
            contrato= contratos,
            nombreEntidad=consultoria_nombreEntidad
        )

        contenido_data = lista_producto_data.get('contenido', {})
        contenido_id = contenido_data.get('id')
        contenido_nombreEntidad = contenido_data.get('nombreEntidad')
        contenido_paginaWeb = contenido_data.get('paginaWeb')
        contenido, _ = Contenido.objects.get_or_create(
            id=contenido_id,
            nombreEntidad=contenido_nombreEntidad,
            paginaWeb=contenido_paginaWeb
            )

        pregFinalizadoyCurso_data = lista_producto_data.get('pregFinalizadoyCurso', {})
        pregFinalizadoyCurso_id = pregFinalizadoyCurso_data.get('id')
        pregFinalizadoyCurso_fechaInicio= pregFinalizadoyCurso_data.get('fechaInicio')
        pregFinalizadoyCurso_reconocimientos= pregFinalizadoyCurso_data.get('reconocimientos')
        pregFinalizadoyCurso_numeroPaginas= pregFinalizadoyCurso_data.get('numeroPaginas')
        pregFinalizadoyCurso, _ = PregFinalizadoyCurso.objects.get_or_create(
            id=pregFinalizadoyCurso_id,
            fechaInicio=pregFinalizadoyCurso_fechaInicio,
            reconocimientos=pregFinalizadoyCurso_reconocimientos,
            numeroPaginas=pregFinalizadoyCurso_numeroPaginas
            )       
        
        apropiacion_data = lista_producto_data.get('apropiacion', {})
        
        licencia_data = apropiacion_data.get('licencia', {})
        licencia_id = licencia_data.get('id')
        licencia_nombre = licencia_data.get('nombre')
        licencias, _ = Licencia.objects.get_or_create(
            id=licencia_id,
            nombre=licencia_nombre
            )

        apropiacion_id = apropiacion_data.get('id')
        apropiacion_fechainicio = apropiacion_data.get('fechainicio')
        apropiacion_fechaFin = apropiacion_data.get('fechaFin')
        apropiacion_formato = apropiacion_data.get('formato')
        apropiacion_medio = apropiacion_data.get('medio')
        apropiacion_nombreEntidad = apropiacion_data.get('nombreEntidad')
        apropiacion, _ = Apropiacion.objects.get_or_create(
            id=apropiacion_id,
            fechainicio=apropiacion_fechainicio,
            fechaFin=apropiacion_fechaFin,
            licencia=licencias,
            formato=apropiacion_formato,
            medio=apropiacion_medio,
            nombreEntidad=apropiacion_nombreEntidad
            )
        
        maestria_data = lista_producto_data.get('maestria', {})
        maestria_id = maestria_data.get('id')
        maestria_fechaInicio = maestria_data.get('fechaInicio')
        maestria_institucion = maestria_data.get('institucion')
        maestria, _ = Maestria.objects.get_or_create(
            id=maestria_id,
            fechaInicio=maestria_fechaInicio,
            institucion=maestria_institucion
            )

       # Crear o obtener el objeto ListaProducto
        lista_producto_id = lista_producto_data.get('id')
        lista_producto_proyectoCursoProducto = lista_producto_data.get('proyectoCursoProducto')
        lista_producto_proyectoFormuladoProducto = lista_producto_data.get('proyectoFormuladoProducto')
        lista_producto_proyectoRSUProducto= lista_producto_data.get('proyectoRSUProducto')
        lista_producto, _ = ListaProducto.objects.get_or_create(
            id=lista_producto_id,
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
            'id': data.get('id'),
            'tituloProducto': data.get('tituloProducto'),
            'investigador': data.get('investigador'),
            'publicacion': data.get('publicacion'),
            'estudiantes': data.get('estudiantes'),
            'estadoProdIniSemestre': data.get('estadoProdIniSemestre'),
            'porcentanjeAvanFinSemestre': data.get('porcentanjeAvanFinSemestre'),
            'observaciones': data.get('observaciones'),
            'estadoProducto': data.get('estadoProducto'),
            'porcentajeComSemestral': data.get('porcentajeComSemestral'),
            'porcentajeRealMensual': data.get('porcentajeRealMensual'),
            'fecha': data.get('fecha'),
            'origen': data.get('origen'),
        }
        producto_data['listaProducto'] = lista_producto.id

        serializer = productoSerializer(data=producto_data)
        if serializer.is_valid():
            producto = serializer.save()
            if soporte:  # Verifica si se envió un archivo
                producto.Soporte = soporte  # Asigna el archivo al campo 'Soporte'
                producto.save()  # Guarda el producto con el archivo

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
