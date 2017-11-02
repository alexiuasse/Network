# -*- coding: cp1252 -*-
import socket
import os
import commands
import thread

ErrorIO = "Arquivo nao encontrado!\nLista de arquivos Disponiveis: \n"

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

def conectado(con, cliente):            # Função para conexão
    print 'Conectado por', cliente
    con.send(commands.getoutput("ls"))
    try:
        fileReq = con.recv(100)
        with open (fileReq,"r") as arquivo:
            statinfo = os.stat(fileReq)
            print 'Tamanho do arquivo em bytes: ', statinfo.st_size
            i = 0
            while True:
                print 'Enviando arquivo ', i
                text = arquivo.read(512)
                if text == "":
                    break
                con.send(text)
                i = i + 1
    except IOError:                     # Tratamento de error para IO
        arqDir = commands.getoutput("ls")
        con.send(ErrorIO+arqDir+'\n')
    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criar socket

orig = (HOST, PORT)
tcp.bind(orig)          # Associa uma porta a uma determinada interface de rede

tcp.listen(5)           # Ouvir até 5

print 'Servidor online ...'
while True:
    con, cliente = tcp.accept()     # Aceitar conexão
    thread.start_new_thread(conectado, tuple([con,cliente]))    # Thread

tcp.close()