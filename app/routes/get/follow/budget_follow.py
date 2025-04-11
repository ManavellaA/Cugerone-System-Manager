from flask import Blueprint, render_template
import app.functions
import os
import json

budget_follow_bp = Blueprint('budget_follow', __name__)

@budget_follow_bp.route('/seguimiento/<key>')
def budget_follow(key):
    print(key)
    if key == 'Client':
        data = app.functions.get_data_from_json(app.functions.INDEX_BUDGET_PATH)
        order = [
            'Cliente',
            'Numero',
            'Fecha',
            'Estado'
        ]
        title = "Seguimiento de Presupuestos"
        
    elif key == 'Supplier':
        data = app.functions.get_data_from_json(app.functions.INDEX_SUPPLIER_PATH)
        
        for archivos in os.listdir(app.functions.DIRECTORY_RECORD_SUPPLIER):
            if archivos.endswith(".json"):
                ruta_archivo = os.path.join(app.functions.DIRECTORY_RECORD_SUPPLIER, archivos)
                try:
                    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                        extract = json.load(archivo)
                        for item in data:
                            if item['Numero'] == extract['number']:
                                item['Entrega'] = extract['fecha'].replace("-", "/")
                except (PermissionError, json.JSONDecodeError) as e:
                    print(f"Error al procesar {archivos}: {e}")
        order = [
            'Proveedor',
            'Numero',
            'Entrega',
            'Estado'
        ]
        title = "Seguimiento de OC"
    
    return render_template('tabla.html', data=data[::-1], order=order, title=title)