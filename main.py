from flask import Flask, render_template, request, jsonify
from marshmallow import ValidationError

from schemas import PeticionRecorridoSchema
from services import optimizar_ruta, OSRMError

app = Flask(__name__)

@app.route('/')
def home():
    """Documentación web del endpoint."""
    return render_template('index.html')

@app.route('/api/optimizacion', methods=['POST'])
def calcular_recorrido_eficiente():
    """Calcula el recorrido eficiente entre un conjunto de coordenadas."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "El cuerpo de la petición debe ser un JSON válido."}), 400

    schema = PeticionRecorridoSchema()
    try:
        datos = schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errores_validacion": err.messages}), 422

    try:
        coordenadas_ordenadas = optimizar_ruta(datos['coordenadas'])
        return jsonify(coordenadas_ordenadas), 200
    except OSRMError as err:
        return jsonify({"error": err.message}), err.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)
