from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from django.http import JsonResponse
import json

@api_view(['POST','GET','PULL','PUT','PATCH','DELETE'])
def mensaje_api_view(request):
    # Guardado de la información que llega tanto el meodo como la información
    prueba = Prueba(descripcion = "pruebas " + request.method)
    prueba.save()
    prueba = Prueba(descripcion = json.dumps(request.data)[0:254])
    prueba.save()
# OK     respuesta = [{
# OK        "message-out": "Test Instant Reply Back",
# OK        "delay": "0",
# OK    }]
# OK    
# OK    return Response(respuesta)

# {
#     "number":"987654",
#     "message-in":"Hola,&buenos&días",
#     "mensaje-in-raw":"Hola, buenos días",
#     "application":"2",
#     "type":"1",
#     "unique-id":"3fsdwet5747",
#     "quoted":"WEQWVDDVWEReqrwer",
# }
 

    if request.method == 'POST' and request.data:

        datos = request.data

        numero = datos['number']
        message_in = datos['message-in']
        message_in_raw = datos['mensaje-in-raw']
        application = datos['application']
        tipo = datos['type']
        unique_id = datos['unique-id']
        quoted = datos['quoted']
        opcion_seleccionada = message_in

#        respuesta = [{"number":numero,"application":application,"message":message_in,"type":tipo, "message-out":"Prueba","delay":"0"}]
#        return Response(respuesta)
        
        # Busca comunicacion
        comunicacion = MensajePicky.objects.filter(number=numero,estatus_mensaje=1).last()
        message = ""
        if comunicacion:
            registro = comunicacion.id
            if is_integer(opcion_seleccionada):
                opcionSeleccionada = int(opcion_seleccionada,0)
            else:
                opcionSeleccionada = 0  
            # opcion tipo de acción Compra , Renta
            opcion0 = comunicacion.opcion0
            accion_str = TIPO_ACCION[int(opcion0,0)][1]
            # opcion tipo de bien Casa, Departamento, Local comercial, Terreno 
            opcion1 = comunicacion.opcion1
            tipo_bien_str = TIPO_BIEN[int(opcion1,0)][1]
            # opción estado 
            opcion2 = comunicacion.opcion2
            opcion2_texto = comunicacion.opcion2_texto
            estado_str = ESTADOS[int(opcion2,0)][1]
            # opcion municipio
            opcion3 = comunicacion.opcion3
            opcion3_texto = comunicacion.opcion3_texto
            municipio_str = opcion3_texto
            if opcion0 == '0':    #    Tipo de accción
                #  Enviar el menú acción
                men = menu_tipo_accion(opcionSeleccionada,registro)
                if men['encontro'] == 1:
                    if opcion_seleccionada == "3":
                        message = "Hasta la vista"
                        conversacion_terminada = MensajePicky.objects.filter(id=registro).update(estatus_mensaje=0)
                    else:
                        #  Enviar el menú de tipo de bien
                        opcionSeleccionada = 0
                        accion_str = TIPO_ACCION[men['opcion0']][1]
                        m = menu_tipo_bien(accion_str, opcionSeleccionada, registro)
                        message = m['message'] 
                else:
                    message = men['message'] 
            elif opcion1 == '0':    #  Tipo de bien
                #  Enviar el menú tipo de bien
                men = menu_tipo_bien(accion_str, opcionSeleccionada, registro)
                if men['encontro'] == 1:
                    tipo_bien_str = TIPO_BIEN[men['opcion1']][1]
                    if opcion_seleccionada == "3":
                        message = "Hasta la vista"
                        conversacion_terminada = MensajePicky.objects.filter(id=registro).update(estatus_mensaje=0)
                    else:
                        #  Enviar Los estados
                        opcion1 = opcionSeleccionada
                        opcionSeleccionada = 0
                        men_edo = menu_estado(opcion0, opcion1, opcionSeleccionada, registro)
                        if men_edo['contador'] == 1:
                            menu_mun = menu_municipio(opcion0, opcion1, men_edo['opcion2'], men_edo['opcion2_texto'], opcionSeleccionada, registro)
                            if menu_mun['contador'] == 1:
                                message = "Seleccionó " + accion_str + "," + tipo_bien_str + "," + men_edo['opcion2_texto'] + "," + menu_mun['opcion3_texto']    
                            else:
                                message = men_edo['message'] + "\n" + menu_mun['message']
                        else:
                            message = men_edo['message'] 
                else:
                    message = men['message']
            elif opcion2 == '0':     # Estados
                #  Enviar los estados
                men_estado = menu_estado(opcion0, opcion1, opcionSeleccionada, registro)
                if men_estado['encontro'] == 1 or men_estado['contador'] == 1:
                    if opcion_seleccionada == "3":
                        message = "Hasta la vista"
                        conversacion_terminada = MensajePicky.objects.filter(id=registro).update(estatus_mensaje=0)
                    else:
                        #  Enviar los municipios
                        opcion2 = opcionSeleccionada
                        opcion2_texto = men_estado['opcion2_texto']
                        opcionSeleccionada = 0
                        menu_mun = menu_municipio(opcion0, opcion1, opcion2, opcion2_texto, opcionSeleccionada, registro)
                        message = men_estado['message'] + menu_mun['message']
                else:
                    message = men_estado['message']
            elif opcion3 == '0':     # Municipios
                #  Enviar los Municipios
                menu_mun = menu_municipio(opcion0, opcion1, opcion2, opcion2_texto, opcionSeleccionada, registro)
                if menu_mun['encontro'] == 1 or menu_mun['contador'] == 1:
                    if opcion_seleccionada == "3":
                        message = "Hasta la vista"
                        conversacion_terminada = MensajePicky.objects.filter(id=registro).update(estatus_mensaje=0)
                    else:
                        #  Enviar la seleccioón y el envio al asesor
                        opcion3 = opcionSeleccionada
                        opcion3_texto = menu_mun['opcion3_texto']
                        opcionSeleccionada = 0
                        message = "Seleccionó " + accion_str + "," + tipo_bien_str + "," + opcion2_texto + "," + menu_mun['opcion3_texto']
                else:
                    message = menu_mun['message']
            else:
                message = "Seleccionó " + accion_str + "," + tipo_bien_str + "," + opcion2_texto + "," + opcion3_texto
        else:
            #  Enviar el menú principal 0 inicia conversación
            message = "Bienvenido a servicio atención personalizada \n"
            menu = Menu.objects.filter(seleccion=0)
            for m in menu:
                message += m.opcion + " " + m.descripcion + "\n"
            comunicacion = MensajePicky(
                number = numero,
                message_in = message_in,
                message_in_raw = message_in_raw,
                message = message,
                application = application,
                tipo = tipo,
                unique_id = unique_id,
                quoted = quoted,
            )
            comunicacion.save()

        respuesta = [{"number":numero,"application":application,"message":message,"type":tipo, "message-out":"Prueba","delay":"0"}]
        
        return Response(respuesta)
    else:

        respuesta = [{}]

        return Response(respuesta)

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()
    
