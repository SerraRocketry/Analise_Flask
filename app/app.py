from backend import motor_analisys, data_treatment

import webbrowser
from flask import Flask, render_template, request, jsonify

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
    return render_template('tratamento.html', displayopt='none')
#####################################################################


######################### Rotas de erros #########################


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html")
#####################################################################

######################### Rotas de teste estático #########################


@app.route('/motor_upload', methods=['POST'])
def upload_motor():
    uploaded_file = request.files['file']
    return process_motor_file(uploaded_file)


@app.route('/save_motor', methods=['POST'])
def save_motor():
    name = request.form['name']
    if name == '':
        return render_template('analises.html', msg='Nome do motor não informado!', displayopt='block')
    motor.save_analisys(name)
    return render_template('analises.html', msg='Análise salva com sucesso!', displayopt='block')
#####################################################################

######################### Rotas de Tratamento de Dados #########################


@app.route('/data_upload', methods=['POST'])
def upload_data():
    return process_data_file(request.files['file'])


@app.route('/save_treatment', methods=['POST'])
def save_treatment():
    name = file.replace('_raw.txt', '')
    data.save_treatment(name)
    return render_template('tratamento.html', msg='Tratamento salvo com sucesso!', displayopt='block')
#####################################################################

######################### Funções de visualização #########################


def process_motor_file(uploaded_file):
    global motor
    motor = motor_analisys(uploaded_file)
    data = motor.get_data()
    result = motor.get_result()
    return render_template("graficos_motor.html", x=data['Tempo'].to_list(), y=data['Empuxo'].to_list(), result=result)


def process_data_file(uploaded_file):
    global data
    data = data_treatment(uploaded_file)
    data_raw = data.get_data()
    time_slider_min = data_raw['Tempo'].min()
    time_slider_max = data_raw['Tempo'].max()
    force_slider_min = data_raw['Empuxo'].min()
    force_slider_max = data_raw['Empuxo'].max()
    table_info = data_raw['Empuxo'].describe().to_dict()
    threshold = round(data_raw['Empuxo'].mean(),3)
    data_filtered = data.data_filter(threshold, [time_slider_min, time_slider_max])
    global file
    file = uploaded_file.filename
    return render_template("graficos_tratamento.html", x=data_filtered['Tempo'].to_list(), y=data_filtered['Empuxo'].to_list(), result=table_info, fmin=force_slider_min, fmax=force_slider_max, threshold=threshold, tmin=time_slider_min, tmax=time_slider_max)


def open_browser(port):
    webbrowser.open_new(f"http://localhost:{port}/")


@app.route('/update_filters', methods=['POST'])
def update_filters():
    global data
    threshold = float(request.form['threshold'])
    tmin = float(request.form['tmin'])
    tmax = float(request.form['tmax'])
    data_filtered = data.data_filter(threshold, [tmin, tmax])
    table_info = data_filtered['Empuxo'].describe().to_dict()
    return jsonify({
        'x': data_filtered['Tempo'].to_list(),
        'y': data_filtered['Empuxo'].to_list(),
        'result': table_info
    })


if __name__ == '__main__':
    port = 5000
    open_browser(port)
    app.run(host='0.0.0.0', port=port)
