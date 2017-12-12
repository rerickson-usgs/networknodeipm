import networkModel as nm
import networkModelPopulate as nmp
import numpy as np
import scipy.stats as stats
import sys 
import matplotlib.pyplot as plt
import pandas as pd


''' 
Pythonic reminder: Remember how inheritance works in Python. Right to left, so inhert these functions on the right.
'''

class nodeTimePeriod:

    def addTimePeriod(self, tp):
        self.timePeriod = tp

    def showTimePeriod(self):
        return self.timePeriod    
    
class networkWithTimePeriod:
    '''
    This netowrk class adds time periods and a run simulation funciton with timeperiods 
    to other netwowork classes. 
    '''

    def __init__(self, networkName = "test network"):
        self.timePeriods = []
        self.networkName = networkName
        self.nodes = []
        self.paths = []

        
    def addTimePeriods(self, timePeriodsIn):
        [ self.timePeriods.append( tp) for tp in timePeriodsIn ]
        
    def showTimePeriods(self):
        return self.timePeriods

    def moveGroups( self, startYear, endYear, timePeriod):
        #####################
        ## Run movement in two steps
        ## First, copy individuals onto a path
        pathUse = [p for p in self.paths if p.timePeriod == timePeriod]
        
        for p in pathUse:
            for nodeStart in self.nodes:
                if nodeStart.showNodeName() is p.showStartNode():
                    startTime = startYear 
                    if timePeriod == self.showTimePeriods()[0]:
                        startTime = startYear - 1 
                    p.groups = [ nodeStart.pathsOut[ p.showPathName() ] *
                                 grp.showPopDistYear( startTime) for grp in nodeStart.groups ]
                    
        ## Second, unload paths
        for p in pathUse:
            for nodeEnd in self.nodes:
                if nodeEnd.showNodeName() ==  p.showEndNode():
                    if len(nodeEnd.groups) != len(p.groups):
                        sys.exit("There are not the same number of groups in the node as there is in the pathway")
                    else:
                        for index in xrange( len(nodeEnd.showGroups() )):
                            nodeEnd.groups[index].popDist[ endYear, :] += p.groups[index] 
                                
    def runSimulation(self):
        ''' 
        This function runs the network simulation and assumes 
        movement occures before spawning.
        '''
        for yearIndex in range(1, self.nYears):
            for tp in self.showTimePeriods():
                ## Step 1, move groups 
                self.moveGroups( yearIndex, yearIndex, tp)
                ## Step 2, update popualtions within nodes
                for n in self.nodes:
                    if n.showTimePeriod() == tp:
                        ## Step 2a: calculate biomass in each node and density effect
                        n.calculateNodeBiomass( omega = self.omega, year = yearIndex )
                        ## Step 2b: project groups through time
                        n.projectGroups(yearIndex, self.omega,
                                        self.hWidth, nodeBiomass = n.showNodeBiomass(),
                                        nextYear = yearIndex)

class createNetworkFromCSVwithTimeBase:
    '''contains functions to populate a network from csv files'''

    def addTimePeriodToPaths(self, pathIn):
        self.network.selfPopulatePaths( path = pathIn)
        for pth in self.network.paths:
            for nd in self.network.nodes:
                if pth.showEndNode() == nd.showNodeName():
                    pth.timePeriod = nd.timePeriod

                    
    def addTimePeriodToNodes(self, dfNode):

        dfNodeUse = dfNode.query(str('network == ' + "'" +
                                     self.network.showNetworkName() + "'"))
     
        ## Loop through each node in the network and generate it
        for nodeRow in dfNodeUse.iterrows():
            for n in self.network.nodes:
                if n.showNodeName() == nodeRow[1]['node']:
                    n.addTimePeriod( nodeRow[1]['timePeriod'])    

    def addNetworkTimePeriods( self, dfNetwork):
        self.network.addTimePeriods( dfNetwork['timePeriods'][0].split(",") )
        
class createNetworkFromCSVwithTime( createNetworkFromCSVwithTimeBase, nmp.createNetworkFromCSV):
    '''contains functions to populate a network from csv files'''

    def __init__(self, dfNetwork, networkIn):
        self.network = networkIn( dfNetwork['networkName'][0] )
        self.network.setYears( dfNetwork['nYears'][0] )
        self.network.setupNetworkMesh( dfNetwork['nPoints'][0],
                                       dfNetwork['minLength'][0],
                                       dfNetwork['maxLength'][0])
        self.network.addTimePeriods( dfNetwork['timePeriods'][0].split(",") )
