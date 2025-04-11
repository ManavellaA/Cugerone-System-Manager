from flask import Blueprint, request, jsonify
import app.functions
from datetime import datetime
import os
import json

save_state_bp = Blueprint('save_state', __name__)

@save_state_bp.route('/guardar-estado', methods=['POST'])
def save_state():
    data = request.json
    tipo = data.get("ref")
    ref = ""    
    
    if tipo == 'Cronograma de Pagos Proveedores':
        ref = app.functions.INDEX_SUPPLIER_PATH
        json_index = app.functions.get_data_from_json(ref)
        if json_index is None:
            return jsonify({"message": "El archivo de índice no existe"}), 409
        numero = data.get('Numero')
        estado_pago = data.get('Estado_pago')
        for item in json_index:
            if item.get('Numero') == numero:
                item['estado_pago'] = estado_pago
                app.functions.save_json(ref, json_index) 
                return jsonify({"message": "Estado actualizado con éxito"}), 200
            
    elif tipo == 'fecha':
        numero = data.get('Numero')
        newDate = data.get("Fecha")
        for archivos in os.listdir(app.functions.DIRECTORY_RECORD_SUPPLIER):
            if archivos.endswith(".json"):
                ruta_archivo = os.path.join(app.functions.DIRECTORY_RECORD_SUPPLIER, archivos)
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    try:
                        extract = json.load(archivo)
                        for item in extract:
                            if str(extract.get('number')) == numero:
                                extract['fecha_pago'] = newDate
                                app.functions.save_json(ruta_archivo, extract)
                                return jsonify({"message": "Fecha actualizada con éxito"}), 200
                    except Exception as e:
                        print("Error al procesar archivo:", ruta_archivo)
                        print(e)
        return jsonify({"message": "No se encontró el número indicado"}), 404

    else: 
        if tipo == 'Seguimiento de OC':
            ref = app.functions.INDEX_SUPPLIER_PATH
        
        elif tipo == 'Seguimiento de Presupuestos':
            ref = app.functions.INDEX_BUDGET_PATH
            
        json_index = app.functions.get_data_from_json(ref)
        
        if json_index is None:
            return jsonify({"message": "El archivo de índice no existe"}), 409
        numero = data.get('Numero') 
        estado = data.get('Estado')

        Dolar_b = data.get("DolarBillete")
        Dolar_d = data.get("DolarDivisa")
        
        if Dolar_b is not None:
            # Eliminar el símbolo de moneda y los espacios
            val_b_limpio = Dolar_b.replace('$', '').replace(' ', '').replace(',', '.')
            Dolar_b = float(val_b_limpio)
        else:
            print("Error: 'DolarBillete' no proporcionado o es None")
            return jsonify({"message": "DolarBillete no proporcionado"}), 400
        
        if Dolar_d is not None:
            # Eliminar el símbolo de moneda y los espacios
            val_d_limpio = Dolar_d.replace('$', '').replace(' ', '').replace(',', '.')
            Dolar_d = float(val_d_limpio)
        else:
            print("Error: 'DolarDivisa' no proporcionado o es None")
            return jsonify({"message": "DolarDivisa no proporcionado"}), 400
        moneda_valor = Dolar_b  # Valor por defecto en caso de que no se encuentre el tipo de moneda
        
        for item in json_index:
            if item.get('Numero') == numero:
                print(item)
                if item.get("Moneda_tipo") == "U$DB":
                    moneda_valor = Dolar_b
                elif item.get("Moneda_tipo") == "U$DD":
                    moneda_valor = Dolar_d
                item['Estado'] = estado
                item['Moneda_cambio'] = moneda_valor
                item['Fecha_estado'] = datetime.now().strftime('%d/%m/%Y')
                app.functions.save_json(ref, json_index)  # Guarda el JSON actualizado
                print(item)
                return jsonify({"message": "Estado actualizado con éxito"}), 200