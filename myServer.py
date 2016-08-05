#! /usr/bin/env python
#coding=utf-8
"""使用SocketServer来实现简单的TCP服务器"""
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
               if file_data == 'exit':
                  break
               action, filename = file_data.split()
               if action == "put":
                  self.recvfile(filename)
               elif action == 'get':
                  self.sendfile(filename)
               elif action == "users":
                  self.users=json.loads(self.request.recv(1024))
                  print self.users
               else:
                 print("the action <%s> is error !" % action)

          else:
            self.request.sendall('invalid')
        else:
          self.request.sendall('请重新输入')
      except Exception, e:
        print("get error at:", e)


if __name__ == "__main__":
  host = '0.0.0.0'
  port = 6000
  s = SocketServer.ThreadingTCPServer((host, port), MyTcpServer)
  s.serve_forever()
