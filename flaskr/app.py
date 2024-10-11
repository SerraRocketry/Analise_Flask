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
        global filename
        filename = '_' + (uploaded_file.filename).split('.')[0]
        global motor
        motor = motor_analisys(uploaded_file)
        data = motor.get_data()
        result = motor.get_result()
        temp = result.to_dict('records')
        collumns = result.columns.values
        return render_template("graficos.html", x=data['Tempo'].to_list(), y=data['Empuxo'].to_list(), colnames=collumns, records=temp)


@app.route('/save_motor', methods=['POST'])
def save_motor():
    name = request.form['name']
    if name == '':
        return render_template('analises.html', msg='Nome do motor não informado!', displayopt='block')
    name+=filename
    motor.save_analisys(name)
    return render_template('analises.html', msg='Análise salva com sucesso!', displayopt='block')
#####################################################################

######################### Rotas de galerias #########################


# @app.route('/voosalvos')
# def analiseVoo():
#     return render_template('voo.html')


@app.route('/motoressalvos')
def show_motor():
    path = r'CenterFlask/flaskr/archives/motor/'
    all_files = glob.glob(os.path.join(path, "*_dados.csv"))
    file = [f.split('motor/')[-1] for f in all_files]
    return render_template('motores.html', motores=file)
#####################################################################

if __name__ == '__main__':
    def open_browser(port):
        webbrowser.open_new(f"http://localhost:{port}/")

    port = 5000
    open_browser(port)
    app.run(port=port, debug=False, host='0.0.0.0')
