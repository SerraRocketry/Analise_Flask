from backend import motor_analisys

import webbrowser
from flask import Flask, render_template, request

import glob
import os

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
    return render_template('analises.html', displayopt='none')


@app.route('/tratamento')
def galeria():
    return render_template('tratamento.html')

######################### Rotas de erros #########################


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html")
#####################################################################

######################### Rotas de análises #########################


@app.route('/analise_teste_estatico')
def analiseTeste():
    return render_template('teste_estatico.html')
#####################################################################

######################### Rotas de teste estático #########################


@app.route('/motor_upload', methods=['POST'])
def upload_motor():
    uploaded_file = request.files['file']
    return process_motor_file(uploaded_file, False)


@app.route('/save_motor', methods=['POST'])
def save_motor():
    name = request.form['name']
    if name == '':
        return render_template('analises.html', msg='Nome do motor não informado!', displayopt='block')
    # name += filename
    motor.save_analisys(name)
    return render_template('analises.html', msg='Análise salva com sucesso!', displayopt='block')
#####################################################################

######################### Rota de Tratamento de Dados #########################

@app.route('/tratamento', methods=['POST'])
def tratamento():
    return render_template('tratamento.html')


def process_motor_file(uploaded_file, saved):
    global motor
    motor = motor_analisys(uploaded_file, saved)
    data = motor.get_data()
    result = motor.get_result()
    temp = result.to_dict('records')
    columns = result.columns.values
    return render_template("graficos.html", x=data['Tempo'].to_list(), y=data['Empuxo'].to_list(), colnames=columns, records=temp)


def open_browser(port):
    webbrowser.open_new(f"http://localhost:{port}/")


if __name__ == '__main__':
    port = 5000
    open_browser(port)
    app.run(host='0.0.0.0', port=port)