import networkModelPopulate as nmp
import numpy as np
import scipy.stats as stats
import sys 
import matplotlib.pyplot as plt
import pandas as pd

class groupWithSex( nmp.group):
    def __init__(self, groupName):
        self.groupName = groupName
        self.recruitmentGroup = False
        
    def addSex( self, inputSex):
        self.sex = inputSex
        
    def showSex( self ):
        return self.sex 
    
    def addRecruitmentGroup(self, rg):
        self.recruitmentGroup = rg

    def showRecruitmentGroup(self):
        return self.recruitmentGroup 


class createNetworkFromCSVwithSex( nmp.createNetworkFromCSV):

    def __init__(self, dfNetwork):
        self.network = nmp.populatedNetwork( dfNetwork['networkName'][0] )
        self.network.setYears( dfNetwork['nYears'][0] )
        self.network.setupNetworkMesh( dfNetwork['nPoints'][0],
                                       dfNetwork['minLength'][0],
                                       dfNetwork['maxLength'][0])

    def addGroupSexFromCSV( self, dfGroups, groupInIn):
        ## How do I override 
        self.addGroupsFromCSV( dfGroups, groupIn = groupInIn )

        # ## Loop through nodes and add in groups
        for n in self.network.nodes:
            ## Loop through each group in a node and in group sex
            for grp in n.groups:
                dfGroupUse = dfGroups.query(
                    str('network == ' + "'" +
                        self.network.networkName + "'" + 
                        ' & node == ' + "'" + 
                        n.showNodeName() + "'" +
                        ' & groupName == ' + "'" +
                        grp.showGroupName() + "'" ))
                grp.addSex( dfGroupUse['groupSex'].values[0] )
                grp.addRecruitmentGroup( dfGroupUse['recruitmentGroup'].values[0] )
                                
class populatedNodeWithSex( nmp.populatedNode):
    def __init__( self, nodeName):
        self.nodeName = nodeName
        self.groups = []
        self.pathsIn = []
        self.pathsOut = {}

    ## sum up recruitmentGroup groups

    ## update linear recruitment function to include recruitment groups 
