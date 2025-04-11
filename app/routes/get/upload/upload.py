from flask import Blueprint, render_template

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/subir')
def subir():
    title = "Subir Archivo"
    return render_template("subir.html", title=title)
