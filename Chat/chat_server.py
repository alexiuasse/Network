# -*- coding: utf-8 -*-

import sys, socket, select, signal, time, thread
from background_server import *
from mensagens import *

class Servidor():
    def __init__(self,HOST,PORT,RECV_BUFFER):
        
        self.SOCKET_LIST = []
        self.USUARIOS = {}
        self.ARQUIVOS = {}
        self.HOST = HOST
        self.PORT = int(PORT)
        self.sock_e = None
        self.RECV_BUFFER = RECV_BUFFER
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # para debugar, deixa a porta livre
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        while True:
            try:
                self.server_socket.bind((self.HOST, self.PORT))
                break
            except Exception:
                self.PORT = self.PORT + 1
        
        self.server_socket.listen(10)

        print msg_controle('OK')+cor('[ Servidor Online ]\n','branco')
        print msg_controle('...')+cor('[ Porta : ','branco')+cor(str(self.PORT),'ciano')+cor(' Host : ','branco')+cor(str(self.HOST),'ciano')+cor(' BUFFER : ','branco')+cor(str(self.RECV_BUFFER),'ciano')+cor(' ]','branco')

        # adiciona um objeto server_socket à lista de conexões legíveis (readble)
        # server socket object to the list of readable connections
        self.SOCKET_LIST.append(self.server_socket)

    def chat_server(self, frequencia):
        
        print msg_controle('...')+cor('[ Entrando em Loop ]','branco')
        print msg_controle('...')+cor('[ Atualizando a cada ','branco')+cor(str(frequencia),'ciano')+cor(' segundos ]\n','branco')
        barra = 1
        
        while True:
            
            # pegar o sinal do ctrl + c
            signal.signal(signal.SIGINT, self.signal_handler)
            # pegar o sinal do ctrl + z, previnir de listen 'zumbi'
            signal.signal(signal.SIGTSTP, self.signal_handler)
            
            if barra:
                time.sleep(frequencia)
                sys.stdout.write('\r\\'); sys.stdout.flush()
                barra = 0
            else:
                time.sleep(frequencia)
                sys.stdout.write('\r/'); sys.stdout.flush()
                barra = 1
            
            # pega a lista de sockets que estão prontos para ler através do select
            # 4º argumento é time_out = 0 : seleciona e nunca bloqueia
            # ready_to_read = notifica quando um socket tem dados disponíveis
            # ready_to_write = dados disponíveis para escrever
            # in_error = erros ocorrido nos socket
            
            ready_to_read,ready_to_write,in_error = select.select(self.SOCKET_LIST,[],[],0)
            
            # para cada socket em ready_to_read
            for sock in ready_to_read:
                # se sock for socket do servidor, então uma nova requisição de conexão foi recebida
                if sock == self.server_socket: 
                    sockfd, addr = self.server_socket.accept()
                    self.SOCKET_LIST.append(sockfd)
                    # NICK do usuario
                    NICK = sockfd.recv(self.RECV_BUFFER)
                    # associar addr com NICK, por meio de dicionario
                    self.USUARIOS.update({sockfd:NICK})
                    
                    print "\r"+msg_controle('!')+cor('[ %s conectou ]' %cor(self.USUARIOS[sockfd],'verde'),'branco')
                    
                    self.broadcast(self.server_socket, sockfd, msg_controle('!')+cor('[ %s conectou ]' %cor(self.USUARIOS[sockfd],'verde'),'branco'),0)
                # senão, é uma mensagem do cliente
                else:
                    # dados do processo recebido do cliente
                    try:
                        # recebendo dados do socket
                        data = sock.recv(self.RECV_BUFFER)
                        # existe dados no socket
                        if data:
                            # achou um comando
                            if data[0] == '$':
                                self.comandos(data, sock)
                            else:
                                self.broadcast(self.server_socket, sock, cor('[%s] : ' %cor(self.USUARIOS[sock],'verde'),'branco')+data, 0)
                        else:
                            # remove o socket que foi corrompido
                            if sock in self.SOCKET_LIST:
                                self.SOCKET_LIST.remove(sock)
                                # nesta fase, nenhum dado significa que provavelmente a conexão foi corrompida
                                self.broadcast(self.server_socket, sock, msg_controle('!')+cor('[ %s saiu ]' %cor(self.USUARIOS[sock],'verde'),'branco'),0)
                                del self.USUARIOS[sock]
                    # exceção
                    except:
                        #self.broadcast(self.server_socket, sock, msg_controle('!')+cor('[ %s saiu ]' %cor(self.USUARIOS[self.sock_deletado],'verde'),'branco'), 0)
                        #del self.USUARIOS[self.sock_deletado]
                        continue

        self.server_socket.close()
        
    # mensagens do chat em broadcast para todos os clientes conectados
    def broadcast (self, server_socket, sock, message, flag):
        
        # se flag ativa, então o servidor esta conversando diretamente com o cliente que fez a requisição de algum comando
        if flag:
            print '\r'+msg_controle('!')+cor('[ Broadcasting servidor ]','branco')
            for socket in self.SOCKET_LIST:
                # envia a mensagem somente para os peers
                if socket != self.server_socket and socket == sock :
                    try :
                        socket.send(message)
                    except :
                        # termina a conexão do socket
                        socket.close()
                        # fecha o socket, remove-o
                        if socket in self.SOCKET_LIST:
                            self.SOCKET_LIST.remove(socket)
                            
        else:
            print '\r'+msg_controle('!')+cor('[ Broadcasting usuario ]','branco')
            for socket in self.SOCKET_LIST:
                # envia a mensagem somente para os peers
                if socket != self.server_socket and socket != sock :
                    try :
                        socket.send(message)
                    except :
                        # termina a conexão do socket
                        socket.close()
                        # fecha o socket, remove-o
                        if socket in self.SOCKET_LIST:
                            self.SOCKET_LIST.remove(socket)
    
    # comandos disponiveis para serem utilizados
    def comandos(self,mensagem,sock):
        i = mensagem.find('(')
        if mensagem[:i] == '$LA':
            self.sock_e = sock
            self.lista_arquivos(sock)
        elif mensagem[:i] == '$LU':
            self.lista_usuarios(sock)
        elif mensagem[:i] == '$PA':
            nome = mensagem.split('(', 1)[1].split(')')[0]
            self.pega_arquivos(sock, nome)
        elif mensagem[:i] == '$LS':
            diretorio = mensagem.split("\n")
            diretorio = diretorio[1:]
            for i in diretorio:
                self.ARQUIVOS.update({i:sock})
            self.broadcast(self.server_socket, self.sock_e, str(self.ARQUIVOS.keys()),1)
        else:
            pass
    
    #con.send(commands.getoutput("ls")) em cada usuario
    def lista_arquivos(self,sock):
        self.broadcast(self.server_socket, sock, '$LS', 0)
    
    # temos que fazer um dicionario que liga um ip com um nome
    # ao se conectar o usuario deve mandar o nick
    def lista_usuarios(self,sock):
        online = ','.join(self.USUARIOS.values())
        self.broadcast(self.server_socket, sock, msg_controle('...')+cor('[ '+online+' ] ','branco') , 1)
    
    # fazer de um jeito que o usuario manda o arquivo que quer em um unico comando
    # se ele quer pegar um arquivo, cria uma conexão tcp em background para isso
    def pega_arquivos(self,sock,nome):
        sys.stdout.write('\r\n\r'); sys.stdout.flush()
        back_server = Background_servidor()
        back_server.Background(self.HOST,self.PORT,self.RECV_BUFFER, nome)
        porta = back_server.Pega_porta()
        # mandar a porta e host para o client e o client criar um background client para troca de arquivo
        self.broadcast(self.server_socket, sock, '$'+str(porta) , 1)
        thread.start_new_thread(back_server.Mandar_arquivo, tuple([nome]))
    
    def signal_handler(self, signal, frame):
        self.server_socket.close()
        sys.stdout.write('\rBye <3\n'); sys.stdout.flush()
        sys.exit(0)
 
if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print msg_controle('!')+cor('[ BUFFER pode ser deixado em branco, default 4096 ] ','branco')
        print msg_controle('ERRO')+cor('[ Modo de uso python chat_server ','branco')+cor('HOST PORTA BUFFER','verde')+cor(' ]','branco')
        sys.exit()
        
    host = sys.argv[1]
    porta = sys.argv[2]
    buffer = sys.argv[3] if (len(sys.argv) < 3) else 4096
    
    servidor = Servidor(host,porta,buffer)
    servidor.chat_server(0.1)
