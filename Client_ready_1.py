from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import socket
import threading
from random import randint


# Encryption/Decryption


def convert_base(num, to_base=10, from_base=10):
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    del num, from_base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]


def Encrypt(into):
    keys = [randint(ord(into[i]), 46655) for i in range(len(into))]
    cip = [ord(into[i]) ^ keys[i] for i in range(len(into))]
    out = {convert_base(keys[i], to_base=36): convert_base(cip[i], to_base=36) for i in range(len(into))}
    del keys, cip
    return out


def Decrypt(into):
    return ''.join([chr(int(convert_base(list(into.keys())[i], from_base=36)) ^ int(convert_base(list(into.values())[i], from_base=36))) for i in range(len(into))])


# Interface


ServerINFO = []
UserName = str()
BufferOfListen = int()
YourSock = randint(49001, 49150)


def Cs(a):
    s = a.geometry()
    s = s.split('+')
    s = s[0].split('x')
    s[0] = str(int((a.winfo_screenwidth() - int(s[0]))/2))
    s[1] = str(int((a.winfo_screenheight() - int(s[0]))/2))
    a.geometry('+{0}+{1}'.format(s[0], s[1]))
    del s, a


def Exiting():
    raise SystemExit


def Closing():
    MessSock.sendto(bytes('exit'.encode('UTF-8')), (ServerINFO[0], ServerINFO[1]))
    MessSock.sendto(bytes('exit'.encode('UTF-8')), (Address, YourSock))
    Exiting()


def write(self, text):
    self.configure(state=NORMAL)
    self.insert(END, text)
    self.configure(state=DISABLED)
    del text, self


def Send():
    txt = MessageUs.get(1.0, END)
    if not txt.isspace():
        MessageUs.delete(1.0, END)
        txt = txt.strip('\n').strip()
        write(Chat, 'You: ' + txt + '\n')
        Chat.yview(END)
        txt = Encrypt(txt)
        txt = '-'.join(list(txt.keys()))+'+'+'-'.join(list(txt.values()))
        threading.Thread(target=SendToServer, args=(txt,)).start()
    del txt


def SendToServer(txt):
    try:
        MessSock.sendto(bytes(txt.encode('UTF-8')), (ServerINFO[0], ServerINFO[2]))
    except:
        messagebox.showerror(title='ERROR_500', message='Server is offline!!!')


def GetServerAddr():
    root = Tk()
    root.geometry('300x225')
    root.update_idletasks()
    Cs(root)
    root.title("Duda's Chat v3.2")
    root['bg'] = "gray22"
    root.resizable(width=FALSE, height=FALSE)
    root.protocol("WM_DELETE_WINDOW", Exiting)

    f_Bf = Frame(root, bg='grey22')
    f_Bf.pack(side=TOP, fill=X)

    labelPre = Label(f_Bf, text="Enter the buffer: ", fg="white", bg="gray22")
    labelPre.pack(side=LEFT)

    Bfget = Entry(f_Bf, fg="white", bg="gray26")
    Bfget.pack(side=RIGHT, pady=10)

    f_NM = Frame(root, bg='grey22')
    f_NM.pack(side=TOP, fill=X)

    label0 = Label(f_NM, text="Your nickname: ", fg="white", bg="gray22")
    label0.pack(side=LEFT)

    NMget = Entry(f_NM, fg="white", bg="gray26")
    NMget.pack(side=RIGHT, pady=10)

    f_SA = Frame(root, bg='grey22')
    f_SA.pack(side=TOP, fill=X)

    label1 = Label(f_SA, text="Server's address: ", fg="white", bg="gray22")
    label1.pack(side=LEFT)

    SAget = Entry(f_SA, fg="white", bg="gray26")
    SAget.pack(side=RIGHT, pady=10)

    f_SCS = Frame(root, bg='grey22')
    f_SCS.pack(side=TOP, fill=X)

    label2 = Label(f_SCS, text="Server's command port: ", fg="white", bg="gray22")
    label2.pack(side=LEFT)

    SCSget = Entry(f_SCS, fg="white", bg="gray26")
    SCSget.pack(side=RIGHT, pady=10)

    f_SMS = Frame(root, bg='grey22')
    f_SMS.pack(side=TOP, fill=X)

    label3 = Label(f_SMS, text="Server's message port: ", fg="white", bg="gray22")
    label3.pack(side=LEFT)

    SMSget = Entry(f_SMS, fg="white", bg="gray26")
    SMSget.pack(side=RIGHT, pady=10)

    f_ok = Frame(root, bg='grey22')
    f_ok.pack(side=TOP, fill=X)

    ok = Button(f_ok, text="Ok",  width=5, height=1, bg='grey20', fg='white', command=lambda: RootOk(Bfget.get(), NMget.get(), SAget.get(), SCSget.get(), SMSget.get(), root))
    ok.pack()

    root.mainloop()


