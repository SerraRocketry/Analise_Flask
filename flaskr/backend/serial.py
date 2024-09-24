import serial

class serialCom:
    def __init__(self):
        self.ser = serial.Serial(port, 9600, timeout=1)
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()

    def send(self, data):
        self.ser.write(data.encode())

    def read(self):
        return self.ser.readline().decode()

    def close(self):
        self.ser.close()