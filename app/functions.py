from flask import jsonify
import os
import pandas as pd
import json

DIRECTORY_VOUCHERS = "comprobantes"

DIRECTORY_FC = "fc"

DIRECTORY_BUDGET = "presupuestos"

DIRECTORY_SUPPLIER = "oc"

DIRECTORY_RECORD_SUPPLIER = os.path.join(DIRECTORY_SUPPLIER, "record")

DIRECTORY_JSON = "json"

DIRECTORY_ADM = "adm"

DIRECTORY_FOLDER = os.path.join("app", "upload")

CUSTOMERS_FILE = os.path.join(DIRECTORY_BUDGET, 'clientes.json')

DIRECTORY_DRIVE  = r"G:\\.shortcut-targets-by-id\\10nBquKEMMvtT78wDzBWzhzGW6oiiWS6c\\SEGUIMIENTOS"

COUNTER_BUDGET_FILE = os.path.join(DIRECTORY_BUDGET, 'counter.txt')

COUNTER_SUPPLIER_FILE = os.path.join(DIRECTORY_SUPPLIER, 'counter_supplier.txt')

INDEX_SUPPLIER_PATH = os.path.join(DIRECTORY_SUPPLIER, 'oc_index.json')

INDEX_BUDGET_PATH = os.path.join(DIRECTORY_BUDGET, 'index.json')

SUPPLIER_FILE = os.path.join(DIRECTORY_SUPPLIER, 'proveedores.json')

DIRECTORY_SUPPLIER_RECORD = os.path.join(DIRECTORY_SUPPLIER, 'record')

DIRECTORY_SHOPPING = os.path.join(DIRECTORY_JSON, 'shopping')


def validate_file(request):
    if "file" not in request.files:
        return False, jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return False, jsonify({"error": "No selected file"}), 400

    return True, file, None

def convert_file(filepath, dirPath, sheet):
    df = pd.read_excel(filepath, sheet_name=sheet)
    df = df.fillna("")

    try:
        for col in df.select_dtypes(include=["datetime64"]).columns:
            df[col] = df[col].apply(lambda x: x.strftime("%d-%m-%Y") if pd.notna(x) else "")
    except:
        pass

    json_data = df.to_dict(orient="records")
    json_filename = f"{os.path.splitext(os.path.basename(filepath))[0]}-{sheet}.json"
    json_filepath = os.path.join(dirPath, json_filename)

    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False)

    return json_filepath

def get_data_from_json(filepath):
    if not os.path.exists(filepath):
        print(f"Error: El archivo {filepath} no existe.")
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            # print(data)
            return data
    except Exception as e:
        print(f"Error al leer el archivo {filepath}: {e}")
        return []

def save_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def get_next_number(type):

    if type == "Datos Cliente":
        if not os.path.exists(COUNTER_BUDGET_FILE):
            with open(COUNTER_BUDGET_FILE, 'w') as file:
                file.write('100')
            return 100
        with open(COUNTER_BUDGET_FILE, 'r+') as file:
            last_number = int(file.read())
            next_number = last_number + 1
            file.seek(0)
            file.write(str(next_number))
            file.truncate()

    elif type == "Datos Proveedor":
        if not os.path.exists(COUNTER_SUPPLIER_FILE):
            with open(COUNTER_SUPPLIER_FILE, 'w') as file:
                file.write('200')
            return 200
        with open(COUNTER_SUPPLIER_FILE, 'r+') as file:
            last_number = int(file.read())
            next_number = last_number + 1
            file.seek(0)
            file.write(str(next_number))
            file.truncate()
            
    return next_number

def parse_number(value: str) -> float:

    """""
    Convierte una cadena con formato numérico (con separadores de miles y decimales)
    a un float, manejando tanto comas como puntos como separadores.
    
    Ejemplos:
    - "1.352,5" → 1352.5
    - "1.352.5" → 1352.5
    - "12,345.67" → 12345.67
    """""
    value = value.strip()
    if not value:
        raise ValueError("Valor vacío")
    
    last_dot = value.rfind('.')
    last_comma = value.rfind(',')
    last_sep = max(last_dot, last_comma)
    
    if last_sep == -1:
        cleaned = value.replace(',', '').replace('.', '')
        return int(cleaned)
    else:
        integer_part = value[:last_sep].replace(',', '').replace('.', '')
        decimal_part = value[last_sep + 1:]
        print("decimal_part" + decimal_part)
        
        return float(f"{integer_part}.{decimal_part}")

