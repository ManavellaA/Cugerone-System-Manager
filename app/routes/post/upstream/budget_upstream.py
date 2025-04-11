from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
import app.functions

budget_upstream_bp = Blueprint('budget_upstream', __name__)

@budget_upstream_bp.route('/upstream', methods=["POST"])
def create_budget():
    data = request.json
    current_date = datetime.now().strftime('%d/%m/%Y')
    data['create_date'] = current_date
    
    if data['tipe'] == "Datos Cliente":
        
        while True:
            # Genera el número consecutivo
            consecutive_number = app.functions.get_next_number(data['tipe'])
            file = f'101-{consecutive_number:06d}'  # Formato 101-xxxxxx
            data['number'] = file
            filename = f'{file}.json'  # Formato 101-xxxxxx.json
            file_path = os.path.join(app.functions.DIRECTORY_BUDGET, filename)

            if os.path.exists(file_path):
                continue  # Si el archivo existe, genera un nuevo número
            else:
                break 

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        app.functions.update_index(data)
        
        return jsonify({"number": data['number']}), 200
    
    elif data['tipe'] == "Datos Proveedor":
        while True:
            # Genera el número consecutivo
            consecutive_number = app.functions.get_next_number(data['tipe'])
            file = f'501-{consecutive_number:06d}'  # Formato 501-xxxxxx
            data['number'] = file
            filename = f'{file}.json'  # Formato 501-xxxxxx.json
            file_path = os.path.join(app.functions.DIRECTORY_RECORD_SUPPLIER, filename)

            if os.path.exists(file_path):
                continue  # Si el archivo existe, genera un nuevo número
            else:
                break 

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        app.functions.update_index(data)
        
        return jsonify({"number": data['number']}), 200