def menu_tipo_accion(opcionSeleccionada, registro):
    obj_accion = {}
    menu = Menu.objects.filter(seleccion=0)
    obj_accion['message_accion'] = "Selecciona lo que gustes realizar\n"
    obj_accion['encontro'] = 0
    obj_accion['opcion0'] = ""
    obj_accion['accion_str'] = ""
    for m in menu:
        if opcionSeleccionada == int(m.opcion):
            obj_accion['encontro'] = 1
        obj_accion['message_accion'] += m.opcion + " " + m.descripcion + "\n"
    if obj_accion['encontro'] == 1:
        seleecion_principal = MensajePicky.objects.filter(id=registro).update(opcion0=opcionSeleccionada)
        obj_accion['opcion0'] = opcionSeleccionada
        obj_accion['accion_str'] = TIPO_ACCION[opcionSeleccionada][1]
        obj_accion['message'] = ''
    else:
        obj_accion['message'] = obj_accion['message_accion']
    return obj_accion

def menu_tipo_bien(accion_str, opcionSeleccionada, registro):
    obj_tipo_bien = {}
    menu = Menu.objects.filter(seleccion=1)
    obj_tipo_bien['message_tipo_bien'] = "Selecciona el tipo de bien que deseas " + accion_str + "\n"
    obj_tipo_bien['encontro'] = 0
    for m in menu:
        if opcionSeleccionada == int(m.opcion):
            obj_tipo_bien['encontro'] = 1
        obj_tipo_bien['message_tipo_bien'] += m.opcion + " " + m.descripcion + "\n"
    if obj_tipo_bien['encontro'] == 1:
        seleecion_tipo_bien = MensajePicky.objects.filter(id=registro).update(opcion1=opcionSeleccionada)
        obj_tipo_bien['opcion1'] = opcionSeleccionada
        obj_tipo_bien['tipo_bien_str'] = TIPO_BIEN[opcionSeleccionada][1]
        obj_tipo_bien['message'] = ''
    else:
        obj_tipo_bien['message'] = obj_tipo_bien['message_tipo_bien']
    return obj_tipo_bien

