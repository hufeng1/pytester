#! /usr/bin/env python

""""
from SocketServer import (TCPServer,StreamRequestHandler as SRH)
from time import ctime

class MyRequestHandler(SRH):
  def handle(self):
    print "connected from ",self.client_address
    self.wfile.write("[%s] %s" %(ctime(),self.rfile.readline()))
tcpSer=TCPServer(("",10001),MyRequestHandler)
print "waiting for connection"
tcpSer.serve_forever()"""

import SocketServer
import time
import os
import json
import shutil
import socket


def kill_process_by_name(name):

    cmd = "ps -e | grep %s" % name
    f = os.popen(cmd)
    txt = f.readlines()
    if len(txt) == 0:
        print "no process \"%s\"!!" % name
        return
    else:
        for line in txt:
            colum = line.split()
            pid = colum[0]
            cmd = "kill -9 %d" % int(pid)
            rc = os.system(cmd)
            if rc == 0:
                print "exec \"%s\" success!!" % cmd
            else:
                print "exec \"%s\" failed!!" % cmd
    return


class MyTcpServer(SocketServer.BaseRequestHandler):

  def recvfile(self, filename):
    name = os.path.basename(filename)
    print("starting recv file <%s> ..." % filename)
    f = open(name, 'wb')
    self.request.send('ready')
    while True:
      data = self.request.recv(4096)
      if data == 'EOF':
        print "recv file success!"
        break
      f.write(data)
    f.close()

  def sendfile(self, filename):
    if os.path.isfile(filename):
      print("starting send file <%s> ..." % filename)
      self.request.send('ready')
      time.sleep(1)
      f = open(filename, 'rb')
      while True:
        data = f.read(4096)
        if not data:
          break
        self.request.send(data)
      f.close()
      time.sleep(1)
      self.request.send('EOF')
      print("send file success!")
    else:
      print("the file <%s> is not exist" % filename)
      self.request.send("the file <%s> is not exist" % filename)

  def sendlogs(self):
      '''send all *.txt files under this directory
       1. send how many log file is needed to send
       2. send log files by the request of the client
      '''
      fileList=[]
      dirList=os.listdir('.')
      for dir in dirList:
          if os.path.isdir(dir):
              tempfileList=os.listdir(os.path.join(dir))
              for tempfile in tempfileList:
                  if tempfile.endswith('.txt'):
                      fileList.append(os.path.join(dir,tempfile))

      self.request.sendall(str(len(fileList)))
      feedback = self.request.recv(1024)
      print feedback
      # send file by request
      for file in fileList:
          self.request.sendall(file)

          feedback=self.request.recv(1024)
          print feedback
          f = open(file, 'rb')
          while True:
              data = f.read(4096)
              if not data:
                  break
              self.request.send(data)
          f.close()
          time.sleep(1)
          self.request.send('EOF')
          feedback=self.request.recv(1024)
          print feedback
          print("send file success!")

  def handle(self):
    print("get connection from :", self.client_address)
    while True:
      try:
        data = self.request.recv(1024)
        print(data)
        if not data:
          print("break the connection!")
          break
        elif data == 'Hi, server':
          self.request.sendall('hi, client')

          while True:
               file_data = self.request.recv(1024)
               print("receive message %s" % file_data)
               if file_data == 'exit':
                  break
               action, filename = file_data.split()
               if action == "put":
                  self.recvfile(filename)
               elif action == 'get':
                  self.sendfile(filename)
               # send user information
               elif action == "configure":
                    self.request.sendall('ready')
                    self.users=json.loads(self.request.recv(1024))
                    print self.users
                    f=open("configure.json",'w')
                    json.dump(self.users,f)
                    f.close()
               # kill process of test program
               elif action == "kill":
                    kill_process_by_name("vcstest")
               elif action == "run":
                   # to do : add feedback
                   os.system("python myTester.py")
               elif action == "log":
                   self.sendlogs()
               elif action == "delete":
                   dirList = os.listdir('.')
                   for dir in dirList:
                       if os.path.isdir(dir):
                           shutil.rmtree(dir)
               else:
                 print("the action <%s> is error !" % action)

          else:
            self.request.sendall('invalid')
        else:
          self.request.sendall('please input again !')
      except Exception, e:
        print("get error at:", e)


if __name__ == "__main__":
  host = '0.0.0.0'
  port = 6000

  myname = socket.getfqdn(socket.gethostname())
  myaddr = socket.gethostbyname(myname)

  s = SocketServer.ThreadingTCPServer((host, port), MyTcpServer)
  s.serve_forever()