def update_index(data):
    index = []
    total = 0.0
    
    if data['tipe'] == "Datos Cliente":
        if os.path.exists(INDEX_BUDGET_PATH):
            try:
                with open(INDEX_BUDGET_PATH, 'r') as index_file:
                    content = index_file.read().strip()
                    if content:
                        index = json.loads(content)
            except json.JSONDecodeError:
                print("El archivo de índice está corrupto.")

        for articulo in data["articulos"]:
            try:
                # Convertir cantidad y unitario usando la función personalizada
                cantidad = parse_number(articulo["cantidad"])
                unitario = parse_number(articulo["unitario"])
                
                total += cantidad * unitario
            except ValueError as e:
                print(f"Artículo omitido: {articulo}. Error: {e}")
                continue  # Saltar artículo inválido

        index.append({
            'Numero': data['number'],
            'Cliente': data.get('cliente', {}).get('nombre', 'Desconocido'), 
            'Fecha': data['create_date'],
            'Monto': total,
            'Moneda': data.get('moneda'),
            'Moneda_tipo': data.get('moneda_tipo'),
            "Estado": ""
        })

        with open(INDEX_BUDGET_PATH, 'w') as index_file:
            json.dump(index, index_file, indent=4)

    if data['tipe'] == "Datos Proveedor":

        # Cargar índice existente (si hay)
        if os.path.exists(INDEX_SUPPLIER_PATH):
            try:
                with open(INDEX_SUPPLIER_PATH, 'r') as index_file:
                    content = index_file.read().strip()
                    index = json.loads(content) if content else []
            except (json.JSONDecodeError, FileNotFoundError):
                print("Índice corrupto.")

        total = 0.0

        for articulo in data["articulos"]:
            try:
                # Convertir cantidad y unitario usando la función personalizada
                cantidad = parse_number(articulo["cantidad"])
                unitario = parse_number(articulo["unitario"])
                
                total += cantidad * unitario
            except ValueError as e:
                print(f"Artículo omitido: {articulo}. Error: {e}")
                continue  # Saltar artículo inválido

        # Añadir registro al índice
        index.append({
            'Numero': data['number'],
            'Proveedor': data.get('proveedor', {}).get('nombre', 'Desconocido'), 
            'Fecha': data['create_date'],
            'Monto': total,
            'Moneda': data.get('moneda'),
            'Moneda_tipo': data.get('moneda_tipo'),
            "Estado": ""
        })

        # Guardar índice
        try:
            with open(INDEX_SUPPLIER_PATH, 'w') as index_file:
                json.dump(index, index_file, indent=4)
        except Exception as e:
            print(f"Error guardando el índice: {e}")
            
    # if data['tipe'] == "Datos Proveedor":

    #     if os.path.exists(INDEX_SUPPLIER_PATH):
    #         try:
    #             with open(INDEX_SUPPLIER_PATH, 'r') as index_file:
    #                 content = index_file.read().strip()
    #                 if content:
    #                     index = json.loads(content)
    #         except json.JSONDecodeError:
    #             print("El archivo de índice está corrupto.")

    #     for articulo in data["articulos"]:
    #         cantidad = float(articulo["cantidad"].replace(',', '.'))
    #         unitario = float(articulo["unitario"].replace(',', '.'))
    #         total += cantidad * unitario

    #     index.append({
    #         'Numero': data['number'],
    #         'Proveedor': data.get('proveedor', {}).get('nombre', 'Desconocido'), 
    #         'Fecha': data['create_date'],
    #         'Monto': total,
    #         'Moneda': data.get('moneda'),
    #         'Moneda_tipo': data.get('moneda_tipo'),
    #         "Estado": ""
    #     })

    #     with open(INDEX_SUPPLIER_PATH, 'w') as index_file:
    #         json.dump(index, index_file, indent=4)

def regen_price_table():
    datos_combinados = []

    for archivo in os.listdir(DIRECTORY_SHOPPING):
        if archivo.endswith(".json"): 
            ruta_archivo = os.path.join(DIRECTORY_SHOPPING, archivo)
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)

                    if isinstance(data, list):
                        datos_combinados.extend(data)
                    else:
                        datos_combinados.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error al leer {archivo}: {e}")

    with open(os.path.join(DIRECTORY_JSON, "precios.json"), 'w', encoding='utf-8') as f_salida:
        json.dump(datos_combinados, f_salida, ensure_ascii=False, indent=4)

def backtracking_corte(piezas, largo_barra, sangria):
    piezas.sort(reverse=True)
    barras = []

    for pieza in piezas:
        colocado = False
        for barra in barras:
            espacio_disponible = largo_barra - sum(barra) - sangria * (len(barra))
            if espacio_disponible >= pieza:
                barra.append(pieza)
                colocado = True
                break  

        if not colocado:
            barras.append([pieza])  

    desperdicio_total = sum(largo_barra - (sum(barra) + sangria * (len(barra) - 1)) for barra in barras)

    return barras, desperdicio_total
