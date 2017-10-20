import networkModel as nm

class populatedPath( nm.path):

    def __init__(self, pathName):
        self.pathName = pathName
        self.groups = []
        self.startNode = ''
        self.endNode = ''

    def addGroups(self, groups):
        self.groups = groups

    def showGroups(self):
        return self.groups



class populatedNode( nm.node):
    def __init__(self, nodeName):
        self.nodeName = nodeName
        self.groups = []
        self.pathsIn = []
        self.pathsOut = []
        ## NEED TO ADD PATHS OUT PROBABIITY 
    def addGroups(self, groups):
        self.groups = groups

    def showGroups(self):
        return self.groups

