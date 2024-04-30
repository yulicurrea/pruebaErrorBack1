from rest_framework import serializers

from .models import (Apropiacion, Articulos, AvanceProyecto, Notificaciones, Capitulos,
                     CategoriaMinciencias, Consultoria, Contenido, Contrato,
                     CuartilEsperado, EntidadPostulo, ConfiguracionEntregableProducto,
                    EstadoProducto, EstadoProyecto, AvanceEntregableProducto, 
                     Estudiantes, Eventos, Financiacion, Grupoinvestigacion, Imagen, AvanceEntregableProyecto, 
                     Industrial, Investigador, Libros, Licencia, ListaProducto, Maestria, ConfiguracionEntregableProyecto,
                     ParticipantesExternos, Posgrado, PregFinalizadoyCurso,
                     Pregrado, Producto, Proyecto, Reconocimientos, Software,
                     TipoEventos, Transacciones, Ubicacion, UbicacionProyecto)

#------------------------ investigador ------------------------

class investigadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigador
        fields = '__all__'

class imagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'
        
class ubicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class grupoinvestigacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupoinvestigacion
        fields = '__all__'

class pregradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregrado
        fields = '__all__'

class posgradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posgrado
        fields = '__all__'

#------------------------ PRODUCTOS ------------------------
class eventosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = '__all__'

class articulosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulos
        fields = '__all__'

class capitulosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulos
        fields = '__all__'

class librosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libros
        fields = '__all__'

class softwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = '__all__'

class industrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industrial
        fields = '__all__'

class reconocimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reconocimientos
        fields = '__all__'

class licenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licencia
        fields = '__all__'

class apropiacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apropiacion
        fields = '__all__'

class contratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'

class consultoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultoria
        fields = '__all__'

class contenidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenido
        fields = '__all__'

class pregFinalizadoyCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PregFinalizadoyCurso
        fields = '__all__'

class maestriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maestria
        fields = '__all__'

class listaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaProducto
        fields = '__all__'

class estudiantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiantes
        fields = '__all__'

class cuartilEsperadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuartilEsperado
        fields = '__all__'

class categoriaMincienciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaMinciencias
        fields = '__all__'

class tipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEventos
        fields = '__all__'

class participantesExternosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantesExternos
        fields = '__all__'

class estadoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoProducto
        fields = '__all__'
    
class productoSerializer(serializers.ModelSerializer):
    Soporte = serializers.FileField(required=False)
    class Meta:
        model = Producto
        fields = '__all__'
    

#------------------------ PROYECTOS ------------------------

class entidadPostuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntidadPostulo
        fields = '__all__'
        
class avanceEntregableProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvanceEntregableProducto
        fields = '__all__'
        
class avanceEntregableProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvanceEntregableProyecto
        fields = '__all__'

class financiacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financiacion
        fields = '__all__'

class transaccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacciones
        fields = '__all__'


class ubicacionProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbicacionProyecto
        fields = '__all__'

class avanceProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvanceProyecto
        fields = '__all__'
        
class notificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificaciones
        fields = '__all__'

class configuracionEntregableProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionEntregableProducto
        fields = '__all__'
        
class configuracionEntregableProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionEntregableProyecto
        fields = '__all__'


class estadoProyecotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoProyecto
        fields = '__all__'

class proyectoSerializer(serializers.ModelSerializer):
    coinvestigadores= investigadorSerializer(read_only=True, many=True)
    class Meta:
        model = Proyecto
        fields = '__all__'
    