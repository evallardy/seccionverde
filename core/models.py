from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models

ACTIVIDAD = (
    (0, 'No'),
    (1, 'Si'),
)
ESTADOS = (
    ('Sin Estado', 'Sin Estado'),
    ('Aguascalientes', 'Aguascalientes'),
    ('Baja California', 'Baja California'),
    ('Baja California Sur', 'Baja California Sur'),
    ('Campeche', 'Campeche'),
    ('Coahuila', 'Coahuila'),
    ('Colima', 'Colima'),
    ('Chiapas', 'Chiapas'),
    ('Chihuahua', 'Chihuahua'),
    ('Ciudad de México', 'Ciudad de México'),
    ('Durango', 'Durango'),
    ('Guanajuato', 'Guanajuato'),
    ('Guerrero', 'Guerrero'),
    ('Hidalgo', 'Hidalgo'),
    ('Jalisco', 'Jalisco'),
    ('México', 'México'),
    ('Michoacán', 'Michoacán'),
    ('Morelos', 'Morelos'),
    ('Nayarit', 'Nayarit'),
    ('Nuevo León', 'Nuevo León'),
    ('Oaxaca', 'Oaxaca'),
    ('Puebla', 'Puebla'),
    ('Querétaro', 'Querétaro'),
    ('Quintana Roo', 'Quintana Roo'),
    ('San Luis Potosí', 'San Luis Potosí'),
    ('Sinaloa', 'Sinaloa'),
    ('Sonora', 'Sonora'),
    ('Tabasco', 'Tabasco'),
    ('Tamaulipas', 'Tamaulipas'),
    ('Tlaxcala', 'Tlaxcala'),
    ('Veracruz', 'Veracruz'),
    ('Yucatán', 'Yucatán'),
    ('Zacatecas', 'Zacatecas'),
)
ESTADOS_NUM = (
    ('Sin Estado', '0'),
    ('Aguascalientes', '1'),
    ('Baja California', '2'),
    ('Baja California Sur', '3'),
    ('Campeche', '4'),
    ('Coahuila', '5'),
    ('Colima', '6'),
    ('Chiapas', '7'),
    ('Chihuahua', '8'),
    ('Ciudad de México', '9'),
    ('Durango', '10'),
    ('Guanajuato', '11'),
    ('Guerrero', '12'),
    ('Hidalgo', '13'),
    ('Jalisco', '14'),
    ('México', '15'),
    ('Michoacán', '16'),
    ('Morelos', '17'),
    ('Nayarit', '18'),
    ('Nuevo León', '19'),
    ('Oaxaca', '20'),
    ('Puebla', '21'),
    ('Querétaro', '22'),
    ('Quintana Roo', '23'),
    ('San Luis Potosí', '24'),
    ('Sinaloa', '25'),
    ('Sonora', '26'),
    ('Tabasco', '27'),
    ('Tamaulipas', '28'),
    ('Tlaxcala', '29'),
    ('Veracruz', '30'),
    ('Yucatán', '31'),
    ('Zacatecas', '32'),
)
ESTATUS_ASESOR = (
    (1, 'Activo'),
    (3, 'Baja'),
)
ESTATUS_BIEN = (
    (1, 'Disponible'),
    (2, 'Apartado'),
    (3, 'Vendido'),
    (4, 'Reservado'),
    (9, 'Eliminado'),
)
ESTATUS_CLIENTE = (
    (1, 'Activo'),
    (2, 'Suspendido'),
    (3, 'Baja'),
)
ESTATUS_MENSAJE = (
    (0, 'Terminado'),
    (1, 'Activo'),
)
TIPO_ACCION = (
    (0, 'Sin acción'),
    (1, 'Comprar'),
    (2, 'Rentar'),
)
TIPO_BIEN = (
    (0, 'Sin tipo'),
    (1, 'Casa'),
    (2, 'Departamento'),
    (3, 'Local comercial'),
    (4, 'Terreno'),
)

