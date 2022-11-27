import socket
import os, time
import Services
import multiprocessing as mp

SRVR_IP = '10.0.0.2'
#SRVR_IP = '127.0.0.1'
SRVR_PORT = 59001
REND_PORT = 59002
CTRL_PORT = 59003
MSG_SIZE = 500

   
def main():
    # Creating Controller/Renderer Sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SRVR_IP, SRVR_PORT))

    lastRequestedFile = ''
    exit = False
    pause = mp.Value('i', 0)

    while not exit:
        data, address = sock.recvfrom(MSG_SIZE)
        messageType, morePortions, message = Services.parseMessage(data)
        print('Message Type: ' + messageType)
        print('More Portions: ' + morePortions)
        print('Received Message: ' + message)

        if messageType == '10':          # Respond with file list
            file_list = getFileList()
            portions = portion(file_list)
            for p in portions:
                message = Services.build_Message('11', p[1], p[0])
                sock.sendto(message, address)

        elif messageType == '20':          #Render file
                lastRequestedFile = message
                global proc
                proc = mp.Process(target=renderFile, args=(message, address, pause))
                proc.start()

        elif messageType == '30':          #Pause File
            pause.value = 1
            message = Services.build_Message('31','0','')
            sock.sendto(message,address)

        elif messageType == '32':          #Resume File
            pause.value = 0
            message = Services.build_Message('33','0','')
            sock.sendto(message,address)

        elif messageType ==  '34':          #Restart File
            proc.terminate()
            pause.value = 0
            proc = mp.Process(target=renderFile, args=(lastRequestedFile, address, pause))
            proc.start()

        elif messageType ==  '99':          #Exit
            proc.join()
            exit = True


def renderFile(data, address, pause):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    f = open('./files/' + data, "r")
    fileContents = f.read()
    portions = portion(fileContents)
    for p in portions:
        time.sleep(2)
        while(pause.value == 1):      #so if pause is set to true then the child is caught in this loop
            pass
        if(pause.value == 0):         #Once pause is set to 0 the child escapes the loop and continues sending
            message = Services.build_Message('21',p[1],p[0])
            sock.sendto(message, address)
    

def getFileList():
    file_list = ','
    for _, _, file in os.walk('./files'):
        file_list = file_list.join(file)
    return file_list

def portion(message):
    messageLen = len(message.encode())
    portionedMessage = []

    for i in range(0, messageLen, MSG_SIZE-3):
        portionedMessage.append([message[i:i+MSG_SIZE-3],'1'])

    portionedMessage[len(portionedMessage)-1][1] = '0'

    return portionedMessage
    

if __name__ == '__main__':
    main()