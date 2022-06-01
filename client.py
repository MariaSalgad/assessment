import socket
import random
import string
from datetime import datetime
import time
import _thread

keyPressed = None

def sendMessageToServer(message):
    bytesToSend = str.encode(message)

    serverAddressPort = ("127.0.0.1", 20001)
    bufferSize = 1024

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = format(msgFromServer[0])[1:]
    print (msg)

def createType():
    return random.randint(1,2)

def createProtocolo():
    return random.randint(66,68)

def createUtc():
    dateTimeAtual = datetime.now()
    utc = dateTimeAtual.strftime('%y%m%d%H%M%S')
    return utc

def createStatus():
    return random.randint(0,1)

def createId():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(3))

def createMessage():
    result = '>DATA' + str(createType()) + ',' + str(createProtocolo()) + ',' + createUtc() + ',' +str(createStatus()) + ';ID=' + createId() + "<"
    return result

def input_thread(a_list):
    input()
    print("Fim do serviço")
    a_list.append(True)
    
def startTimeMessage():
    a_list = []
    _thread.start_new_thread(input_thread, (a_list,))
    print("Inicio do serviço")
    print("\n####################")
    print("\nPressione Enter para finalizar a execução")
    print("\n####################\n")
    while not a_list:
        sendMessageToServer(createMessage())
        time.sleep(1)
    

startTimeMessage()