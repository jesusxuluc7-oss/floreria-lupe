from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a MongoDB local
cliente = MongoClient("mongodb://localhost:27017/")

# Base de datos
db = cliente["floreria_lupe"]

# Colección
productos_collection = db["productos"]

@app.route("/")
def home():
    productos = list(productos_collection.find())

    return render_template(
        "index.html",
        productos=productos
    )

@app.route("/procesar-pedido", methods=["POST"])
def procesar_pedido():

    pedido = request.get_json()

    print("Pedido:", pedido)

    return jsonify({
        "mensaje": "Pedido recibido correctamente"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)