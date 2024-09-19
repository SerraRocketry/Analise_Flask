from flask import Flask, render_template, request
import serial
import serial.tools.list_ports
from datetime import datetime
from flask_socketio import SocketIO
from threading import Lock
import pandas as pd
import webbrowser

thread = None
thread_lock = Lock()

app = Flask(__name__)
socketio = SocketIO(app)

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


@app.route('/conexoes')
def conexoes():
    return render_template('conexoes.html')
#####################################################################

######################### Rotas de análises #########################


@app.route('/analise_voo')
def analiseVoo():
    return render_template('voo.html')


@app.route('/analise_teste_estatico')
def analiseTeste():
    return render_template('teste_estatico.html')


@app.route('/motor_upload', methods=['POST'])
def upload_motor():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        df = pd.read_excel(uploaded_file)
        f = [round(i, 2) for i in df['Forca'].to_list()]
        t = [round(i, 2) for i in df['Tempo_de_queima'].to_list()]
        print(f)
        return render_template("graficos.html", forca=f, tempo=t)
#####################################################################

######################### Rotas de conexão #########################


@app.route('/connect', methods=['POST'])
def select():
    select = request.form.get('conexoes')
    if select == 'wifi':
        return render_template('wifi.html')
    elif select == 'bluetooth':
        return render_template('bluetooth.html')
    elif select == 'serial':
        serialp = get_serial_ports()
        return render_template('serial.html', serialp=serialp)
    else:
        return render_template('conexoes.html')


@app.route('/sconnect', methods=['POST'])
def select_serial():
    global sport
    sport = request.form.get('serialports')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_serial)
    return render_template('message.html')


@socketio.on('message')
def handle_message(msg):
    ser.write(msg['msg'].encode())
    print(f"Enviado: {msg['msg']}")
    response = ser.readline().decode('utf-8').strip()
    socketio.emit('my response', {'data': response,
                  'time': get_current_datetime()})


@socketio.on('close')
def close_connection(close):
    ser.close()
    print('Connection closed')


@app.route('/bconnect', methods=['POST'])
def select_bluetooth():
    return render_template('message.html')


@app.route('/wconnect')
def select_wifi():
    return render_template('message.html')
#####################################################################


def get_serial_ports():
    ports = [port for port in list(
        serial.tools.list_ports.comports())]
    return [{'serialp': str(port)+' - '+str(desc)} for port, desc, hwid in ports if '/dev/ttyUSB' in port or '/dev/serial' in port]


def get_current_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def background_serial():
    try:
        global ser
        ser = serial.Serial(sport, 9600)
    except serial.SerialException as e:
        print(f"Erro ao abrir a porta serial: {e}")

    while True:
        ser.write(b'a')
        response = ser.readline().decode('utf-8').strip()
        socketio.emit('my response', {
            'data': response, 'time': get_current_datetime()})
        socketio.sleep(1)


def open_browser(port):
    webbrowser.open_new(f"http://localhost:{port}/")


if __name__ == '__main__':
    port = 5000
    open_browser(port)
    socketio.run(app, host='0.0.0.0', port=port)
