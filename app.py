from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Conexión a MongoDB Atlas (Render usa variable de entorno)
uri = os.getenv("MONGO_URI")
cliente = MongoClient(uri)

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
