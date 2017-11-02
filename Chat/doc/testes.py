
from threading import Thread as Process
 
import socket
import cPickle as pickle
 
class servidor():
    def __init__(self):
        self.port = 9001
        self.host = socket.gethostname()
        self.conectados = []
        self.escuchar()
    
    def escuchar(self):
        try:
            ser = socket.socket()
            ser.bind((self.host, self.port))
            ser.listen(5)
            while True:
                (sck, addr) = ser.accept()
                if not sck in self.conectados:
                    self.conectados.append(sck)
                    Process(target=self.indpt, args=(sck,addr)).start()
        except KeyboardInterrupt:
            print c.FAIL % ("Saliendo")
            ser.close()
            return
    
    def indpt(self, sck, addr):
        try:
            direccion = "%s:%i" % addr
            print c.OKGREEN % ("conectado a: " + direccion)
            sck.send(pickle.dumps(("Servidor", "Conectado al servidor")))
            while True:
                buff = sck.recv(10024).strip()
                if not len(buff):
                    print c.FAIL % (direccion + " desconectado")
                    self.conectados.remove(sck)
                    sck.close()
                    return
                else:
                    for i in self.conectados:
                        if i != sck:
                            print i.send(buff + "\r\n")
        except:
            print c.FAIL % (direccion + " desconectado")
            sck.close()
            return
 
class c:
    OKGREEN = '\033[92m[*] %s\033[0m'
    FAIL = '\033[91m[-] %s\033[0m'
 
servidor()