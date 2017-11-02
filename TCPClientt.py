# -*- coding: cp1252 -*-
import socket
from traceback import print_exc
import sys

HOST = 'localhost'               # IP of server
PORT = 9009                     # Port of server
ERROR = '\033[91m[ERROR]\033[0m\t'
WAIT = '\033[93m[WAIT]\033[0m\t'
OK = '\033[92m[OK]\033[0m\t'
try:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    print WAIT,"Trying to stablish conection with the server: ", '\033[92m',dest,'\033[0m'
    tcp.connect(dest)
    msg = tcp.recv(512)            # message from server requesting a name
    print repr(msg)
    if msg:
        print OK,"Connect with success: ", '\033[92m',dest,'\033[0m'
    fileReq = raw_input("\033[92m[OK]\033[0m\tArchive to request: ")
    tcp.send(fileReq)
    msg = tcp.recv(512)
    if not msg:
        print ERROR,"Server sent nothing"
        print ERROR,"Closing the connection"
        tcp.close()
        print ERROR,"Connection close, leaving now"
        sys.exit(1)
    with open ('Client',"w") as archive:
        while True:
            if not msg: break       # if msg has nothing, so is FALSE
            archive.write (msg)
            msg = tcp.recv(512)
            #print msg
    print OK,"Connection Finished"
    tcp.close()
except Exception :
    print '\033[91m\033[1m'
    print_exc()
    print '\033[0m'
    print ERROR,"Closing client"
    if tcp:
        print ERROR,"Closing connection"
        tcp.close()
    print ERROR,"Bye ..." 