def menu_estado(opcion0, opcion1, opcionSeleccionada, registro):
    obj_estado = {}
    if opcion0 == '1':
        bien = Bien.objects.filter(compra=1, tipo=opcion1).order_by('estado')
    else:
        bien = Bien.objects.filter(renta=1, tipo=opcion1).order_by('estado')
    obj_estado['estado_anterior'] = ""
    obj_estado['contador'] = 0
    obj_estado['encontro'] = 0
    obj_estado['message_edo'] = "Selecciona el estado de tu preferencias \n"
    for b in bien:
        if obj_estado['estado_anterior'] != b.estado:
            obj_estado['contador'] += 1
            obj_estado['estado_anterior'] = b.estado
            obj_estado['num_estado'] = next(t[1] for t in ESTADOS_NUM if t[0] == obj_estado['estado_anterior'])
            if opcionSeleccionada == obj_estado['num_estado']:
                obj_estado['encontro'] = 1
            obj_estado['message_edo'] += obj_estado['num_estado'] + " " + b.estado + "\n"
    if obj_estado['encontro'] == 1:
        obj_estado['opcion2'] = obj_estado['num_estado']
        obj_estado['opcion2_texto'] = obj_estado['estado_anterior']
        seleccion_estado = MensajePicky.objects.filter(id=registro).update(opcion2=opcionSeleccionada, 
                                                        opcion2_texto=obj_estado['estado_anterior'])
        obj_estado['message'] = ""
    elif obj_estado['contador'] == 1:
        obj_estado['opcion2'] = obj_estado['num_estado']
        obj_estado['opcion2_texto'] = obj_estado['estado_anterior']
        seleccion_estado = MensajePicky.objects.filter(id=registro).update(opcion2=obj_estado['num_estado'], 
                                                        opcion2_texto=obj_estado['estado_anterior'])
        obj_estado['message'] = "Tenemos solo en el estado de " + obj_estado['estado_anterior'] + "\n"
    else:
        obj_estado['message'] = obj_estado['estado_anterior']
    return obj_estado
            
def menu_municipio(opcion0, opcion1, opcion2, opcion2_texto, opcionSeleccionada, registro):
    obj_municipio = {}
    if opcion0 == '1':
        bien = Bien.objects.filter(compra=1, tipo=opcion1, estado=opcion2_texto).order_by('municipio')
    else:
        bien = Bien.objects.filter(renta=1, tipo=opcion1, estado=opcion2_texto).order_by('municipio')
    obj_municipio['encontro'] = 0
    obj_municipio['contador'] = 0
    obj_municipio['municipio_ant'] = ""
    obj_municipio['message_mpio'] = "Selecciona el municipio de tu preferencias \n"
    for b in bien:
        if opcionSeleccionada == b.id:
            obj_municipio['encontro'] = 1
            obj_municipio['opcion3'] = b.id
            obj_municipio['opcion3_texto'] = b.municipio
        if obj_municipio['municipio_ant'] != b.municipio:
            obj_municipio['contador'] += 1
            obj_municipio['municipio_ant'] = b.municipio
            obj_municipio['num_municipio'] = b.id
            obj_municipio['opcion3_texto'] = b.municipio
            obj_municipio['message_mpio'] += str(b.id) + " " + b.municipio + "\n"
    if obj_municipio['encontro'] == 1:
        if obj_municipio['contador'] == 1:
            obj_municipio['message'] = "Solo tenemos en el municipio de \n"+ obj_municipio['message_mpio']
        obj_municipio['message'] = ""
        seleccion_municipio = MensajePicky.objects.filter(id=registro).update(opcion3=opcionSeleccionada, 
                                                    opcion3_texto=obj_municipio['opcion3_texto'])
    elif obj_municipio['contador'] == 1:
        obj_municipio['message'] = "Solo tenemos en el municipio de \n"+ obj_municipio['message_mpio']
        seleccion_municipio = MensajePicky.objects.filter(id=registro).update(opcion3=obj_municipio['num_municipio'], 
                                                    opcion3_texto=obj_municipio['opcion3_texto'])
    else:    
        obj_municipio['message'] = obj_municipio['message_mpio']
    return obj_municipio

