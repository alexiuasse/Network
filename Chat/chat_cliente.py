# -*- coding: utf-8 -*-

import sys, socket, select, signal, commands, os, thread
from mensagens import *
from background_client import *
 
class Cliente():
    def __init__(self, HOST, PORTA, NICK):
        self.HOST = HOST
        self.PORTA = int(PORTA)
        self.NICK = NICK[:10]
        self.NOME_ARQ = ''
        self.BUFFER = 4096
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        
        # conectar to servidor
        try :
            self.client_socket.connect((self.HOST,self.PORTA))
            # enviar o nick para o servidor
            self.client_socket.send(self.NICK)
        except :
            print msg_controle('ERRO')+cor('[ Não foi possivel conectar ]','branco')
            sys.exit()
            
        print msg_controle('OK')+cor('[ Conectado ]','branco')
        print msg_controle('...')+cor('[ Porta : ','branco')+cor(str(self.PORTA),'ciano')+cor(' Host : ','branco')+cor(str(self.HOST),'ciano')+cor(' Nick : ','branco')+cor(NICK,'ciano')+cor(' ]','branco')
        print msg_controle('!')+cor('[ -H para imprimir os comandos disponiveis ] ','branco')
        print comandos_cliente()
        
    def chat_client(self):
        self.NICK = cor(self.NICK,'ciano')
        print msg_controle('OK')+cor('[ Comece a se divertir ','branco')+cor(':D ','negrito')+cor(']\n','branco')
        sys.stdout.write(cor('[%s] : ' %self.NICK,'branco')); sys.stdout.flush()
        
        while True:
            
            # pegar o sinal do ctrl + c
            signal.signal(signal.SIGINT, self.signal_handler)
            # pegar o sinal do ctrl + z, previnir que a porta fique ocupada
            signal.signal(signal.SIGTSTP, self.signal_handler)
            
            socket_list = [sys.stdin, self.client_socket]
            
            # Get the list sockets which are readable
            ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
            
            for sock in ready_to_read:
                if sock == self.client_socket:
                    # incoming message from remote server, self.client_socket
                    data = sock.recv(4096)
                    if not data :
                        print '\r'+msg_controle('!')+cor('[ Desconectado do servidor ]','branco')
                        sys.exit()
                    else :
                        # quer dizer que o servidor criou um servidor em 'background' para atender o cliente
                        if (len(data) > 0 ) and (data[0] == '$'):
                            #self.Pegar_arquivos(data)
                            self.comandos(data)
                        else:
                            data = data + "                        "
                            sys.stdout.write('\r'+data)
                        sys.stdout.write('\n\r'+cor('[%s] : '%self.NICK,'branco')); sys.stdout.flush()
                # pegar o que o usuario digitou e enviar
                else :
                    # user entered a message
                    msg = sys.stdin.readline().rstrip('\n')
                    sys.stdout.write('\r'+cor('[%s] : '%self.NICK,'branco')); sys.stdout.flush()
                    # digitou algum comando
                    if (len(msg) > 1) and (msg[0] == '$'):
                        if msg == '$SAIR()':
                            print '\r'+'Bye <3'+"                      "
                            self.client_socket.close()
                            sys.exit(0)
                        # enviar somente o comando
                        self.client_socket.send(msg)
                        self.NOME_ARQ = msg.split('(', 1)[1].split(')')[0]
                    # solicitou ajuda
                    elif msg == '-H':
                        print comandos_cliente()
                        sys.stdout.write('\r'+cor('[%s] : '%self.NICK,'branco')); sys.stdout.flush()
                    # se não for mensagem vazia
                    elif not(msg.count(' ') == len(msg)):
                        self.client_socket.send(msg)
                    #sys.stdout.write(cor('[%s] : '%self.NICK,'branco')); sys.stdout.flush()
                
    def signal_handler(self, signal, frame):
        self.client_socket.close()
        sys.stdout.write('\rBye <3                  \n'); sys.stdout.flush()
        sys.exit(0)
    
    # comandos disponiveis para serem utilizados
    def comandos(self,mensagem):
        if mensagem == '$LS':
            diretorio = '$LS()\n'
            diretorio = diretorio + (commands.getoutput("ls Documentos"))
            self.client_socket.send(diretorio)
        else:
            self.Pegar_arquivos(mensagem)
    
    def Pegar_arquivos(self, mensagem):
        mensagem = mensagem.rsplit('$')
        back_cliente = Background_cliente(self.HOST,mensagem[1],self.BUFFER,self.NOME_ARQ,self.NICK)
        thread.start_new_thread(back_cliente.Pegar_arquivo, tuple([self.NOME_ARQ]))

if __name__ == "__main__":
    if(len(sys.argv) < 4):
        print msg_controle('ERRO')+cor('[ Modo de uso python chat_cliente ','branco')+cor('HOST PORTA NICK','verde')+cor(' obs: NICK deve conter menos que 10 caracteres]','branco')
        sys.exit()
        
    HOST = sys.argv[1]
    PORTA = int(sys.argv[2])
    NICK = sys.argv[3]
    if len(NICK) > 10:
        print msg_controle('ERRO')+cor('[ NICK maior que o permitido ','branco')

    cliente = Cliente(HOST,PORTA,NICK)
    cliente.chat_client()