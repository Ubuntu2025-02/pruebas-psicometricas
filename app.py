from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)

# MongoDB connections
client = MongoClient('mongodb+srv://testpruebasdiscleo:L30_D!sc2025#@cluster0.zg4g3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db_elo = client['bd1']
db_disc = client['bd2']
collection_elo = db_elo['resultados_elo'] 
collection_disc = db_disc["registros"]

# Main routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def resultados():
    return render_template('home.html')

# ELO test routes
@app.route('/prueba-elo')
def prueba_elo():
    return render_template('elo.html')

@app.route('/resultados-elo')
def resultados_elo():
    try:
        registros = list(collection_elo.find({}, {'_id': 0}))
        return render_template('bd_elo.html', resultados=registros)
    except Exception as e:
        return f"Error al recuperar los resultados: {str(e)}", 500

@app.route('/guardar-resultados', methods=['POST'])
def guardar_resultados_elo():
    try:
        # Obtener los datos del formulario
        data = request.get_json()
        nombre = data['nombre']
        edad = int(data['edad'])
        resultados = data['resultados']
        fecha = datetime.now()

        # Crear un documento para insertar en MongoDB
        registro = {
            'nombre': nombre,
            'edad': edad,
            'resultados': resultados,
            'fecha': fecha
        }

        # Insertar el documento en la colección
        collection_elo.insert_one(registro)

        # Retornar una respuesta de éxito
        return jsonify({'message': 'Resultados guardados exitosamente'}), 200

    except Exception as e:
        # Retornar una respuesta de error
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DISC test routes
@app.route('/prueba-disc')
def prueba_disc():
    return render_template('disc.html')

@app.route('/resultados-disc')
def resultados_disc():
    try:
        resultados = list(collection_disc.find({}, {'_id': 0}))
        return render_template('bd_disc.html', resultados=resultados)
    except Exception as e:
        return f"Error al recuperar los resultados: {str(e)}", 500

@app.route('/guardar_resultados', methods=['POST'])
def guardar_resultados_disc():
    try:
        data = request.get_json()
        nombre = data['nombre']
        edad = data['edad']
        resultados = data['resultados']
        pattern = data['pattern']

        documento = {
            'nombre': nombre,
            'edad': edad,
            'fecha': datetime.now(),
            'resultados': resultados,
            'pattern': pattern
        }

        collection_disc.insert_one(documento)
        return jsonify({"message": "Resultados guardados correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Thank you page route
@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

# Additional API endpoints
@app.route('/obtener-registros', methods=['GET'])
def obtener_registros():
    try:
        registros = list(collection_elo.find({}, {'_id': 0}))
        return jsonify(registros), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)