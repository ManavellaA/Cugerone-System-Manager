from flask import Blueprint, render_template
import os
import app.functions

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/materiales')
def materiales():        
    data = app.functions.get_data_from_json(os.path.join(app.functions.DIRECTORY_JSON, "precios.json"))
    order = [
        "FECHA",
        "PROVEEDOR",
        "MATERIAL",
        "TIPO",
        "MEDIDA",
        "MONEDA",
        "VALOR UNITARIO",
        "OBSERVACIONES",
    ]
    title = "Precios"
    
    return render_template('tabla.html', data=data, order=order, title=title)

