import socket
import threading


def Listen():
    while True:
        Data = sock.recv(2**18).decode()
        print(Data)


adress = socket.gethostname()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((adress, 11723))
print("your address is:", str(sock).split('(')[1].strip('>').strip(')'))
ToIp = input('ToIp: ')
ToSOCK = input('ToSOCK: ')

threading.Thread(target=Listen).start()

while True:
    k = input()
    sock.sendto(bytes((ToIp+'`'+ToSOCK+'`'+k+' ').encode('UTF-8')), ('192.168.11.73', 11719))