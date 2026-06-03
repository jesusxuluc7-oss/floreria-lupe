from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# 🔌 MongoDB (seguro para Render)
uri = os.getenv("MONGO_URI")

if not uri:
    raise Exception("MONGO_URI no está configurada en Render")

cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)

db = cliente["floreria_lupe"]
productos_collection = db["productos"]

# 🏠 HOME (LIMITADO para evitar crash de memoria)
@app.route("/")
def home():
    productos = list(productos_collection.find().limit(12))  # 🔥 FIX RAM
    return render_template("index.html", productos=productos)

# 📦 PEDIDOS
@app.route("/procesar-pedido", methods=["POST"])
def procesar_pedido():
    pedido = request.get_json()

    print("Pedido:", pedido)

    return jsonify({
        "mensaje": "Pedido recibido correctamente"
    })

# 🚀 RUN (solo local, Render usa gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
