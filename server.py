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
    
    with open('dados.json', 'w') as json_file:
        json_file.write(jsonData)


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

def validateType(type):
    return type == '1' or type == '2'

def validateProtocolo(protocolo):
    try:
        number = int(protocolo)
        return number >= 66 and number <= 68
    except: 
        return False

def validateUtc(utc):
    try:
        return bool(datetime.strptime(utc, '%y%m%d%H%M%S'))
    except:
        return False

def validateStatus(status):
    return status =='0' or status == '1'

def validateId(id):
    return len(id == 3)

def validateRules(json):
    return validateType(json["type"]) and validateProtocolo(json["protocolo"]) and validateUtc(json["utc"]) and validateStatus(json["status"]) and validateId(json["id"])

def saveData(jsonData):
    createTable()
    if validateRules(jsonData):
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
            print("Não foi possível conectar ao banco")
    else:
        return "Dados invalidos"

startServer()