class MensajePicky(models.Model, PermissionRequiredMixin):
    token = models.CharField("Token", max_length=255, null=True, blank=True)
    number = models.CharField("Number", max_length=50)                                 # Number
    message_in = models.CharField("Mensage in", max_length=255)                        # Message_in
    message_in_raw = models.CharField("Mensaje in raw", max_length=255)                # Message_in_raw
    message = models.CharField("Mensaje", max_length=255, null=True, blank=True)
    application = models.CharField("Aplicación", max_length=255, null=True, blank=True)# Application
    tipo = models.CharField("Type", max_length=255, default=2)                         # Tipo 
    unique_id = models.CharField("Unique id", max_length=255, null=True, blank=True)
    quoted = models.CharField("Quoted", max_length=255, null=True, blank=True)
    estatus_mensaje = models.IntegerField("Estatus del mensaje", choices=ESTATUS_MENSAJE, default=1)
    fecha_alta = models.DateTimeField("Fecha alta", auto_now_add=True)                 # fecha alta
    opcion0 = models.CharField("Acción", max_length=10, default='0')
    opcion1 = models.CharField("Opción Bien", max_length=10, default='0')
    opcion2 = models.CharField("Opción Estado", max_length=10, default='0')
    opcion2_texto = models.CharField("Opción Estado texto", max_length=40, default=' ', null=True, blank=True)
    opcion3 = models.CharField("Opción Municipio", max_length=100, default='0')
    opcion3_texto = models.CharField("Opción Municipio texto", max_length=200, default=' ', null=True, blank=True)

    class Meta:
        verbose_name = 'Mensaje picky'
        verbose_name_plural = 'Mensajes picky'
        ordering = ['id']
        db_table = 'MensajePicky'
        
class Menu(models.Model, PermissionRequiredMixin):
    seleccion = models.IntegerField("Selección")
    opcion = models.CharField("Opción", max_length=2)              #  opcion 1 menu 2 bienes
    descripcion = models.CharField("Descripción", max_length=255)
    
    class Meta:
        verbose_name = 'Opción Menú'
        verbose_name_plural = 'Opciones Menú'
        ordering = ['seleccion', 'opcion']
        db_table = 'Menu'
    
    def __str__(self):
        return '%s %s %s %s' % (self.id, self.seleccion, self.opcion, self.descripcion)

class Prueba(models.Model, PermissionRequiredMixin):
    descripcion = models.CharField("Descripción", max_length=255)
    fecha = models.TimeField("Fecha", auto_now_add=True)
    
    class Meta:
        verbose_name = 'Dato Prueba'
        verbose_name_plural = 'Datos pruebas'
        ordering = ['-fecha']
        db_table = 'Prueba'
    
    def __str__(self):
        return '%s - %s' % (self.fecha, self.descripcion)
    
class Bien(models.Model, PermissionRequiredMixin):
    calle = models.CharField("Calle", max_length=255)
    numero = models.CharField("Número", max_length=20)
    colonia = models.CharField("Colonia", max_length=255)
    municipio = models.CharField("Municipio", max_length=255)
    codigo_postal = models.CharField("Código postal", max_length=5)
    estado = models.CharField("Estado", max_length=35, choices=ESTADOS)
    longitud = models.CharField("Longitud", max_length=15, null=True, blank=True)
    latitud = models.CharField("Latitud", max_length=15, null=True, blank=True)
    tipo = models.IntegerField("Tipo bien", choices=TIPO_BIEN, default=0)
    compra = models.IntegerField("Compra", choices=ACTIVIDAD, default=0)
    renta = models.IntegerField("Renta", choices=ACTIVIDAD, default=0) 
    estatus_bien = models.IntegerField("Estatus", choices=ESTATUS_BIEN, default=1)

    class Meta:
        verbose_name = 'Bien'
        verbose_name_plural = 'Bienes'
        ordering = ['estado','municipio', 'colonia', 'calle','numero']
        db_table = 'Bien'
    
    def __str__(self):
        return '%s %s, %s %s, %s, %s, %s, %s, %s' % (self.calle, self.numero, self.colonia, self.codigo_postal, self.municipio, self.estado , self.compra, self.renta, self.tipo)
    
