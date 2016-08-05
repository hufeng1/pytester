import os, shutil,stat

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
    # copy mode
    names = os.listdir(sourceDir)
    for name in names:
        srcname = os.path.join(sourceDir, name)
        for dest in destDir:
            dstname = os.path.join(dest, name)
            shutil.copystat(srcname, dstname)


def execN(destDir,users,name):
    i=0;
    for dest in destDir:
        os.chmod(os.path.join(dest,name),stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)

    for dest in destDir:
        cmd='cd '+dest+ ';'+'./'+name+' '+users[i]["UserID"]+' '+users[i]["Password"]+' '+users[i]["RunType"]+' '+users[i]["BizTypeID"]+' &'
        i=i+1
        os.system(cmd)

if __name__ == "__main__":
    copyN('hello',['dir0','dir1'])


