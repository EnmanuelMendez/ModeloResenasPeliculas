from flask import Flask, request, jsonify, render_template
import joblib
from flask_cors import CORS
import os


# Cargar modelo y vectorizador
model = joblib.load("modelo_sentimientos.pkl")
vectorizer = joblib.load("vectorizador.pkl")

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "texto" not in data:
        return jsonify({"error": "Debes enviar un JSON con el campo 'texto'"}), 400

    texto = data["texto"]
    texto_vec = vectorizer.transform([texto])
    pred = model.predict(texto_vec)[0]
    sentimiento = "Positivo :)" if pred == 1 else "Negativo :("

    return jsonify({
        "texto": texto,
        "sentimiento": sentimiento
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)