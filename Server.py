import socket
import threading


DictOfUsers = {}


def ListenComand():
    while True:
        Command, UsAddr = INCommSock.recvfrom(BufferOfListen)
        threading.Thread(target=CommandProcessing, args=(Command, UsAddr,)).start()


def CommandProcessing(Command, UsAddr):
    Command = Command.decode()
    if Command != '':
        if Command[0] == '/':
            if not (UsAddr in DictOfUsers):
                DictOfUsers[UsAddr] = Command[1:]
                for i in DictOfUsers:
                    OUTCommSock.sendto(bytes(('SERVER: ' + Command[1:] + ' joined the chat!').encode('UTF-8')), i)
        elif Command == 'exit' and UsAddr in DictOfUsers:
            for i in DictOfUsers:
                if i != UsAddr:
                    OUTCommSock.sendto(bytes(('SERVER: '+DictOfUsers[UsAddr]+' has left the chat!').encode('UTF-8')), i)
            del DictOfUsers[UsAddr]
        elif Command == 'who is here' and UsAddr in DictOfUsers:
            OUTCommSock.sendto(bytes(('Users on the server:'+'-'+'-'.join(list(DictOfUsers.values()))).encode('UTF-8')), UsAddr)


def ListenUsers():
    while True:
        Data, UsAddr = INMessSock.recvfrom(BufferOfListen)
        threading.Thread(target=DataProcessing, args=(Data, UsAddr,)).start()


def DataProcessing(Data, UsAddr):
    Data = Data.decode()
    if Data != '' and UsAddr in DictOfUsers:
        for i in DictOfUsers:
            if i != UsAddr:
                OUTMessSock.sendto(bytes((DictOfUsers[UsAddr]+': '+Data).encode('UTF-8')), i)


BufferOfListen = 2**int(input('Enter the buffer: '))
SocketOfCommServer = int(input('Enter the command socket number: '))
SocketOfMessServer = int(input('Enter the message socket number: '))

Address = socket.gethostname()
INMessSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
INMessSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
INMessSock.bind((Address, SocketOfMessServer))

INCommSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
INCommSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
INCommSock.bind((Address, SocketOfCommServer))

OUTMessSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
OUTMessSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

OUTCommSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
OUTCommSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

threading.Thread(target=ListenComand).start()
threading.Thread(target=ListenUsers).start()

print("Server was started!")
print("The server's command socket address is:", str(INCommSock).split('(')[1].strip('>').strip(')'))
print("The server's message socket address is:", str(INMessSock).split('(')[1].strip('>').strip(')'))

while True:
    command = input('\n//: ')
    print()
    if len(command) >= 6:
        if command[0] == '/':
            if command[1:] == 'users':
                for i in DictOfUsers:
                    print('{0:<20}{1:>35}'.format(DictOfUsers[i], str(i)))
                print()
                print('Now there are', len(DictOfUsers), 'users on the server')
            elif command[1:4] == 'add':
                command = command.split(' ')[1:]
                DictOfUsers[(command[0], int(command[1]),)] = command[2]
                print(command[2], 'was added!')
            elif command[1:4] == 'del':
                command = command.split(' ')
                command = (command[1], int(command[2]),)
                print(DictOfUsers[command], command, 'was deleted')
                OUTCommSock.sendto(bytes('exit'.encode('UTF-8')), command)
                del DictOfUsers[command]
            elif command[1:] == 'clean all':
                for i in DictOfUsers.copy():
                    print(DictOfUsers[i], 'was deleted')
                    OUTCommSock.sendto(bytes('exit'.encode('UTF-8')), i)
                    del DictOfUsers[i]
