import socket
import os
import Services
import multiprocessing
from multiprocessing import Value

#SRVR_IP = '10.0.0.2'
SRVR_IP = '127.0.0.1'
REND_PORT = 59001
CTRL_PORT = 59002
MSG_SIZE = 1000

   
def main():
    # Creating Controller/Renderer Sockets
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    c_sock.bind((SRVR_IP, CTRL_PORT))
    r_sock.bind((SRVR_IP, REND_PORT))

    exit = False
    pause = Value('d', 0)

    while not exit:
        data, address = c_sock.recvfrom(MSG_SIZE)
        messageType, morePortions, message = Services.parseMessage(data)
        print('Message Type: ' + messageType)
        print('More Portions: ' + morePortions)
        match messageType:
            case '10':          #File list
                file_list = getFileList()
                portions = portion(file_list)
                for p in portions:
                    message = Services.build_Message('11',p[1],p[0])
                    c_sock.sendto(message.encode(), address)
            
            case '20':          #Render file    
                pid = os.fork()
                if(pid > 0):
                    print()
                else:
                    f = open(data, "r")
                    fileContents = f.read()
                    portions = portion(fileContents)           
                    for p in portions:
                        while(pause == 1):      #so if pause is set to true then the child is caught in this loop
                            print()

                        if(pause == 0):         #Once pause is set to 0 the child escapes the loop and continues sending
                            message = Services.build_Message('21',p[1],p[0])
                            r_sock.sendto(message.encode(), address)            #TO DO: what address?
                
                    children = multiprocessing.active_children()    #Should we terminate the child after it's done sending?
                    for child in children:
                        child.terminate()

            case '30':          #Pause File
                if(pid > 0):
                    pause.value = 1
                    message = Services.build_Message('31','0','')
                    r_sock.sendto(message.encode(),address)
            
            case '32':          #Resume File
                if(pid > 0):
                    pause.value = 0
                    message = Services.build_Message('33','0','')
                    r_sock.sendto(message.encode(),address)
            
            case '34':          #restart File
                if(pid > 0):    
                    children = multiprocessing.active_children()    #Terminating children in python is hard, this will terminate all children but there should only be one
                    for child in children:
                        child.terminate()
                
                pid = os.fork()
                if(pid > 0):    
                    print()
                else:           
                    f = open(data, "r")
                    fileContents = f.read()
                    portions = portion(fileContents)           
                    for p in portions:
                        for p in portions:
                            while(pause == 1):      #so if pause is set to true then the child is caught in this loop
                                print() #don't know what goes here, but nothing i guess

                            if(pause == 0):         #Once pause is set to 0 the child escapes the loop and continues sending
                                message = Services.build_Message('21',p[1],p[0])
                                r_sock.sendto(message.encode(), address)            #TO DO: what address?
                    
                    children = multiprocessing.active_children()    #Should we terminate the child after it's done sending?
                    for child in children:
                        child.terminate()


            case '99':          #Exit
                children = multiprocessing.active_children()    
                for child in children:
                    child.terminate()
                
                exit = True

        print("received message: %s" % data)

def getFileList():
    file_list = ','
    for _, _, file in os.walk('./files'):
        file_list = file_list.join(file)
    print(file_list)
    return file_list

def streamFile(file_name):
    with open(file_name) as file:
        line = file.readlines()
    os._exit()

def portion(message):
    messageLen = len(message.encode())
    portionedMessage = []

    for i in range(0, messageLen, MSG_SIZE):
        portionedMessage.append([message[i:i+MSG_SIZE],'1'])

    portionedMessage[len(portionedMessage)-1][1] = '0'

    return portionedMessage
    

if __name__ == '__main__':
    main()