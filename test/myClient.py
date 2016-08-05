# coding:utf-8

import socket
import sys, os
import time


def recvfile(filename):
    print "server ready, now client recv file~~"
    name = os.path.basename(filename)
    f = open(name, 'wb')
    while True:
        data = s.recv(4096)
        if data == 'EOF':
            print "recv file success!"
            break
        f.write(data)
    f.close()


def sendfile(filename):
    print "server ready, now client send file~~"
    f = open(filename, 'rb')
    while True:
        data = f.read(4096)
        if not data:
            break
        s.sendall(data)
    f.close()
    time.sleep(1)
    s.sendall('EOF')
    print "send file success!"


def confirm(s, client_command):
    s.send(client_command)
    confirm_data = s.recv(1024)
    print(confirm_data)
    if confirm_data == 'ready':
        return True
    else:
        return False


#def auth_user():
#    name = raw_input('Server: input our name:')
#    s.sendall('name:' + name.strip())
#    response = s.recv(1024)
#    if response == 'valid':
#        res = False
#        while not res:
#            res = auth_pass()
#        return True
#    else:
#        return False


def auth_pass():
    pwd = raw_input('Server: input our password:')
    s.sendall('pwd:' + pwd.strip())
    response = s.recv(1024)
    if response == 'valid':
        return True
    else:
        return False


############################main##############################
ip = '127.0.0.1'
port = 6000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ip, port))
    s.sendall('Hi, server')
    res = s.recv(1024)
    print(res)
    while True:
        #result = auth_user()
        #if result:
            while True:
                select = raw_input("Server: Do you want put/get the file from the server?(y/n):")
                if select == 'y':
                    client_command = raw_input("method:put/get filename:")
                    if not client_command:
                        continue
                    elif client_command == 'exit':
                        s.sendall('exit')
                        sys.exit('退出')
                    action, filename = client_command.split()
                    if action == 'put':
                        if os.path.isfile(filename):
                            if confirm(s, client_command):
                                sendfile(filename)
                        else:
                            print("the file <%s> is not exist" % filename)
                    elif action == 'get':
                        if confirm(s, client_command):
                            recvfile(filename)
                    else:
                        print("command error!")
                else:
                    s.sendall('exit')
                    sys.exit('传输完成，正常退出')
except socket.error, e:
    print "get error as", e
finally:
    s.close()