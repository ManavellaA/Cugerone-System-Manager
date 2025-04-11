from flask import Blueprint, render_template
import app.functions
import os
import json

budget_list_bp = Blueprint('budget_list', __name__)

@budget_list_bp.route('/list/<ref>')
def budget_list(ref):
    if ref == 'Client':
        data = app.functions.get_data_from_json(app.functions.INDEX_BUDGET_PATH)
        order = [
            'Cliente',
            'Numero',
            'Fecha'
        ]
        title = "Lista de Presupuestos"
        
    elif ref == 'Supplier':
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
                        
                    except json.JSONDecodeError as e:
                        print(f"Error al leer el archivo {archivos}: {e}")

        order = [
            'Fecha',
            'Proveedor',
            'Numero',
            'Entrega'
        ]
        title = "Lista de OC"
        
    return render_template('tabla.html', data=data[::-1], order=order, title=title)