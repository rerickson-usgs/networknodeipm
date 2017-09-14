## This code tests the self building network codes.
import networkNodeIPM  as nnIPM
import pandas as pd

###################################################
## Test migration with a simple system with 2 time periods: "summer" and "winter"

## Read in parameter CSV files 
inputFolder = "./inputParameters/"
groupsFile = inputFolder + "twoNodeTwoSeasonTestGroups.csv"
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + "twoNodeTwoSeasonTestNodes.csv"
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + "twoNodeTwoSeasonTestNetwork.csv"
dfNetwork = pd.read_csv(networkFile)

## create network from CSV

twoNodeSystemTwoSeasons = nnIPM.initalizeModelFromCSVs( dfNetwork = dfNetwork, dfNode = dfNode, dfGroups = dfGroups)


# print twoNodeSystemTwoSeasons.nodes[0].showTimePeriod()

twoNodeSystemTwoSeasons.describeNetwork()

twoNodeSystemTwoSeasons.plotAllNode( showGroups = True, saveData = "twoNodeTowSeasonGroupOut.csv")


print "done with two node two season test"



# test = range(0, 10)

# for t in test:
#     if t <2:
#         print t + 1
