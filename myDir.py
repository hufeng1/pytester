import os, shutil

def makeNDir(n):
    dirList=[]
    for i in range(n):
        dirName='dir'+str(i)
        dirList.append(dirName)
        if os.path.exists(dirName):
            print "File exits !"
        else:
            os.mkdir(dirName)

    return dirList


def rmNdir(n):
    os.system('rm -rf dir*')

def copyN(sourceDir,destDir):

    for dest in destDir:
        if os.path.exists(dest):
            cmd='rm -rf '+dest
            os.system(cmd)
        shutil.copytree(sourceDir,dest,True)


def execN(destDir,users,name):
    i=0;
    for dest in destDir:
        cmd='cd '+dest+ ';'+'./'+name+' '+users[i]["UserID"]+' '+users[i]["Password"]+' '+users[i]["RunType"]+' '+users[i]["BizTypeID"]+' &'
        i=i+1
        os.system(cmd)

if __name__ == "__main__":
    copyN('hello',['dir0','dir1'])


