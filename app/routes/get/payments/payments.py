from flask import Blueprint, render_template
import app.functions
import os
import json

payments_bp = Blueprint('payments_bp', __name__)

@payments_bp.route('/adm/payments')
def payments():
    data = app.functions.get_data_from_json(app.functions.INDEX_SUPPLIER_PATH)
    
    for archivos in os.listdir(app.functions.DIRECTORY_RECORD_SUPPLIER):
        if archivos.endswith(".json"):
            ruta_archivo = os.path.join(app.functions.DIRECTORY_RECORD_SUPPLIER, archivos)
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                try:
                    extract = json.load(archivo)
                    for item in data:
                        if item['Numero'] == extract['number']:
                            item['Entrega'] = extract['fecha'].replace("-", "/")
                            try:
                                item['Fecha_de_pago'] = extract['fecha_pago'].replace("-", "/")
                            except KeyError as e:
                                if e == 0:
                                    print(f"Advertencia: Clave {e} no encontrada en {archivos}. Se omite.")
                            try:
                                item['Forma_de_pago'] = extract['forma_pago']
                            except KeyError as e:
                                if e == 0:
                                    print(f"Advertencia: Clave {e} no encontrada en {archivos}. Se omite.")
                            try:
                                item['Estado_pago'] = item['estado_pago']
                            except KeyError as e:
                                if e == 0:
                                    print(f"Advertencia: Clave {e} no encontrada en {archivos}. Se omite.")
                            try:
                                if item['Estado'] != 'Entregado':
                                    item['Entrega'] = 'En curso'
                                else:    
                                    item['Entrega'] = item['Estado']
                            except KeyError as e:
                                if e == 0:
                                    print(f"Advertencia: Clave {e} no encontrada en {archivos}. Se omite.")
                            try:
                                if any("Comprobante_pago" in dic for dic in item):
                                    print("Comprobante Copiado")
                                else:    
                                    item['Comprobante_pago'] = ""
                            except KeyError as e:
                                print(f"Fallo comprobante.")
                            try:
                                if any("FC" in dic for dic in item):
                                    print("FC Copiado")
                                else:    
                                    item['FC'] = ""
                            except KeyError as e:
                                print(f"Fallo comprobante.")
                                
                except json.JSONDecodeError as e:
                    print(f"Error al leer el archivo {archivos}: {e}")

    # print(data)

    order = [
        'Forma_de_pago',
        'Fecha_de_pago',
        'FC',
        'Estado_pago',
        'Proveedor',
        'Numero',
        'Entrega',
        'Comprobante'
    ]
    
    title = "Cronograma de Pagos Proveedores"
        
    return render_template('tabla.html', data=data[::-1], order=order, title=title)