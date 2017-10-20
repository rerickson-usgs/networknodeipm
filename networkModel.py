

class path:
    ''' paths contains the names of the start and end nodes'''
    def __init__(self, pathName):
        self.pathName = pathName
        self.startNode = ''
        self.endNode = ''

    def showPathName(self):
        return self.pathName
        
    def addStartNode(self, startNode):
        self.startNode = startNode
        
    def showStartNode(self):
        return self.startNode

    def addEndNode(self, endNode):
        self.endNode = endNode
    
    def showEndNode(self):
        return self.endNode

class node:
    ''' nodes contain the names of paths that go in and out '''
    def __init__(self, nodeName):
        self.nodeName = nodeName
        self.pathsIn = []
        self.pathsOut = []

    def showNodeName(self):
        return self.nodeName
        
    def addPathsIn(self, pathsIn):
        [ self.pathsIn.append( pI ) for pI in pathsIn]

    def showPathsIn(self):
        return [pI for pI in self.pathsIn]
        
    def addPathsOut(self, pathsOut):
        [ self.pathsOut.append( pI ) for pI in pathsOut]

    def showPathsOut(self):
        return [pI for pI in self.pathsOut]

class network:
    ''' netoworks contain paths and nodes '''
    def __init__(self, networkName):
        self.networkName = networkName
        self.nodes = []
        self.paths = []

    def showNetworkName(self):
        return self.networkName            

    def showNetworkName(self):
        return self.networkName            

    def addNodes(self, nodesIn):
        [ self.nodes.append( n ) for n in nodesIn]

    def nNodes(self):
        return len(self.nodes)    
    
    def addPaths(self, pathsIn):
        [ self.paths.append( n ) for n in pathsIn]

    def nPaths(self):
        return len(self.paths)    

    def selfPopulatePaths(self):
        for nodeStart in self.nodes:
            for pathOut in nodeStart.showPathsOut():
                for nodeEnd in self.nodes:
                    for pathIn in nodeEnd.showPathsOut():
                        if pathIn is pathOut:
                            self.pathTemp = path( pathOut)
                            self.pathTemp.addStartNode( nodeStart)
                            self.pathTemp.addEndNode( nodeEnd)
                            self.addPaths( [self.pathTemp])
