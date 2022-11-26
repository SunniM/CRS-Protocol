import socket
import os
import Services
import multiprocessing as mp

#SRVR_IP = '10.0.0.2'
SRVR_IP = '127.0.0.1'
SRVR_PORT = 59001
REND_PORT = 59002
CTRL_PORT = 59003
MSG_SIZE = 1000
pause = mp.Value('d', 0)

   
def main():
    # Creating Controller/Renderer Sockets
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    c_sock.bind((SRVR_IP, CTRL_PORT))
    r_sock.bind((SRVR_IP, REND_PORT))

    data, address = c_sock.recvfrom(MSG_SIZE)
    messageType, morePortions, message = Services.parseMessage(data)
    print('Message Type: ' + messageType)
    print('More Portions: ' + morePortions)
    if(messageType == '10'):
        file_list = getFileList()
        portions = portion(file_list)
        for portion in portions:
            message = Services.build_Message('11',portion[1],portion[0])
            c_sock.sendto(message, address)
    
    exit = False

    while not exit:
        data, address = r_sock.recvfrom(MSG_SIZE)
        messageType, morePortions, message = Services.parseMessage(data)
        print('Message Type: ' + messageType)
        print('More Portions: ' + morePortions)
        print("received message: " + message)
        
        match messageType:
            case '20':          #Render file
                global p
                p = mp.Process(target=renderFile, args=(message, address, r_sock))
                p.start()

            case '30':          #Pause File
                pause.value = 1
                message = Services.build_Message('31','0','')
                r_sock.sendto(message,address)
            
            case '32':          #Resume File
                pause.value = 0
                message = Services.build_Message('33','0','')
                r_sock.sendto(message,address)
            
            case '34':          #Restart File
                p.terminate()
                p.start()
                
            case '99':          #Exit
                p.terminate()
                exit = True


def renderFile(data, address, r_sock):
    f = open(data, "r")
    fileContents = f.read()
    portions = portion(fileContents)           
    for portion in portions:
        while(pause == 1):      #so if pause is set to true then the child is caught in this loop
            print()
        if(pause == 0):         #Once pause is set to 0 the child escapes the loop and continues sending
            message = Services.build_Message('21',portion[1],portion[0])
            r_sock.sendto(message, address)            

def getFileList():
    file_list = ','
    for _, _, file in os.walk('./files'):
        file_list = file_list.join(file)
    print(file_list)
    return file_list

def portion(message):
    messageLen = len(message.encode())
    portionedMessage = []

    for i in range(0, messageLen, MSG_SIZE):
        portionedMessage.append([message[i:i+MSG_SIZE],'1'])

    portionedMessage[len(portionedMessage)-1][1] = '0'

    return portionedMessage
    

if __name__ == '__main__':
    main()