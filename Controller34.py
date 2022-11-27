import socket
import sys, os
import Services
import multiprocessing as mp
import threading
mp.allow_connection_pickling()


#print(file_list.split(','))

SRVR_IP = '127.0.0.1'
SRVR_PORT = 59001
SRVR_ADDR = (SRVR_IP, SRVR_PORT)

REND_IP = '127.0.0.1'
REND_PORT = 59002
REND_ADDR = (REND_IP, REND_PORT)

MSG_SIZE = 500

# ctrl > rend > serv
# ctrl > serv

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(Services.build_Message('10','0',''), SRVR_ADDR)
    data, _ = sock.recvfrom(MSG_SIZE)
    messageType, _, message = Services.parseMessage(data)
    if messageType == '11':
        files = message.split(',')
    
    global rendering
    rendering = False
    exit = False
    while (not exit):
        for i in range(len(files)):
                print('[{0}] {1}'.format(i+1, files[i]))
        print('[{0}] EXIT'.format(len(files) + 1))
        print('Select a file: ')

        x = int(input())
        if (x == (len(files) + 1)):
            exit = True
            message = Services.build_Message('99', '0', '')
            sock.sendto(message, REND_ADDR)
            sock.sendto(message, SRVR_ADDR)
            break
        else:
            x = files[x-1]
            message = Services.build_Message('20', '0', x)
            sock.sendto(message, REND_ADDR)
            data, _ = sock.recvfrom(MSG_SIZE)
            messageType, _, message = Services.parseMessage(data)
            if messageType == '22':
                rendering = True
                #newstdin = os.dup(sys.stdin.fileno())
                global p
                p = threading.Thread(target=render_controls, args=(sock,))
                p.start()

        while(rendering):
            print("TEST")
            data, _ = sock.recvfrom(MSG_SIZE)
            messageType, _, message = Services.parseMessage(data)
            if(messageType == '23'):
                rendering = False
                print("Rendering Complete Press Enter")
                p.join()

def render_controls(sock):
    #sys.stdin = os.fdopen(newstdin)
    while(rendering):
        print("1. Pause \n2. Resume \n3. Restart")
        selection = input()
        if rendering:
            if selection == '1':
                message = Services.build_Message('30','0','')
                sock.sendto(message, REND_ADDR)

            elif selection == '2':
                    message = Services.build_Message('32','0','')
                    sock.sendto(message, REND_ADDR)

            elif selection =='3':
                message = Services.build_Message('34','0','')
                sock.sendto(message, REND_ADDR)

if __name__ == '__main__':
    main()