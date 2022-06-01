import socket
import random
import string
from datetime import datetime
import time
import _thread

def sendMessageToServer(message):
    bytesToSend = str.encode(message)

    serverAddressPort = ("127.0.0.1", 20001)
    bufferSize = 1024

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    message = format(msgFromServer[0])[1:]
    print (message)

def createType():
    return random.randint(1,2)

def createProtocolo():
    return random.randint(66,68)

def createUtc():
    actualDateTime = datetime.now()
    utc = actualDateTime.strftime('%y%m%d%H%M%S')
    return utc

def createStatus():
    return random.randint(0,1)

def createId():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(3))

def createMessage():
    message = '>DATA' + str(createType()) + ',' + str(createProtocolo()) + ',' + createUtc() + ',' +str(createStatus()) + ';ID=' + createId() + "<"
    return message

def inputThread(cmdList):
    input()
    print("Fim do serviço")
    cmdList.append(True)
    
def startTimeMessage():
    cmdList = []
    _thread.start_new_thread(inputThread, (cmdList,))
    
    print("Inicio do serviço")
    print("\n####################")
    print("\nPressione Enter para finalizar a execução")
    print("\n####################\n")

    while not cmdList:
        sendMessageToServer(createMessage())
        time.sleep(1)
    

startTimeMessage()