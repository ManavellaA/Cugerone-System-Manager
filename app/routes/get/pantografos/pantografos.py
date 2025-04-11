from flask import Blueprint, render_template
import os
import app.functions

pantografos_bp = Blueprint('pantografos', __name__, template_folder='../templates')

@pantografos_bp.route('/pantografos')
def seguimiento():
    file = "PLANILLA DE SEGUIMIENTO"
    Sheet_name = "CRONOGRAMA"
    fileTipe = str(file + ".xlsx")
    print(os.path.join(app.functions.DIRECTORY_JSON, str(file + ".json")))
    app.functions.convert_file(os.path.join(app.functions.DIRECTORY_DRIVE, fileTipe), app.functions.DIRECTORY_JSON, Sheet_name)
    data = app.functions.get_data_from_json(os.path.join(app.functions.DIRECTORY_JSON, str(file + "-" + "CRONOGRAMA" + ".json")))
    order = ["OT", "CLIENTE", "ARCHIVO", "ESTADO", "PIEZAS CORTADAS", "ASIGNADO"]
    title = "Pantografos"
    
    return render_template('tabla.html', data=data, order=order, title=title)