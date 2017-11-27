import pandas as pd
import numpy as np
import sys 

class nodeHarvest:

    def setHarvest( self, harvestLevel):
        self.harvest = harvestLevel

    def showNodeHarvest(self):
        return self.harvest

    def showNodeHarvestYear(self, year):
        if len(self.harvest.shape) == 1:
            return self.harvest[ year]
        elif len(self.harvest.shape) == 2:
            return self.harvest[ year ,:]
        else:
           sys.exit("The harvest matrix has more than 2 dimensions")
        
    def nodeHarvest( self, year):
        for grp in self.groups:
            grp.updatePopDistYear( year,
                                   grp.showPopDistYear( year) *
                                   ( 1 - self.showNodeHarvestYear( year) )
            ) 

class addNodeHarvestCSV:

    def addHarvestIntoNodes( self, dfHarvest):
        for nd in self.network.nodes:
            dfHarvestUse = dfHarvest.query( str('node == ' + "'" + nd.showNodeName() + "'"))
            ## If entry is float, simply use a vector to store harvest
            if dfHarvestUse['harvest'].dtype.kind == 'f':
                harvestIn = ( np.ones( self.network.nYears) *
                              dfHarvestUse['harvest'].values[0] )
                nd.setHarvest( harvestIn)
            else:
                harvestIn = np.zeros( self.network.nYears)
                harvestLevel, startYear, endYear =  dfHarvestUse['harvest'].values[0].split(";")
                harvestIn[ int(startYear): int(endYear)] = float(harvestLevel)
                nd.setHarvest( harvestIn)
