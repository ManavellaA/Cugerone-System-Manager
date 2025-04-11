from flask import Blueprint, render_template
import app.functions

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/presupuesto')
def budget():
    empresas = app.functions.get_data_from_json(app.functions.CUSTOMERS_FILE)
    tipo = "Cliente"
    return render_template('form.html', empresas=empresas, tipo=tipo)