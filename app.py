from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

uri = os.getenv("MONGO_URI")

cliente = None
productos_collection = None

if uri:
    try:
        cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = cliente["floreria_lupe"]
        productos_collection = db["productos"]
        print("Mongo conectado")
    except Exception as e:
        print("Error Mongo:", e)
else:
    print("No hay MONGO_URI")


@app.route("/")
def home():
    try:
        productos = []

        if productos_collection:
            productos = list(productos_collection.find().limit(10))

        return render_template("index.html", productos=productos)

    except Exception as e:
        print("ERROR EN /:", e)
        return "Error cargando la página", 500


@app.route("/procesar-pedido", methods=["POST"])
def procesar_pedido():
    try:
        pedido = request.get_json()
        print("Pedido:", pedido)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
