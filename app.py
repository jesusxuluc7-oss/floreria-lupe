from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# 🔌 MongoDB Atlas
uri = os.getenv("MONGO_URI")

if not uri:
    raise Exception("MONGO_URI no está configurada en Render")

cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)

db = cliente["floreria_lupe"]
productos_collection = db["productos"]

# 🏠 HOME
@app.route("/")
def home():
    try:
        productos = list(productos_collection.find().limit(10))
        return render_template("index.html", productos=productos)
    except Exception as e:
        print("Error en / :", e)
        return "Error cargando productos", 500


# 📦 PEDIDO
@app.route("/procesar-pedido", methods=["POST"])
def procesar_pedido():
    try:
        pedido = request.get_json()

        print("Pedido recibido:", pedido)

        return jsonify({
            "mensaje": "Pedido recibido correctamente"
        })

    except Exception as e:
        print("Error en pedido:", e)
        return jsonify({"error": "Error procesando pedido"}), 500


# 🚀 RUN LOCAL (Render usa Gunicorn, esto no afecta producción)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
