from flask import Flask, request, jsonify
import joblib

# Cargar modelo y vectorizador
model = joblib.load("modelo_sentimientos.pkl")
vectorizer = joblib.load("vectorizador.pkl")

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    # El usuario debe enviar: {"texto": "The movie was great"}
    data = request.get_json()

    if not data or "texto" not in data:
        return jsonify({"error": "Debes enviar un texto en el campo 'texto'"}), 400

    texto = data["texto"]

    # Vectorizar texto
    vec = vectorizer.transform([texto])

    # Predicción
    pred = model.predict(vec)[0]

    # Convertir a etiqueta legible
    sentimiento = "positivo" if pred == 1 else "negativo"

    return jsonify({
        "texto": texto,
        "sentimiento": sentimiento
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)