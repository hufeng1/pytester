import socket
import sys, os
import time
import json


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


def recvlogs():
    filenum=s.recv(1024)
    s.sendall('get num')
    print ("file number is :%s"%filenum)
    for i in range (int(filenum)):
        filename=s.recv(1024)

        s.sendall("get name")
        filename=filename.replace('/','_')

        print ("receive log file :%s"%filename)

        print "server ready, now client recv file~~"

        f = open(filename, 'wb')
        while True:
            data = s.recv(4096)
            if data == 'EOF':
                print "recv file success!"
                break
            f.write(data)
        f.close()
        s.sendall('get file')


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
# to do : dectect file list automatically
#fileList=['message.xml','TestUnit.xml','vcssys.xml','vcsidsync.xml','myTester.py','myDir.py','killNProcess.py','vcstest']
#fileList=['message.xml']
fileList=os.listdir('.')
for filename in fileList:
    if filename.endswith(r'.txt'):
        fileList.remove(filename)

print fileList
#ip = '127.0.0.1'
#ports = [6000]
address=[('127.0.0.1',6000)]
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
#    for port in ports:
    for (ip,port) in address:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.sendall('Hi, server')
        res = s.recv(1024)
        print(res)

        while True:
            select = raw_input("Server: Do you want put/get the file from the server:%d?(y/n):"%port)
            if select == 'y':
                client_command = raw_input("method:put/get filename:")
                if not client_command:
                    continue
                elif client_command == 'exit':
                    s.sendall('exit')
                    sys.exit('exit')
                action  = client_command
                if action == 'put':
                    for file in fileList:
                        if os.path.isfile(file):
                            if confirm(s, action+' '+file):
                                sendfile(file)
                        else:
                            print("the file <%s> is not exist" % file)
                elif action == 'get':
                    filename=raw_input("Please input the file name that you want to get:")
                    if confirm(s, action+' '+filename):
                        recvfile(filename)
                # send user info configure file
                elif action == 'configure':
                    if confirm(s,'configure file'):
                        f = open("configure.json")
                        j = json.load(f)
                        print json.dumps(j)
                        s.sendall(json.dumps(j))
                # let tester run
                elif action == "run":
                    s.sendall('run file')

                else:
                    print("command error!")
            else:
                s.sendall('exit')
                s.close()
                break


    while True:
        client_command = raw_input("method: kill (process)/ get (log)/ exit:")
        if not client_command:
            continue
        # run tester
        elif client_command == "run":
            for (ip, port) in address:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.sendall('Hi, server')
                res = s.recv(1024)
                print(res)
                s.sendall("run file")
                s.close()
        # collect log
        elif client_command == "log":
            for (ip, port) in address:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.sendall('Hi, server')
                res = s.recv(1024)
                print(res)
                s.sendall("log log")
                recvlogs()
                s.close()
        # kill tester process
        elif client_command == "kill":
            for (ip, port) in address:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.sendall('Hi, server')
                res = s.recv(1024)
                print(res)
                s.sendall("kill vcstest")
                s.close()
        # delete tester file
        elif client_command == "delete":
            for (ip, port) in address:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.sendall('Hi, server')
                res = s.recv(1024)
                print(res)
                s.sendall("delete vcstest")
                s.close()
        elif client_command == "exit":
            break

    print ("Bye!")

except socket.error, e:
    print "get error as", e
finally:
    s.close()