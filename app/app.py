

from backend import motor_analisys, data_treatment
import os

import webbrowser
from flask import Flask, render_template, request, jsonify, Blueprint

project_name = "serra-rocketry"

page = Blueprint(
    name="page",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
    )

# app = Flask(__name__)

######################### Rotas principais (Begin) #########################

@page.route('/')
def index():
    return render_template('index.html')

@page.route('/home')
def indexhome():
    return render_template('index.html')

@page.route('/analises')
def analise():
    return render_template('analises.html', displayopt='none')

@page.route('/tratamento')
def galeria():
    return render_template('tratamento.html', displayopt='none')

######################### Rotas principais (End) #########################


######################### Rotas de erros (Begin) #########################


@page.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@page.errorhandler(500)
def internal_error(e):
    return render_template("500.html")
######################### Rotas de erros (End) #########################

###########################################################################

######################### Rotas de teste estático (Begin) #########################

@page.route('/motor_upload', methods=['POST'])
def upload_motor():
    uploaded_file = request.files['file']
    return process_motor_file(uploaded_file)

@page.route('/save_motor', methods=['POST'])
def save_motor():
    name = request.form['name']
    if name == '':
        return render_template('analises.html', msg='Nome do motor não informado!', displayopt='block')
    motor.save_analisys(name)
    return render_template('analises.html', msg='Análise salva com sucesso!', displayopt='block')

######################### Rotas de teste estático (End) #########################

###########################################################################

######################### Rotas de Tratamento de Dados (Begin) #########################

@page.route('/data_upload', methods=['POST'])
def upload_data():
    return process_data_file(request.files['file'])


@page.route('/save_treatment', methods=['POST'])
def save_treatment():
    name = file.replace('_raw.txt', '')
    data.save_treatment(name)
    return render_template('tratamento.html', msg='Tratamento salvo com sucesso!', displayopt='block')

######################### Rotas de Tratamento de Dados (End) #########################

###########################################################################

######################### Funções de visualização (Begin) #########################


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
    webbrowser.open_new(f"http://localhost:{port}/{project_name}")

@page.route('/update_filters', methods=['POST'])
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

######################### Funções de visualização (End) #########################

app = Flask(__name__)
app.register_blueprint(page, url_prefix=f"/{project_name}",)

if __name__ == '__main__':
    
    host = '0.0.0.0' # aberto para todos os IPs
    port = 5000
    extra_files = []

    print("")
    print("* Watched:")
    for path in [ "./templates", "./static/css", "./static/js" ]:
        for file in os.listdir(f"{path}"):
            print( f"\t{path}/{file}" )
            extra_files.append( f"{path}/{file}" )
    print("")

    # extra_files.append([ f"./static/css/{j}" for j in os.listdir("./static/css") ])

    # page.config["TEMPLATES_AUTO_RELOAD"] = True # possivelmente não funcionando ...
    # page.config["DEBUG"] = True # possivelmente redundante ...
    # app.config["TESTING"] = True #

    running = True
    browser_running = False

    app.run(
            host=host,
            port=port,
            debug=True,
            extra_files=extra_files,
        )

    # comando: flask run --debug --extra-files templates/base.html
