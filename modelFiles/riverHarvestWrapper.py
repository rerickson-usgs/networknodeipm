import sys
sys.path.append("../modelFiles")
import networkModelPopulate as nmp
import nodeHarvest as nh
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''
Wrapper file for river scnearios with harvest and barriers
'''

def riverWrapper(scnName  = "river",
                 groupNumber = "Scn_0",
                 nodeNumber= "Scn_0",
                 networkNumber = "Scn_0",
                 harvestScn = "noH",
                 inputFolder = "./inputParameters/",
                 outputFolder = "./modelOutputs/"):

    ## read in parameter files 
    groupsFile = inputFolder + scnName + "_groups_" + groupNumber +'.csv'
    dfGroups = pd.read_csv(groupsFile)
    
    nodeFile = inputFolder + scnName + '_Nodes_' + nodeNumber + '.csv'
    dfNode = pd.read_csv(nodeFile)
    
    networkFile = inputFolder + scnName +'_Network_' + networkNumber +'.csv'
    dfNetwork = pd.read_csv(networkFile)
    
    harvestFile = inputFolder + scnName + "_Harvest_" + harvestScn + ".csv"
    dfHarvest = pd.read_csv(harvestFile)
    
    ## define custom classes
    class networkUse( nmp.populatedNetwork):
        pass
    
    class nodeUse(
            nh.nodeHarvest,
            nmp.populatedNode):
        
        def projectGroups(self, year, omega, hWidth, nodeBiomass,
                          nextYear = None):
            '''  
            projects population using midpoint rule.
            First dotproduct is growth/maturation.
            Second dotproduct is recruitment.
            '''
            reproducingPopulation  = 0.0
            
            groupsMale   = [grp.showSex() == "male"  for grp in self.groups]
            groupsFemale = [grp.showSex() == "female"  for grp in self.groups]
            groupsPop    = np.array([grp.showPopYear(year)  for grp in self.groups])
            
            maleContribution   = np.array([grp.showImpactOnMaleRatio()    for grp in self.groups])[ groupsMale]
            femaleContribution = np.array([grp.showImpactOnFemaleRatio()  for grp in self.groups])[ groupsFemale]
            
            malePop   = groupsPop[groupsMale]
            femalePop = groupsPop[groupsFemale]

            maleRatio   = (maleContribution   * malePop / malePop.sum()).sum()
            femaleRatio = (femaleContribution * femalePop / femalePop.sum()).sum()
            
            for grp in self.groups:
                ## First, sum up reruitment groups
                if grp.showRecruitmentGroup():
                    reproducingPopulation += grp.showPopDistYear( year)
                    if grp.showSex() == "male":
                        if grp.showRecruitmentProportion() > 0.0:
                            grp.addRecruitmentProportionMod(
                                maleRatio
                            )                    
                            
                    if grp.showSex() == "female":
                        if grp.showRecruitmentProportion() > 0.0:
                            grp.addRecruitmentProportionMod(
                                femaleRatio
                            )

            for grp in self.groups:
                popAdd = ( np.dot( hWidth * grp.growth( omega, omega), 
                                   grp.showPopDistYear( year) *
                                   grp.survival( omega) ) +
                           np.dot(hWidth * grp.recruitment( omega, omega),
                                  reproducingPopulation *  grp.density(nodeBiomass) *
                                  grp.showRecruitmentProportionMod() )
                )
                
                if grp.showStocking():
                    grp.updatePopDistYear( year + 1, popAdd + grp.showStockingPopYear(year))
                else:
                    grp.updatePopDistYear( year + 1, popAdd)
            
    class createNetworkUse(
            nh.addNodeHarvestCSV,
            nmp.createNetworkFromCSV):
        pass

    ## Create network and add in network features
    createNetwork = createNetworkUse(dfNetwork, networkUse)
    createNetwork.addNodesFromCSV( dfNode, nodeUse)
    createNetwork.addGroupsFromCSV( dfGroups)
    createNetwork.addHarvestIntoNodes( dfHarvest)

    ## Extract network, run sims, and look at results
    network = createNetwork.showNetwork()
    network.selfPopulatePaths()
    network.runSimulation()

    network.calculateNetworkPop()
    network.saveGroupData(saveGroupFile = outputFolder + "groups_" +
                          scnName + "_" + nodeNumber  + "_" + harvestScn +  ".csv")