def RootOk(Buff, NAME, Ip, Cs, Ms, Form):
    global ServerINFO, UserName, BufferOfListen
    if NAME != 'SERVER' and not NAME.isspace() and Buff != '' and NAME != '' and Ip != '' and Cs != '' and Ms != '':
        try:
            Cs = int(Cs)
            Ms = int(Ms)
            Buff = int(Buff)
            ServerINFO = [Ip, int(Cs), int(Ms)]
            BufferOfListen = 2**Buff
            UserName = str(NAME)
            MessSock.sendto(bytes(('/' + NAME).encode('UTF-8')), (ServerINFO[0], ServerINFO[1]))
            Form.destroy()
        except ValueError:
            messagebox.showerror(title='ERROR_100', message='You entered the command port or message port are incorrectly!!!')
        except socket.gaierror:
            messagebox.showerror(title='ERROR_900', message='Server is offline!!!')
    elif NAME == 'SERVER':
        messagebox.showerror(title='ERROR_202', message='The name "SERVER" is reserved by the system!!!')
    elif Buff == '' or NAME == '' or Ip == '' or Cs == '' or Ms == '':
        messagebox.showerror(title='ERROR_0', message='Fill in all the fields!!!')
    elif NAME.isspace():
        messagebox.showerror(title='ERROR_201', message='Invalid name!!!')


def ListenServer():
    try:
        while True:
            Data = MessSock.recvfrom(BufferOfListen)[0]
            Data = Data.decode()
            if Data != 'exit':
                threading.Thread(target=DataProcessing, args=(Data,)).start()
            else: break
    except:
        messagebox.showerror(title='ERROR_400', message='The server went down!!!')



def DataProcessing(Data):
    if Data[:6] == 'SERVER':
        write(Chat, Data+'\n')
        Chat.yview(END)
    elif Data[:5] == 'Users':
        Us['text'] = Data.replace('-', '\n')
    else:
        Data = Data.split(' ')
        Data[0] = Data[0] + ' '
        Data[1] = Data[1].split('+')
        Data = Data[0] + Decrypt(dict(zip(Data[1][0].split('-'), Data[1][1].split('-'))))
        write(Chat, Data+'\n')
        Chat.yview(END)


def Refresh():
    try:
        MessSock.sendto(bytes('who is here'.encode('UTF-8')), (ServerINFO[0], ServerINFO[1]))
    except:
        messagebox.showerror(title='ERROR_501', message='Server is offline!!!')


Address = socket.gethostname()
MessSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MessSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
MessSock.bind((Address, YourSock))

GetServerAddr()

window = Tk()
window.geometry('1002x500')
window.update_idletasks()
Cs(window)
window.title("Duda's Chat v3.2")
window['bg'] = "gray22"
window.resizable(width=FALSE, height=FALSE)
window.protocol("WM_DELETE_WINDOW", Closing)

tabs = ttk.Notebook(window)
tabs.pack(fill='both', expand='yes')

t1 = Frame(window, bg='grey22')
tabs.add(t1, text='Chat | '+UserName)
t2 = Frame(window, bg='grey22')
tabs.add(t2, text='INFO')

f_top = Frame(t1, bg='grey22')
f_top.pack(side=TOP, fill=X)
f_bot = Frame(t1, bg='grey22')
f_bot.pack(side=BOTTOM, fill=X)

Chat = Text(f_top, bg='grey25', fg='white', width=122, height=23)
Chat.configure(state=DISABLED)
scrollC = Scrollbar(f_top, command=Chat.yview)
scrollC.pack(side=LEFT, fill=Y)
Chat.pack(side=LEFT)
Chat.config(yscrollcommand=scrollC.set)

MessageUs = Text(f_bot, bg='grey25', fg='white', width=108, height=6)
scrollM = Scrollbar(f_bot, command=MessageUs.yview)
scrollM.pack(side=LEFT, fill=Y)
MessageUs.pack(side=LEFT, anchor=SW)

SendBtn = Button(f_bot, text="Send",  width=14, height=6, bg='grey17', fg='white', command=Send)
SendBtn.pack(side=RIGHT, anchor=SE)
MessageUs.config(yscrollcommand=scrollM.set)

f_line1 = Frame(t2, bg='grey22')
f_line1.pack(side=TOP, fill=X)
f_line2 = Frame(t2, bg='grey22')
f_line2.pack(side=TOP, fill=X)
f_line3 = Frame(t2, bg='grey22')
f_line3.pack(side=TOP, fill=X)
f_line4 = Frame(t2, bg='grey22')
f_line4.pack(side=TOP, fill=X)

Ni = Label(f_line1, text="Your nickname: "+UserName, fg="white", bg="gray22")
Ni.pack(side=LEFT)

IP = Label(f_line2, text="Your address: "+str(MessSock).split('(')[1].strip('>').strip(')'), fg="white", bg="gray22")
IP.pack(side=LEFT)

RF = Button(f_line3, text="Refresh",  width=6, height=1, bg='grey17', fg='white', command=Refresh)
RF.pack(side=LEFT)

Us = Label(f_line4, text="Users on the server: \n", fg="white", bg="gray22")
Us.pack(side=LEFT)

threading.Thread(target=ListenServer).start()

window.mainloop()
