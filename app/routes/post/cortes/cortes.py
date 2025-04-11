from flask import Blueprint, request, render_template, jsonify
from app.functions import backtracking_corte


corte_bp = Blueprint("corte", __name__)

@corte_bp.route("/cortes", methods=["GET", "POST"])
def cortes():
    title="Optimización de Corte de Barras"
    
    if request.method == "POST":
        largo_barra = request.form["largo_barra"]
        if largo_barra: 
            largo_barra = int(request.form["largo_barra"])
        else:
            largo_barra = 6000
            
        sangria = request.form["sangria"]
        if sangria: 
            sangria = int(request.form["sangria"])
        else:
            sangria = 3
        medidas = list(map(int, request.form.getlist("medida[]")))
        
        cantidades = list(map(int, request.form.getlist("cantidad[]")))

        # Generamos la lista completa de piezas según las cantidades
        piezas = [medida for medida, cantidad in zip(medidas, cantidades) for _ in range(cantidad)]

        # Ejecutamos el algoritmo de corte
        barras, desperdicio = backtracking_corte(piezas, largo_barra, sangria)

        cant_barras = len(barras)
        
        return render_template(
            "cortes.html",
            title=title,
            barras=barras,
            desperdicio=desperdicio,
            sangria=sangria,
            largo_barra=largo_barra,
            cant_barras=cant_barras,
            enumerate=enumerate,
            sum=sum,
            len=len
        )
    return render_template("cortes.html", title=title)
