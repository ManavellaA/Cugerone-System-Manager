from flask import Blueprint, render_template
import os
import app.functions

budget_edit_bp = Blueprint('budget_edit', __name__)

@budget_edit_bp.route('/edit/<number>')
def budget_edit(number):
    def directory(number):
        if number[:2] == '10':
            return os.path.join(app.functions.DIRECTORY_BUDGET, f'{number}.json')
        elif number[:2] == '50':
            return os.path.join(app.functions.DIRECTORY_SUPPLIER_RECORD, f'{number}.json')
        else:
            return None  # Retornar None si no coincide con las condiciones
    
    editable = True
    data = app.functions.get_data_from_json(directory(number))
    
    return render_template('presupuesto.html', data=data, editable=editable)
