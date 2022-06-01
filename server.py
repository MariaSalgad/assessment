import json
import socket
import mysql.connector
from datetime import datetime
import re

from numpy import save

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
        jsonData = createJsonUsing(message)
        
        msgFromServer = saveData(jsonData)
        
        clientMsg = format(message)
        print(clientMsg[1:])
        address = bytesAddressPair[1]
    
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)

def createJsonUsing(message):
    (objectList, idNumber) = splitMessageInListAndIdNumber(message)
    time_date = createTimeUsing(objectList)

    data = {'type': createTypeUsing(objectList),
    'protocolo': createProtocoloUsing(objectList),
    'utc': createStringTimeUsing(time_date),
    'status': createStatusUsing(objectList),
    'id': idNumber}

    saveJsonFile(data)
    return data

def saveJsonFile(data):
    jsonData = json.dumps(data)
    
    with open('dados.json', 'a') as json_file:
        json_file.write(jsonData+",\n")


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

def databaseConnection():    
    try:
        con = mysql.connector.connect(host='localhost',database='teste',user='root',password='')
        if con.is_connected():
            db_info = con.get_server_info()
            print("Conectado ao servidor MySQL versão ",db_info)
            cursor = con.cursor()
            cursor.execute("select database();")
            linha = cursor.fetchone()
            print("Conectado ao banco de dados ",linha)
            return (con, cursor)
    except mysql.connector.Error:
        print("Não foi possível conectar ao banco")
        
def createTable():
    
    (connection, cursor) = databaseConnection()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS dev_status 
                (type INT, protocolo INT, utc DATETIME, status INT, id VARCHAR(255))''')
        connection.commit()
        connection.close()
    except:
        connection.close()

def saveData(jsonData):
    createTable()
    query = ("INSERT INTO dev_status(type, protocolo, utc, status, id) VALUES(%s,%s,%s,%s,%s)")
    values = (jsonData["type"], jsonData["protocolo"], jsonData["utc"], jsonData["status"], jsonData["id"])
    try:
        print(jsonData)
        (connection, cursor) = databaseConnection()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return "Dados salvos com sucesso"
    except mysql.connector.Error:
            return "Não foi possível conectar ao banco de dados"
startServer()