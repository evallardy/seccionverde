from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.http import JsonResponse
import json

@api_view(['POST','GET','PULL','PUT','PATCH','DELETE'])
def mensaje_api_view(request):
    # Guardado de la información que llega tanto el meodo como la información
    prueba = Prueba(descripcion = json.dumps(request.data)[0:254])
    prueba.save()

    if request.method == 'POST' and request.data:
        datos = request.data
        if datos['number'] and datos['message-in'] and datos['message_in_raw'] \
            and datos['application'] and datos['type']:
            numero = datos['number']
            message_in = datos['message-in']
            message_in_raw = datos['message_in_raw']
            application = datos['application']
            tipo = datos['type']
            opcion_seleccionada = message_in_raw
            # Busca comunicacion
            comunicacion = MensajePicky.objects.filter(number=numero,estatus_mensaje=1).last()
            message = ""
            respuesta = ""
            if comunicacion:
                # quitar espacion en la cadena del mensaje
                opcion_sel = opcion_seleccionada.upper().replace(" ", "")
                nivel = comunicacion.nivel
                pk = comunicacion.id
                if buscaOpcion(comunicacion, opcion_sel):
                    if opcion_sel == 'R':
                        # Envia menu anteriror
                        sig_comunicacion = MensajePicky.objects.filter(id=pk).update(nivel=nivel-1)
                        menu_json = traeJson(comunicacion, nivel-1)
                        message = creaMenu(json.dumps(menu_json))
                    elif opcion_sel == 'X':
                        sig_comunicacion = MensajePicky.objects.filter(id=pk).update(estatus_mensaje=0)
                        message = "Gracias por su preferencia, lo esperamos muy pronto \n\n"
                    else:
                        menu_json = traeJson(comunicacion, nivel)
                        menu_json['seleccion'] = opcion_sel
                        menu_json1 = generaJson(comunicacion, nivel + 1)
                        if nivel == 1:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion1=menu_json, opcion2=menu_json1, nivel=nivel+1)
                        elif nivel == 2:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion2=menu_json, opcion3=menu_json1, nivel=nivel+1)
                        elif nivel == 3:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion3=menu_json, opcion4=menu_json1, nivel=nivel+1)
                        elif nivel == 4:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion4=menu_json, opcion5=menu_json1, nivel=nivel+1)
                        elif nivel == 5:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(nivel=nivel+1)
                        message = creaMenu(json.dumps(menu_json1))
                else:
                    # Envia nuevamente el mismo menu
                    menu_json = traeJson(comunicacion, nivel)
                    message = creaMenu(json.dumps(menu_json))
            else:
                #  Crea el menu primer nivel
                menu_json = generaJson(None, 1)
                message = creaMenu(json.dumps(menu_json))
                
                # Guarda la peticion la primera vez con su primer menu
                comunicacion = MensajePicky(
                    number = numero,
                    message_in = message_in,
                    message_in_raw = message_in_raw,
                    application = application,
                    tipo = tipo,
                    nivel=1,
                    opcion1 = menu_json,
                )
                comunicacion.save()
            # Se envia repuesta 
            respuesta = {"number":numero,"application":application,"message":message,"type":tipo, "message-out":message,"delay":"0"}
            return Response(respuesta)
        else:
            # Se envia el mensaje de error, no envian nada
            if datos['number']:
                respuesta = mensajeError(datos['number'])
            else:
                respuesta = mensajeError("Faltan datos")
            return Response(respuesta)
    else:
        # Se envia el mensaje de error, no envian nada
        respuesta = mensajeError("Sin número")
        return Response(respuesta)
                
