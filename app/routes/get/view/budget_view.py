from flask import Blueprint, render_template
import os
import app.functions

budget_view_bp = Blueprint('budget_view', __name__)

@budget_view_bp.route('/view/<number>')
def view_budget(number):
    tipe = number[:1]
    if tipe == '1':
        file_path = os.path.join(app.functions.DIRECTORY_BUDGET, f'{number}.json')
        budget = app.functions.get_data_from_json(file_path)
    elif tipe == '5':
        file_path = os.path.join(app.functions.DIRECTORY_RECORD_SUPPLIER, f'{number}.json')
        budget = app.functions.get_data_from_json(file_path)
    
    return render_template('presupuesto.html', data=budget)
