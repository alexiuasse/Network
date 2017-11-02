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
        'ERRO' : '\033[91m[ ! ]\033[0m\t',
        '...' : '\033[93m[ .. ]\033[0m\t',
        '!' : '\033[93m[ ! ]\033[0m\t',
        'OK' : '\033[92m[ OK ]\033[0m\t'
    }
    
    return controle[tipo]

def comandos_cliente():
    return msg_controle('!')+cor('[ $lista_arquivos() $lista_usuarios() $pega_arquivos(','branco')+cor('ARQUIVO','ciano')+cor(') ]','branco')