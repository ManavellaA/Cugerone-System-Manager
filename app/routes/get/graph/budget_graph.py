from flask import Blueprint, render_template
import app.functions
from datetime import datetime
import requests
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Usar 'Agg' para evitar el uso de GUI

budget_graph_bp = Blueprint('budget_graph', __name__)

@budget_graph_bp.route('/graficos/<year>', methods=['GET', 'POST'])
def graph(year):
    if year > "0":
        url = 'http://192.168.0.190:5010/dolar_billete'
        dolar_b = float(requests.get(url).text.replace(',', '.'))

        json_data = app.functions.get_data_from_json(app.functions.INDEX_BUDGET_PATH)

        montos_por_mes = [0] * 12
        totales_por_mes = [0] * 12
        
        for item in json_data:
            fecha = datetime.strptime(item["Fecha"], "%d/%m/%Y")
            mes = fecha.month
            año = str(fecha.year)
            año_seleccionado = year
                        
            if item.get("Estado") == "Aceptado" and año == año_seleccionado:
                if item.get("Moneda") == "$":
                    if item.get("Moneda_cambio"):
                        monto = float(item.get("Monto", 0)) / float(item.get("Moneda_cambio", 1))
                    else:
                        monto = 0  
                    montos_por_mes[mes - 1] += monto
                    totales_por_mes[mes - 1] += monto  
                else:
                    monto = float(item.get("Monto", 0))
                    montos_por_mes[mes - 1] += monto
                    totales_por_mes[mes - 1] += monto  
            
            elif item.get("Estado") == "Parcial" and año == año_seleccionado:
                if item.get("Moneda") == "$":
                    if item.get("Moneda_cambio"):
                        monto_nuevo = float(item.get("Monto_nuevo", 0)) / float(item.get("Moneda_cambio", 1))
                        monto = float(item.get("Monto", 0)) / float(item.get("Moneda_cambio", 1))
                    else:
                        monto_nuevo = 0  
                        monto = 0
                    montos_por_mes[mes - 1] += monto_nuevo  
                    totales_por_mes[mes - 1] += monto
                else:
                    monto_nuevo = float(item.get("Monto_nuevo", 0))
                    monto = float(item.get("Monto", 0))
                    montos_por_mes[mes - 1] += monto_nuevo  
                    totales_por_mes[mes - 1] += monto
            
            else:
                if año == año_seleccionado:
                    if item.get("Moneda") == "$":
                        if item.get("Moneda_cambio"):
                            monto = float(item.get("Monto", 0)) / float(item.get("Moneda_cambio", 1))
                        else:
                            monto = float(item.get("Monto", 0)) / float(dolar_b) 
                        totales_por_mes[mes - 1] += monto  
                    else:
                        monto = float(item.get("Monto", 0))
                        totales_por_mes[mes - 1] += monto 

        labels = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Gráfico general (barras)
        def crear_grafico_barras(labels, val1, val2, title):
            def add(data):
                suma = sum(data)
                suma_formateado = "{:,.1f}".format(suma).replace(",", "X").replace(".", ",").replace("X", ".")
                return str(suma_formateado)

            acepted_sum = add(val1)
            entered_sum = add(val2)
            
            x = np.arange(len(labels))  
            ancho = 0.35  

            fig, ax = plt.subplots(figsize=(12, 6))

            ax.bar(x - ancho/2, val1, ancho, label='Aceptados' + " U$D " + acepted_sum, color='blue')
            ax.bar(x + ancho/2, val2, ancho, label='Cotizados' + " U$D " + entered_sum, color='orange')

            ax.set_xlabel('Meses')
            ax.set_ylabel('Presupuestado')
            ax.set_title(title)
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend()
            ax.set_xticklabels(labels, rotation=45, ha='right')

            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight')
            img.seek(0)
            return base64.b64encode(img.getvalue()).decode()
        
        
        def crear_grafico_torta(mes, aceptados, cotizados):
            # Calcular cuánto falta para alcanzar los cotizados
            faltante = max(0, cotizados - aceptados)  # Evitamos valores negativos
            valores = [aceptados, faltante]

            # Calcular los porcentajes respecto al total cotizado
            def autopct_personalizado(valores):
                porcentaje_aceptados = (aceptados / cotizados) * 100 if cotizados != 0 else 0
                porcentaje_faltante = (faltante / cotizados) * 100 if cotizados != 0 else 0
                return [f'{porcentaje_aceptados:.1f}%', f'{porcentaje_faltante:.1f}%']

            fig, ax = plt.subplots(figsize=(6, 6))  # Tamaño del gráfico

            # Crear el gráfico de torta
            pie_result = ax.pie(
                valores,
                labels=['Aceptados', 'Faltante'],
                colors=['blue', 'orange'],
                startangle=90 
            )

            # Extraemos los textos de los segmentos
            if len(pie_result) == 2:
                wedges, texts = pie_result
                autotexts = []  # Si no hay autotexts, lo dejamos vacío
            else:
                wedges, texts, autotexts = pie_result

            # Asignar los textos personalizados
            porcentajes = autopct_personalizado(valores)
            for text, porcentaje in zip(texts, porcentajes):
                text.set_text(porcentaje)

            ax.set_title(f'Gráfico de {mes}')

            # Guardar gráfico como PNG en memoria
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight')
            img.seek(0)
            plt.close(fig)  # Liberar memoria

            return base64.b64encode(img.getvalue()).decode()

        plot_url_general = crear_grafico_barras(labels, montos_por_mes, totales_por_mes, 'Anual')

        # Gráficos mensuales de torta y barras
        graficos_mensuales = []
        for i, label in enumerate(labels):
            if montos_por_mes[i] > 0 or totales_por_mes[i] > 0:
                # Gráfico de torta
                plot_url_torta = crear_grafico_torta(label, montos_por_mes[i], totales_por_mes[i])
                # Gráfico de barras
                plot_url_barras = crear_grafico_barras([label], [montos_por_mes[i]], [totales_por_mes[i]], f'{label} - Barras')
                
                graficos_mensuales.append((label, plot_url_torta, plot_url_barras))

        return render_template('graph.html',year=year , plot_url_general=plot_url_general, graficos_mensuales=graficos_mensuales)
    
    return render_template('graph.html')