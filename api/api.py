# Dependencies
import sys
from flask import Flask, request, jsonify
import pickle
import traceback
import pandas as pd

# API definition
app = Flask(__name__)

## Funciones
@app.route('/predict', methods=['POST'])
def predict():
    if model:
        json_ = 'None'
        json_ = request.json
        print(json_)

        # Leemos los datos
        data = pd.DataFrame(json_)

        # Procesamos los datos
        query = pre.preprocess(data)

        # Predicción
        prediction = list(model.predict(query))
        # Probabilidad de predicción
        pred_prob = list(model.predict_proba(query))

        # Devolvemos las predicciones realizadas.
        results = list()
        for i in range(len(prediction)):
            results.append({'prediction': str(prediction[i]), 'probability': str(pred_prob[i][0])})
        return jsonify({
            'status': 'SUCCESS',
            'results': results
            })
    else:
        print('ERROR:: ' + traceback.format_exc())
        # Devolvemos el error al usuario
        return jsonify({
            'status': 'ERROR',
            'description': 'Internal Server Error'
        })

## Inicio
if __name__ == '__main__':
    try:
        port = int(sys.argv[1])  # Utilizamos el puerto indicado
    except:
        port = 5000  # Puerto por defecto 5000

    try:
        host = str(sys.argv[2]) # Utilizamos la ip indicada
    except:
        host = '127.0.0.1' # localhost

    model = pickle.load(open("model/fake_class_model.sav", 'rb'))  # Cargar model
    print('Model loaded')

    api_url = 'http://' + host + ':' + str(port)

    # En docker usar host:0.0.0.0
    if host == '127.0.0.1':
        app.run(port=port, debug=True)
    else:
        app.run(host=host, port=port, debug=True)