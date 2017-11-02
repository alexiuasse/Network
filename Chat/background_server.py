# -*- coding: utf-8 -*-

import socket, sys, time
from mensagens import *

class Background_servidor():
    def Background(self,HOST,PORT,RECV_BUFFER, NOME_ARQ):
        
        self.HOST = HOST
        self.PORT = int(PORT)
        self.RECV_BUFFER = RECV_BUFFER
        self.NOME_ARQ = NOME_ARQ
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # para debugar, deixa a porta livre
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        while True:
            try:
                self.server_socket.bind((self.HOST, self.PORT))
                break
            except socket.error, e:
                self.PORT = self.PORT + 1
                
        self.server_socket.listen(1)
        
        print msg_controle('OK')+cor('[ Background servidor Online ]','branco')
        print msg_controle('...')+cor('[ Porta : ','branco')+cor(str(self.PORT),'ciano')+cor(' Host : ','branco')+cor(str(self.HOST),'ciano')+cor(' BUFFER : ','branco')+cor(str(self.RECV_BUFFER),'ciano')+cor(' ]','branco')
        
    def Pega_porta(self):
        return self.PORT
    
    def Mandar_arquivo(self, NOME_ARQ):
        while True:
            con, cliente = self.server_socket.accept()
            try:
                with open ('Documentos/'+NOME_ARQ,"r") as arquivo:
                    while True:
                        text = arquivo.read(4096)
                        if not text: break
                        con.send(text)
                print msg_controle('OK')+cor('[ Arquivo : ','branco')+cor(NOME_ARQ,'ciano')+cor(' transferido com sucesso ]','branco')
                con.close()
                break
            except Exception, e:
                print e
                print msg_controle('ERRO')+cor('[ Ocorreu algum erro na transferência ]','branco')
        time.sleep(30)
        print msg_controle('!')+cor('[ Background servidor Offline ]\n','branco')
        print msg_controle('...')+cor('[ Porta : ','branco')+cor(str(self.PORT),'ciano')+cor(' Host : ','branco')+cor(str(self.HOST),'ciano')+cor(' BUFFER : ','branco')+cor(str(self.RECV_BUFFER),'ciano')+cor(' ]','branco')
        self.server_socket.close()