#-*-coding:utf-8-*-

import json

f=file("configure.json")

s=json.load(f)

print s

print s.keys()

for user in s["usersInfo"]:
    print user["DestUserID"]

print len(s["usersInfo"])

userNum=len(s["usersInfo"])
dirtList=[]
for i in range(len(s["usersInfo"])):
    dirtList.append('dir'+str(i))

print dirtList
f.close()