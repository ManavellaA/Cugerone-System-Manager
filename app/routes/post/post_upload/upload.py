from flask import Blueprint, request, jsonify
import os
import json
import re
import pdfplumber
from datetime import datetime
import app.functions

post_upload_bp = Blueprint('post_upload', __name__)

@post_upload_bp.route("/upload/<ref>", methods=["POST"])
def upload_file(ref):

    is_valid, file_or_response, status_code = app.functions.validate_file(request)

    if not is_valid:
        print("Error de validación:", file_or_response.get_json())
        return file_or_response, status_code

    file = file_or_response

    if file.filename == "ORLANDI.pdf":
        filepath = os.path.join(app.functions.DIRECTORY_FOLDER, file.filename)
        if os.path.exists(filepath):
            os.remove(filepath)

        file.save(filepath)

        codigos_orlandi = {
            "14PL": "PERFILERIA-PLANCHUELA", 
            "14AN": "PERFILERIA-ANGULO", 
            "14HB": "HERRERIA-RENDONDO HERRERO", 
            "14HT": "PERFILERIA-HIERRO TE", 
            "14HU": "PERFILERIA-UPN", 
            "14DT": "PERFILERIA-IPN", 
            "00CR": "CAÑO-SCHEDULLE", 
            "00HC": "HERRERIA-REDONDO CONSTRUCCIÓN", 
            "00MH": "HERRERIA-MALLA ELECTROSOLDADA", 
            "14PC": "PERFILERIA-PERFIL C", 
            "03CE": "CAÑO-ESTRUCTURAL", 
            "14PW": "PERFILERIA-PERFIL W", 
            "00MD": "HERRERIA-METAL DESPLEGADO"
        }

        descuento = 66.0
        with pdfplumber.open(os.path.join(app.functions.DIRECTORY_FOLDER, file.filename)) as pdf:
            data = []
            regex = re.compile(r'^\d.*|\d$')
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')

                for line in lines:
                    parts = line.split()
                    if parts and regex.match(parts[0]):
                        codigo = parts[0][:4]  # Solo los primeros 4 caracteres

                        # Verificar si los primeros 4 caracteres coinciden con algún código de codigos_orlandi
                        if codigo in codigos_orlandi:
                            print(f"Código encontrado: {codigo}")

                            if len(parts) >= 5:
                                descripcion = " ".join(parts[1:-4])
                                try:
                                    precio_unidad = float(parts[-3].replace(".", "").replace(",", ".")) * (1 - descuento / 100)
                                    precio_unidad = round(precio_unidad, 2)
                                except ValueError:
                                    print(f"Error al convertir el valor a número en la línea: {line}")
                                    continue

                                moneda = parts[-1]
                                if moneda == 'BNA':
                                    moneda = 'U$D BILLETE'

                                fecha = datetime.now().strftime('%d/%m/%Y')
                                # Separar el valor de codigos_orlandi en TIPO y MATERIAL
                                material, tipo = codigos_orlandi[codigo].split('-')

                                data.append({
                                    "PROVEEDOR": "ORLANDI",
                                    "FECHA": fecha,  
                                    "MATERIAL": material,
                                    "TIPO": tipo, 
                                    "MONEDA": moneda,
                                    "VALOR UNITARIO": precio_unidad,
                                    "OBSERVACIONES": descripcion
                                })

        print("Datos extraídos Exitosamente")

        if data:
            output_file_path = 'ORLANDI.json'
            json_file = os.path.join(app.functions.DIRECTORY_SHOPPING, output_file_path)

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Datos guardados en {json_file}")
        else:
            print("No se encontraron coincidencias.")
        
        app.functions.regen_price_table()
            
    if ref == "adm":
        archivo = file
        numero = request.form.get("num")
        index = app.functions.get_data_from_json(app.functions.INDEX_SUPPLIER_PATH)
        if request.form.get("type") == 'fc':
            archivo_filepath = os.path.join(app.functions.DIRECTORY_FC, archivo.filename)
            for item in index:
                try:
                    if item["Numero"] == numero:
                        item["FC"] = str(archivo.filename)
                        file.save(archivo_filepath)
                        app.functions.save_json(app.functions.INDEX_SUPPLIER_PATH, index)

                except:
                    print(f"Advertencia: Error en la carga del Comprobante", numero)
        else:
            archivo_filepath = os.path.join(app.functions.DIRECTORY_VOUCHERS, archivo.filename)
            for item in index:
                try:
                    if item["Numero"] == numero:
                        item["Comprobante_pago"] = str(archivo.filename)
                        file.save(archivo_filepath)
                        app.functions.save_json(app.functions.INDEX_SUPPLIER_PATH, index)

                except:
                    print(f"Advertencia: Error en la carga del Comprobante", numero)

    return jsonify({"message": "File successfully uploaded and converted", "json_path": file.filename}), 200

