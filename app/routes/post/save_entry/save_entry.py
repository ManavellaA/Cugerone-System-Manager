from flask import Blueprint, request, jsonify
import app.functions

save_entry_bp = Blueprint('save_entry', __name__)

@save_entry_bp.route('/guardar/<ref>', methods=['POST'])
def save_supplier(ref):
    new_entry = request.get_json()
    
    if not new_entry.get('nombre') or not new_entry.get('ciudad'):
        return jsonify({"error": "Nombre y Ciudad son requeridos"}), 400

# ---------- reference ----------
    print(ref)
    if ref.lower() == '<supplier>':
        directory = app.functions.SUPPLIER_FILE
        
    elif ref.lower() == '<client>':
        directory = app.functions.CUSTOMERS_FILE
        
    else:
        return jsonify({"error": "No se reconoce la referencia"}), 400
    
# -------------------------------
        
    entry = app.functions.get_data_from_json(directory)
    
    for idx, name in enumerate(entry):
        if name['nombre'].lower() == new_entry['nombre'].lower():
            entry[idx] = new_entry
            app.functions.save_json(directory, entry)
            return jsonify({"message": "Actualizado con éxito"}), 200
    
    entry.append(new_entry)
    app.functions.save_json(directory, entry)
    return jsonify({"message": "Guardado con éxito"}), 201