def generaJson(comunicacion, nivel):
    opciones = {}
    if nivel == 1:
        titulo = 'Bienvenido a servicio atención personalizada\n\n' + '¿Que le gustaría hacer?\n\n'
        bienes = Bien.objects.filter(compra_renta=3)
        if bienes:
            opciones[1] = TIPO_ACCION[1][1]
            opciones[2] = TIPO_ACCION[2][1]
        else:
            bienes = Bien.objects.filter(compra_renta=1)
            if bienes:
                opciones[1] = TIPO_ACCION[1][1]
            bienes = Bien.objects.filter(compra_renta=2)
            if bienes:
                opciones[2] = TIPO_ACCION[2][1]
        opciones['X'] = 'Terminar'
    elif nivel == 2:
        accion = opcionSeleccionadaT(comunicacion, 1)
        accionN = opcionSeleccionada(comunicacion, 1)
        titulo = '¿Que deseas ' + accion + '?\n\n'
        tipos = Bien.objects.filter(compra_renta__in=[accionN,3]).values_list('tipo', flat=True).distinct()
        for tipo in tipos:
            opciones[tipo] = TIPO_BIEN[tipo][1]
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 3:
        accion = opcionSeleccionadaT(comunicacion, 1)
        accionN = opcionSeleccionada(comunicacion, 1)
        tipo = opcionSeleccionadaT(comunicacion, 2)
        tipoN = opcionSeleccionada(comunicacion, 2)
        titulo = '¿En que estado quieres ' + accion + ' ' + tipo + '?\n\n'
        estados = Bien.objects.filter(compra_renta__in=[accionN,3],tipo=tipoN).values_list('estado', flat=True).distinct().order_by('estado')
        for estado in estados:
            opciones[estado] = ESTADOS[estado][1]
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 4:
        accion = opcionSeleccionadaT(comunicacion, 1)
        accionN = opcionSeleccionada(comunicacion, 1)
        tipo = opcionSeleccionadaT(comunicacion, 2)
        tipoN = opcionSeleccionada(comunicacion, 2)
        estado = opcionSeleccionadaT(comunicacion, 3)
        estadoN = opcionSeleccionada(comunicacion, 3)
        titulo = '¿En que municipio del estado ' + estado + " quieres " + accion + ' ' + tipo + '?\n\n'
        municipios = Bien.objects.filter(compra_renta__in=[accionN,3],tipo=tipoN, estado=estadoN).values_list('municipio', flat=True).distinct().order_by('municipio')
        contador = 0
        for municipio in municipios:
            contador += 1
            opciones[contador] = municipio
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 5:
        accion = opcionSeleccionadaT(comunicacion, 1)
        accionN = opcionSeleccionada(comunicacion, 1)
        tipo = opcionSeleccionadaT(comunicacion, 2)
        tipoN = opcionSeleccionada(comunicacion, 2)
        estado = opcionSeleccionadaT(comunicacion, 3)
        estadoN = opcionSeleccionada(comunicacion, 3)
        municipio = opcionSeleccionadaT(comunicacion, 4)
        titulo = '¿Que ' + tipo + ' deseas ' + accion + '?, en el municipio ' + municipio + ' del estado ' + estado + '\n\n'
        bienes = Bien.objects.filter(compra_renta__in=[accionN,3],tipo=tipoN, estado=estadoN, municipio=municipio).order_by('colonia')
        for bien in bienes:
            opciones[bien.id] = bien.colonia
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    else:
        accion = opcionSeleccionadaT(comunicacion, 1)
        accionN = opcionSeleccionada(comunicacion, 1)
        tipo = opcionSeleccionadaT(comunicacion, 2)
        tipoN = opcionSeleccionada(comunicacion, 2)
        estado = opcionSeleccionadaT(comunicacion, 3)
        estadoN = opcionSeleccionada(comunicacion, 3)
        municipio = opcionSeleccionadaT(comunicacion, 4)
        bienN = opcionSeleccionada(comunicacion, 5)
        bien = Bien.objects.filter(id=bienN).first()
        titulo = 'Los datos de ' + tipo + ' que seleccionaste para ' + accion + ', en el municipio ' + municipio + ' del estado ' + estado + '\n\n'
        titulo += 'Esta en la colonia ' + bien.colonia
        opciones = {}
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    data = {'titulo': titulo, 'seleccion':0, 'opciones': opciones}
    return data

def buscaOpcion(comunicacion, opcion_sel):
    nivel = comunicacion.nivel
    menu_json = traeJson(comunicacion, nivel)
    return existeOpcion(menu_json, opcion_sel)

def traeJson(comunicacion, opcion):
    if opcion == 1:
        menu_json = comunicacion.opcion1
    elif opcion == 2:
        menu_json = comunicacion.opcion2
    elif opcion == 3:
        menu_json = comunicacion.opcion3
    elif opcion == 4:
        menu_json = comunicacion.opcion4
    else:
        menu_json = comunicacion.opcion5
    return menu_json

def existeOpcion(menu_json, opcion_sel):
    encontro = False
    for opcion in menu_json['opciones']:
        if opcion == opcion_sel:
            encontro = True
            break
    return encontro
                
def opcionSeleccionada(comunicacion, opcion):
    if opcion == 1:
        menu_json = comunicacion.opcion1
    elif opcion == 2:
        menu_json = comunicacion.opcion2
    elif opcion == 3:
        menu_json = comunicacion.opcion3
    elif opcion == 4:
        menu_json = comunicacion.opcion4
    else:
        menu_json = comunicacion.opcion5
    opcion_sel = menu_json
    seleccion = opcion_sel['seleccion']
    return seleccion

def opcionSeleccionadaT(comunicacion, opcion):
    if opcion == 1:
        menu_json = comunicacion.opcion1
    elif opcion == 2:
        menu_json = comunicacion.opcion2
    elif opcion == 3:
        menu_json = comunicacion.opcion3
    elif opcion == 4:
        menu_json = comunicacion.opcion4
    else:
        menu_json = comunicacion.opcion5
    opcion_sel = menu_json
    seleccion = opcion_sel['seleccion']
    return opcion_sel['opciones'][seleccion]

def creaMenu(objeto):
    json_data = json.loads(objeto)
    mensaje = json_data['titulo']
    if json_data['opciones']:
        opciones = json_data['opciones']
        for opcion in opciones:
            mensaje += opcion + " - " + opciones[opcion] + "\n"
    return mensaje

def mensajeError(numeroTelefono):
    mensaje = 'Faltan datos'
    respuesta = {'Error':mensaje}
    prueba = Prueba(descripcion = "Celular:" + numeroTelefono + "/" + mensaje)
    prueba.save()
    return respuesta

