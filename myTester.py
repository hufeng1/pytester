import myDir,myXML,json

if __name__ == "__main__":

    # parse configure
    f=file("configure.json")
    users=json.load(f)

    # generate file directorys
    dirtList=[]
    for i in range (len(users["usersInfo"])):
        dirtList.append('dir'+str(i))

    #dirList=['dir0', 'dir1','dir2','dir3']
    myDir.copyN('hello', dirtList)

    # get usersList
    usersList=[]
    for user in users["usersInfo"]:
        print user
        usersList.append(user)

    print usersList

    tree = myXML.read_xml("./TestUnit.xml")

    i=0
    for user in usersList:
        outputFile='./'+dirtList[i]+'/TestUnit.xml'
        i=i+1

        nodes = myXML.find_nodes(tree, "DestUserID/item")

        myXML.change_node_properties(nodes, {"UserID": user["DestUserID"]})

        myXML.write_xml(tree, outputFile)

    myDir.execN(dirtList, usersList,"vcstest")