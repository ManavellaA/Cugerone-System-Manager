from flask import Blueprint, request, jsonify, send_from_directory, abort, current_app 
import os
import app.functions

download_bp = Blueprint('download', __name__)

@download_bp.route("/download", methods=["POST"])
def download_file():
    filename = request.json["filename"]
    directory = ''
    matching_files = []
    file_to_download = ''
    try:
        if "type" in request.json:
            try:
                if request.json["type"] == 'adm':
                    directory = os.path.abspath(app.functions.DIRECTORY_VOUCHERS)
                    files_in_directory = os.listdir(directory)
                    index = app.functions.get_data_from_json(app.functions.INDEX_SUPPLIER_PATH)
                    name = ''
                    for item in index:
                        if item['Numero'] == filename:
                            name = item['Comprobante_pago']
                    file_to_download = name
                else:
                    print('Entró')
                    if request.json["type"] == 'fc':
                        directory = os.path.abspath(app.functions.DIRECTORY_FC)
                        files_in_directory = os.listdir(directory)
                        index = app.functions.get_data_from_json(app.functions.INDEX_SUPPLIER_PATH)
                        name = ''
                        for item in index:
                            if item['Numero'] == filename:
                                name = item['FC']
                        file_to_download = name
            except KeyError as e:
                    print('algo paso con el Comprobante', e)
                    

        else:
            filename = request.json["filename"]
            directory = os.path.abspath(app.functions.DIRECTORY_FOLDER)
            files_in_directory = os.listdir(directory)
            matching_files = [f for f in files_in_directory if os.path.splitext(f)[0] == filename]

            if not matching_files:
                current_app.logger.error(f"Archivo no encontrado con el nombre: {filename}")
                abort(404, description="Archivo no encontrado.")

            file_to_download = matching_files[0]
            current_app.logger.info(f"Solicitud de descarga recibida para el archivo: {filename}")
            current_app.logger.info(f"Archivo encontrado: {file_to_download}")

    except Exception as e:
        current_app.logger.error(f"Error al procesar la solicitud: {e}")
        return jsonify({"error": str(e)}), 500
    
    print(directory)
    print(file_to_download)

    return send_from_directory(directory, file_to_download, as_attachment=True)
