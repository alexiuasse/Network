# -*- coding: iso-8859-1 -*-

def cor_texto(cor):
	cores = {
            'vermelho': '\33[31m',
            'verde': '\33[32m',
            'azul': '\33[34m',
            'ciano': '\33[36m',
            'magenta': '\33[35m',
            'amarelo': '\33[33m',
            'preto': '\33[30m',
            'branco': '\33[37m',
            'original': '\33[0;0m',
            'reverso': '\33[2m',
            'negrito': '\33[1m'
	}

	return cores[cor]
    
def cor(mensagem,cor):
    return cor_texto(cor)+ mensagem + cor_texto('original')

def msg_controle(tipo):
    controle = {
        'ERRO' : '\r\033[91m[ ! ]\033[0m ',
        '...' : '\r\033[93m[ . ]\033[0m ',
        '!' : '\r\033[93m[ ! ]\033[0m ',
        'OK' : '\r\033[92m[ OK ]\033[0m '
    }
    
    return controle[tipo]

def comandos_cliente():
    m1 = msg_controle('!')+"[ $LA()\t,listagem de arquivos ]\n"
    m2 = msg_controle('!')+"[ $LU()\t,listagem de usuarios ]\n"
    m3 = msg_controle('!')+"[ $PA(\33[36mARQUIVO\33[0;0m)\t,pegar um arquivo ]\n"
    m4 = msg_controle('!')+"[ $SAIR()\t, sair do programa ]"
    mensagem = m1 + m2 + m3 + m4
    return cor(mensagem,'branco')








