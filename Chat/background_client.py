# -*- coding: utf-8 -*-

import socket, sys
from mensagens import *

class Background_cliente():
    def __init__(self,HOST,PORT,RECV_BUFFER,NOME_ARQ, NICK):
        
        self.HOST = HOST
        self.PORT = int(PORT)
        self.RECV_BUFFER = RECV_BUFFER
        self.NOME_ARQ = NOME_ARQ
        self.NICK = NICK
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client_socket.connect((self.HOST,self.PORT))
            #print '\r\n'+msg_controle('OK')+cor('[ Conexão estabelecida, pegando arquivo : ','branco')+cor(NOME_ARQ,'ciano')+cor(' ]','branco')
            #print msg_controle('...')+cor('[ Porta : ','branco')+cor(str(self.PORT),'ciano')+cor(' Host : ','branco')+cor(str(self.HOST),'ciano')+cor(' BUFFER : ','branco')+cor(str(self.RECV_BUFFER),'ciano')+cor(' ]','branco')
        except socket.error, e:
            #print msg_controle('ERRO')+cor('[ Não foi possivel estabelecer conexão ]','branco')
            self.client_socket.close()
        
    def Pegar_arquivo(self,NOME_ARQ):
        try:
            with open ('Downloads/'+NOME_ARQ,"w") as arquivo:
                while True:
                    msg = self.client_socket.recv(self.RECV_BUFFER)
                    if not msg: break
                    arquivo.write(msg)
            #sys.stdout.write('\r\n'); sys.stdout.flush()
            print msg_controle('OK')+cor('[ Arquivo : ','branco')+cor(NOME_ARQ,'ciano')+cor(' transferido com sucesso ]','branco')
            sys.stdout.write('\r'+cor('[%s] : '%self.NICK,'branco')); sys.stdout.flush()
        except Exception, e:
            #print e
            print msg_controle('ERRO')+cor('[ Ocorreu algum erro na transferência ]','branco')
        #print msg_controle('!')+cor('[ Background cliente Offline ]','branco')
        #sys.stdout.write(cor(self.NICK,'verde') + ' : '); sys.stdout.flush()
        self.client_socket.close()