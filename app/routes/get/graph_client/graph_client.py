from flask import Blueprint, render_template
import app.functions
import json
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64
from datetime import datetime
import os

matplotlib.use('Agg')  # Usar 'Agg' para renderizar sin GUI

graph_client_bp = Blueprint('graph_client', __name__)

@graph_client_bp.route('/grafico-clientes/<anio>')
def graph_client(anio):
    if anio != "0":
        index = json.load(open(app.functions.INDEX_BUDGET_PATH, 'r', encoding='utf-8'))
        list = {}

        for item in index:
            client = item.get('Cliente', 'Desconocido')
            date = item.get('Fecha', 0)
            date = datetime.strptime(date, '%d/%m/%Y')
            year = date.year
            if client not in list and int(anio) == year:  
                list[client] = {
                    'Cliente': client,
                    'Monto': 0
                }

        # Montos
        for item in index:
            client = item.get('Cliente', 'Desconocido')
            date = item.get('Fecha', 0)
            date = datetime.strptime(date, '%d/%m/%Y')
            year = date.year
            state = item.get('Estado', 'Desconocido')
            if state == "Parcial":
                state = "Aceptado"
                
            if client in list and int(anio) == year and state == "Aceptado":
                monto = item.get('Monto_nuevo', item.get('Monto', 0)) 
                moneda = item.get('Moneda', '')
                moneda_cambio = item.get('Moneda_cambio', 1)
                if moneda == "$":
                    list[client]['Monto'] += monto
                elif moneda == "U$D":
                    list[client]['Monto'] += monto * moneda_cambio

        # Calcula el total de todos los montos
        total_monto = sum(client['Monto'] for client in list.values())
        
        list_ordered = dict(sorted(list.items(), key=lambda item: item[1]['Monto'], reverse=True))
        
        # Prepara los datos para el gráfico
        labels = []
        sizes = []

        for client, data in list.items():
            if data['Monto'] > 0:  # Incluye solo clientes con montos mayores a 0
                labels.append(client)
                sizes.append(data['Monto'])

        # Combina los clientes con menor porcentaje en "Otros"
        threshold = 0.5  # Porcentaje mínimo para aparecer como etiqueta
        other_size = 0
        new_labels = []
        new_sizes = []

        for label, size in zip(labels, sizes):
            percentage = size / total_monto * 100
            if percentage < threshold:
                other_size += size
            else:
                new_labels.append(label)
                new_sizes.append(size)

        if other_size > 0:
            new_labels.append("Otros")
            new_sizes.append(other_size)

        # Crea el gráfico de torta
        plt.figure(figsize=(12, 8))  # Tamaño ajustado
        wedges, texts, autotexts = plt.pie(
            new_sizes,
            labels=new_labels,
            autopct=lambda p: f'{p:.1f}%' if p > 1 else '',
            startangle=140,
            pctdistance=0.85,  # Ajusta la distancia del texto al centro
            explode=[0.1 if label == "Otros" else 0 for label in new_labels],  # Resalta "Otros"
        )

        # plt.title('Distribución porcentual de montos por cliente', fontsize=16)
        plt.axis('equal')  # Asegura que el gráfico sea circular
        plt.tight_layout()

        # Mejorar la visibilidad de las etiquetas
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_fontsize(8)

        # Codifica Base64
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        graph_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        # Devuelve el gráfico al template
        return render_template("graph_clients.html", graph=graph_base64, year=anio, list=list_ordered)
    return render_template("graph_clients.html")
