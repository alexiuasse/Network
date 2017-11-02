from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
import cPickle as pickle
import socket
import time
import sys
 
 
class Gui(QWidget):
    def __init__(self, host, port):
        QWidget.__init__(self)
        
        self.nick = "Yo"
        
        self.recv = QTextEdit()
        self.send = QLineEdit()
        self.btn_send = QPushButton("Enviar")
        self.btn_connect = QPushButton("Conectar")
        
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.recv)
        vbox.addLayout(hbox)
        vbox.addWidget(self.btn_connect)
        
        hbox.addWidget(self.send)
        hbox.addWidget(self.btn_send)
        
        self.setLayout(vbox)
 
        self.btn_send.clicked.connect(self.enviar)
        self.btn_connect.clicked.connect(self.conectar)
    
    def conectar(self):
        self.con = Conectar()
        self.connect(self.con, SIGNAL("conexion"), self.conexion)
        self.con.show()
    
    def conexion(self, data, nick):
        self.nick = nick
        self.sck = socket.socket()
        self.sck.connect(data)
        
        self.e_thread = Escuchar(self.sck)
        self.connect(self.e_thread, SIGNAL("message"), self.mensaje)
        self.e_thread.start()
    
    def mensaje(self, data):
        mensaje = '<font color="red">%s: </font>%s' % data
        self.recv.append(mensaje)
    
    def enviar(self):
        data = str(self.send.text().toAscii())
        
        paquete = (self.nick, data)
        paquete = pickle.dumps(paquete)
        
        if data:
            self.sck.send(paquete)
            self.send.setText("")
            self.mensaje((self.nick, data))
    
 
class Conectar(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        self.host = QLineEdit('localhost')
        self.port = QLineEdit('9009')
        self.nick = QLineEdit()
        self.btn_connect = QPushButton("Conectar")
        
        hport = QHBoxLayout()
        hhost = QHBoxLayout()
        hnick = QHBoxLayout()
        vbox = QVBoxLayout()
        
        hhost.addWidget(QLabel("Host:"))
        hhost.addWidget(self.host)
        
        hport.addWidget(QLabel("Port:"))
        hport.addWidget(self.port)
        
        hnick.addWidget(QLabel("Nick:"))
        hnick.addWidget(self.nick)
        
        vbox.addLayout(hhost)
        vbox.addLayout(hport)
        vbox.addLayout(hnick)
        vbox.addWidget(self.btn_connect)
        
        self.setLayout(vbox)
        
        self.btn_connect.clicked.connect(self.comprobar)
    
    def comprobar(self):
        port = int(self.port.text().toAscii())
        host = str(self.host.text().toAscii())
        nick = str(self.nick.text().toAscii())
        
        if not nick:
            nick = host
        
        if port and host:
            self.emit(SIGNAL("conexion"), (host, port), nick)
 
class Escuchar(QThread):
    def __init__(self, sck):
        QThread.__init__(self)
        self.sock = sck
        
    def run(self):
        while True:
            buff = self.sock.recv(10024).strip()
            serialized = pickle.loads(buff)
            time.sleep(0.3)
            self.emit(SIGNAL("message"), serialized)
    
    def __del__(self):
        self.wait()
 
App = QApplication(sys.argv)
GUI = Gui("192.168.1.7", 9001)
GUI.show()
App.exec_()