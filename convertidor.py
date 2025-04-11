import os
import json
import app.functions

def procesar_archivos_json(carpeta):
    resultados = []

    for nombre_archivo in os.listdir(carpeta):
        if nombre_archivo.endswith('.json'):
            ruta_archivo = os.path.join(carpeta, nombre_archivo)

            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                try:
                    data = json.load(archivo)  # Cargar el JSON correctamente
                    monto = 0

                    # Verificar si hay artículos y procesarlos
                    for item in data.get("articulos", []):  # Ahora recorremos la lista de artículos
                        cant_str = item.get("cantidad", "0")
                        unit_str = item.get("unitario", "0")

                        # Verificar si los valores contienen caracteres no numéricos válidos
                        if not cant_str.replace(".", "").replace(",", "").isdigit() or not unit_str.replace(".", "").replace(",", "").isdigit():
                            print(f"Error en formato numérico en {nombre_archivo}, artículo: {item}")
                            continue  # Saltar este artículo y seguir con el siguiente

                        try:
                            cant = float(cant_str.replace(".", "").replace(",", "."))  # Formato correcto
                            unit = float(unit_str.replace(".", "").replace(",", "."))  
                            monto += cant * unit  
                        except ValueError:
                            print(f"Error en conversión numérica en {nombre_archivo}, artículo: {item}")
                            continue  # Saltar este artículo en caso de error

                    resultado = {
                        "Numero": data.get("number", ""),
                        "Proveedor": data.get("proveedor", {}).get("nombre", ""),
                        "Fecha": data.get("create_date", ""),
                        "Monto": monto,
                        "Moneda": data.get("moneda", ""),
                        "Moneda_tipo": data.get("moneda_tipo", ""),
                        "Estado": ""
                    }

                    resultados.append(resultado)

                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error al procesar el archivo {nombre_archivo}: {e}")

    return resultados

carpeta_json = app.functions.DIRECTORY_RECORD_SUPPLIER

resultados = procesar_archivos_json(carpeta_json)

for resultado in resultados:
    print(json.dumps(resultado, ensure_ascii=False, indent=4))
