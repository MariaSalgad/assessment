import socket
import re
from datetime import datetime

def startServer():
    localIP     = "127.0.0.1"
    localPort   = 20001
    bufferSize  = 1024

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = format(bytesAddressPair[0])

        clientMsg = format(message)
        print(clientMsg[1:])
        address = bytesAddressPair[1]
        msgFromServer = "Mensagem recebida."
        bytesToSend   = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)

def splitMessageInListAndIdNumber(message):
    lista = message.split(';')
    lista2 = lista[0].split(',')
    idNumber = lista[1]
    id = idNumber[3:6]
    return(lista2,id)

def createTypeUsing(lista: list):
    type = lista[0]
    type = re.sub('[^0-9]', '', type)
    return type

def createProtocoloUsing(lista: list):
    return lista[-3]

def createTimeUsing(lista: list):
    return datetime.strptime(lista[2],'%y%m%d%H%M%S')

def createStringTimeUsing(time):
    return time.strftime('%Y-%m-%d %H:%M:%S')

def createStatusUsing(lista: list):
    return lista[3]