import socket
import Services
import multiprocessing as mp

#print(file_list.split(','))

SRVR_IP = '127.0.0.1'
REND_IP = '127.0.0.1'
SRVR_PORT = 59001
REND_PORT = 59002
CTRL_PORT = 59003
MSG_SIZE = 1000

def main():
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s_sock.sendto(Services.build_Message('10','0',''), (SRVR_IP, SRVR_PORT))
    data, _ = s_sock.recvfrom(MSG_SIZE)
    _, _, message = Services.parseMessage(data)
    files = message.split()

    rendering = False

    exit = False
    while (not exit):
        for i in range(len(files)):
                print('[{0}] {1}'.format(i+1, files[i]))
        print('[{0}] EXIT'.format(len(files)))
        print('Select a file: ')
        x = int(input())
        if(x == len(files)):
            exit = True
            break
        else:
            x = files[x-1]
            message = Services.build_Message('20', '0', x)
            r_sock.sendto(message, (REND_IP, REND_PORT))
            rendering = True
        p = mp.Process(target=render_controls, args=(r_sock))

        while(rendering):
            data, _ = r_sock.recvfrom(MSG_SIZE)
            messageType, _, message = Services.parseMessage(data)
            if(messageType == '23'):
                rendering = False
                p.terminate()

def render_controls(r_sock):
    while(True):
        print("1. Pause \n2. Resume \n3. Restart \n4. Exit")
        selection = input()
        match selection:
            case '1' :
                message = Services.build_Message('30','0','')
            case '2' :
                message = Services.build_Message('32','0','')
            case '3' :
                message = Services.build_Message('34','0','')
            case '4' :
                message = Services.build_Message('99','0','')
            case _:
                r_sock.sendto(message, (REND_IP,REND_PORT))

if __name__ == '__main__':
    main()