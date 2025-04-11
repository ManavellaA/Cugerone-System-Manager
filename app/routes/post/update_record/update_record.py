from flask import Blueprint, request, jsonify
import requests
import datetime
import os
import app.functions

update_record_bp = Blueprint('update_record', __name__)

@update_record_bp.route('/update/<number>', methods=["POST"])
def view_budget(number):
    data = request.json
    index = ""
    directory = ""
    Monto_nuevo = 0
    state = ""
    
    url = 'http://192.168.0.190:5010/dolar_billete'
    dolar_b = float(requests.get(url).text.replace(',', '.'))
    
    if number[:2] == '10':
        directory = os.path.join(app.functions.DIRECTORY_BUDGET, f'{number}.json')
        index = os.path.join(app.functions.INDEX_BUDGET_PATH)
        state = "Parcial"
    elif number[:2] == '50':
        directory = os.path.join(app.functions.DIRECTORY_SUPPLIER_RECORD, f'{number}.json')
        index = os.path.join(app.functions.INDEX_SUPPLIER_PATH)
        state = "Editado"
    else:
        print(f"Error: No se encontró un directorio válido para el número {number}")
        return "Error: Directorio no encontrado", 404

    jsonData = app.functions.get_data_from_json(directory)

    # print(data['items'])
    
    for item_primero in jsonData["articulos"]:
        for item_segundo in data['items']:
            if item_primero["articulo"] == item_segundo["articulo"]:
                item_primero["cantidad"] = app.functions.parse_number(item_segundo["cantidad"])
                item_primero["unitario"] = app.functions.parse_number(item_segundo["unitario"])
                item_primero["observaciones"] = item_segundo["observaciones"]
    
    for art in jsonData['articulos']:
        # print(art['unitario'])
        Monto_nuevo += float(art['cantidad']) * float(art['unitario'])
    
    jsonData["update"] = datetime.datetime.now().strftime("%d/%m/%Y")
    
    app.functions.save_json(directory, jsonData)
    
    indexData = app.functions.get_data_from_json(index)
    
    for item in indexData:
        if item["Numero"] == number:
            item["Cambios"] = state
            item["Monto_nuevo"] = Monto_nuevo
            item["Moneda_cambio"] = dolar_b
    
    app.functions.save_json(index, indexData)
    
    return jsonify(message="Datos actualizados con éxito"), 200
