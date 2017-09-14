## This code tests the self building network codes.
import numpy as np
import scipy.stats as stats
import networkNodeIPM  as nnIPM
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

##############################
## Test only one group
inputFolder = "./inputParameters/"
groupsFile = inputFolder + "oneGroupTestGroups.csv"
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + "oneGroupTestNodes.csv"
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + "oneGroupTestNetwork.csv"
dfNetwork = pd.read_csv(networkFile)


## create network from CSV
oneGroupTest = nnIPM.initalizeModelFromCSVs( dfNetwork = dfNetwork, dfNode = dfNode, dfGroups = dfGroups)

print oneGroupTest.nNodes()
oneGroupTest.runNetworkSimulation()
oneGroupTest.describePaths()

[node.calculateNodePopulaiton() for node in oneGroupTest.nodes]
[node.plotNodeGroups(nYears = oneGroupTest.nYears) for node in oneGroupTest.nodes]

print "done with one group test"

##############################
## Test two nodes with two groups 

## Read in parameter CSV files 

groupsFile = inputFolder + "groupsParametersBuild.csv"
dfGroups = pd.read_csv(groupsFile)


nodeFile = inputFolder + "nodeParametersBuild.csv"
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + "networkParametersBuild.csv"
dfNetwork = pd.read_csv(networkFile)


## create network from CSV

twoNodeSystem = nnIPM.initalizeModelFromCSVs( dfNetwork = dfNetwork, dfNode = dfNode, dfGroups = dfGroups)

print twoNodeSystem.nNodes()
twoNodeSystem.runNetworkSimulation()
twoNodeSystem.describePaths()

[node.calculateNodePopulaiton() for node in twoNodeSystem.nodes]
[node.plotNodeGroups(nYears = twoNodeSystem.nYears) for node in twoNodeSystem.nodes]


print "Done with two group test"


######################################
## include stocking of YY-males
## Test one nodes with three groups 

## Read in parameter CSV files 
inputFolder = "./inputParameters/"
groupsFileOneYY = inputFolder + "oneNodeYYmaleTestGroups.csv"
dfGroupsOneYY = pd.read_csv(groupsFileOneYY)

nodeFileOneYY = inputFolder + "oneNodeYYmaleTestNodes.csv"
dfNodeOneYY = pd.read_csv(nodeFileOneYY)

networkFileOneYY = inputFolder + "oneNodeYYmaleTestNetwork.csv"
dfNetworkOneYY = pd.read_csv(networkFileOneYY)

oneNodeSystemYYmales = nnIPM.initalizeModelFromCSVs( dfNetwork = dfNetworkOneYY, dfNode = dfNodeOneYY, dfGroups = dfGroupsOneYY)

oneNodeSystemYYmales.runNetworkSimulation()

[node.calculateNodePopulaiton() for node in oneNodeSystemYYmales.nodes]
[node.plotNodeGroups(nYears = oneNodeSystemYYmales.nYears) for node in oneNodeSystemYYmales.nodes]

######################################
## include stocking of YY-males
## Test two nodes with three groups 

## Read in parameter CSV files 
inputFolder = "./inputParameters/"
groupsFile = inputFolder + "twoNodeYYmaleTestGroups.csv"
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + "twoNodeYYmaleTestNodes.csv"
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + "twoNodeYYmaleTestNetwork.csv"
dfNetwork = pd.read_csv(networkFile)

## create network from CSV

twoNodeSystemYYmales = nnIPM.initalizeModelFromCSVs( dfNetwork = dfNetwork, dfNode = dfNode, dfGroups = dfGroups)

twoNodeSystemYYmales.plotAllNode()

print "inbetween two plots"

twoNodeSystemYYmales.plotAllNode( showGroups = True)

print "done with YY-male test"



### include stocking of sterile males
### Test two nodes with three groups 

## Read in parameter CSV files 
inputFolder = "./inputParameters/"
groupsFile = inputFolder + "twoNodeSterileMaleTestGroups.csv"
dfGroups = pd.read_csv(groupsFile)

nodeFile = inputFolder + "twoNodeSterileMaleTestNodes.csv"
dfNode = pd.read_csv(nodeFile)

networkFile = inputFolder + "twoNodeSterileMaleTestNetwork.csv"
dfNetwork = pd.read_csv(networkFile)

## create network from CSV

twoNodeSystemSterilemales = nnIPM.initalizeModelFromCSVs( dfNetwork = dfNetwork, dfNode = dfNode, dfGroups = dfGroups)

twoNodeSystemSterilemales.plotAllNode( showGroups = True)

print "done with Sterile-male test"



