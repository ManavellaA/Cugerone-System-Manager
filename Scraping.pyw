import requests
from bs4 import BeautifulSoup
from flask import Flask
import threading
import time
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Variables globales para almacenar los valores del dólar
dolar_billete = 0
dolar_billete_date = 0
dolar_divisa = 0
dolar_divisa_date = 0

def fetch_dolar_prices(): # WebScrapping a BNA
    
    global dolar_billete, dolar_billete_date, dolar_divisa, dolar_divisa_date
    
    while True:
        try:
            url = "https://www.bna.com.ar/Personas"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                billetes = soup.find(id='billetes')
                divisas = soup.find(id='divisas')

                if billetes:
                    dolar_billete_venta = billetes.find_all('td')[2].text.strip().replace('.', ',')
                    dolar_bill_date = billetes.find_all('th')[0].text.strip()

                    # Solo actualiza si se obtienen valores válidos
                    dolar_billete = dolar_billete_venta
                    dolar_billete_date = dolar_bill_date
                else:
                    print("No se pudo acceder a cotización Billete")

                if divisas:
                    dolar_divisa_venta = divisas.find_all('td')[2].text.strip().replace('.', ',')
                    dolar_div_date = divisas.find_all('th')[0].text.strip()

                    # Solo actualiza si se obtienen valores válidos
                    dolar_divisa = dolar_divisa_venta
                    dolar_divisa_date = dolar_div_date
                else:
                    print("No se pudo acceder a cotización Divisa")

                date = datetime.now().strftime('%H:%M:%S-%d/%m/%Y')
                print(date ," /--/ ", dolar_billete, "-", dolar_billete_date, "/", dolar_divisa, "-",dolar_divisa_date)

            else:
                print("No se pudo acceder a la página del Banco Nación Argentina.")
        except Exception as e:
            print(f"Error al obtener los precios del dólar: {e}")
            
        time.sleep(120)

# --------------------------------------------------------------
# EndPoints datos

@app.route('/dolar_billete', methods=['GET'])
def dolar_billete_endpoint():
    return dolar_billete

@app.route('/dolar_divisa', methods=['GET'])
def dolar_divisa_endpoint():
    return dolar_divisa

@app.route('/dolar_billete_date', methods=['GET'])
def dolar_billete_date_endpoint():
    return dolar_billete_date

@app.route('/dolar_divisa_date', methods=['GET'])
def dolar_divisa_date_endpoint():
    return dolar_divisa_date

# --------------------------------------------------------------

if __name__ == '__main__':
    # Iniciar el hilo para actualizar los precios del dólar
    thread = threading.Thread(target=fetch_dolar_prices)
    thread.daemon = True
    thread.start()

    # Iniciar la aplicación Flask
    app.run(host="0.0.0.0", port="5010")
    
    # 192.168.0.190:5010/dolar_divisa
    # 192.168.0.190:5010/dolar_divisa_date
    # 192.168.0.190:5010/dolar_billete
    # 192.168.0.190:5010/dolar_billete_date