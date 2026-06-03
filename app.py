from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# 🔌 CONEXIÓN SEGURA A MONGO
uri = os.getenv("MONGO_URI")

cliente = None
db = None
productos_collection = None

if uri:
    try:
        cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = cliente["floreria_lupe"]
        productos_collection = db["productos"]
        print("✅ MongoDB conectado")
    except Exception as e:
        print("❌ Error MongoDB:", e)
else:
    print("⚠️ MONGO_URI no configurada en Render")


# 🏠 HOME (ANTI-CRASH TOTAL)
@app.route("/")
def home():
    try:
        productos = []

        if productos_collection is not None:
            productos = list(productos_collection.find().limit(10))

        return render_template("index.html", productos=productos)

    except Exception as e:
        print("❌ Error en /:", e)
        return "Error cargando la página", 500


# 📦 PEDIDOS (SEGURO)
@app.route("/procesar-pedido", methods=["POST"])
def procesar_pedido():
    try:
        pedido = request.get_json()
        print("📦 Pedido recibido:", pedido)

        return jsonify({"ok": True, "mensaje": "Pedido recibido"})
    
    except Exception as e:
        print("❌ Error pedido:", e)
        return jsonify({"ok": False, "error": str(e)}), 500


# 🚀 RUN LOCAL (Render usa Gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
