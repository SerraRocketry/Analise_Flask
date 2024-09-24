from unittest import result
from backend import motor_analisys

import webbrowser
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)

######################### Rotas principais #########################


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def indexhome():
    return render_template('index.html')


@app.route('/analises')
def analise():
    return render_template('analises.html')


@app.route('/galeria')
def galeria():
    return render_template('galeria.html')
#####################################################################

######################### Rotas de análises #########################


@app.route('/analise_voo')
def analiseVoo():
    return render_template('voo.html')


@app.route('/analise_teste_estatico')
def analiseTeste():
    return render_template('teste_estatico.html')
#####################################################################

######################### Rotas de teste estático #########################


@app.route('/motor_upload', methods=['POST'])
def upload_motor():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        df = motor_analisys(uploaded_file)
        return render_template("graficos.html")
#####################################################################

######################### Rotas de galerias #########################


# @app.route('/voosalvos')
# def analiseVoo():
#     return render_template('voo.html')


# @app.route('/motoressalvos')
# def analiseTeste():
#     return render_template('teste_estatico.html')
#####################################################################

if __name__ == '__main__':
    def open_browser(port):
        webbrowser.open_new(f"http://localhost:{port}/")

    port = 5000
    open_browser(port)
    app.run(port=port, debug=False, host='0.0.0.0')
