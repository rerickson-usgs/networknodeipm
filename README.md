# Spatially explicit integral projection model


## Overview 

**Code purpose:** This file contains the source code and script to run a spatially explicit integral projection (population) model. The current model examples demonstrate the model for invasive carp, but could be applied to any species with spatially discrete populations. 

**Model documentation:** The model implemented with this code is described in a corresponding manuscript and TRACE documentation. 

**Code software design:** The model was programmed using Python. 
The most basic unit within the model are `groups`. 
`Groups` occupy `nodes` and `nodes` are connected with `paths` to form `networks`. 
A [Unified Modeling Language (UML) Diagram](https://en.wikipedia.org/wiki/Unified_Modeling_Language) is included in this [repository](./UMLdocuments/) to document the code architecture.

**Software testing:** The code has several formal unit tests (i.e., files that start with `unitTest*`). 
There are also several "non-unit" tests that check the plotting functions and allow for visual checks for the models results. 
These files also demonstrate how the model may be used. 


**Prerequisite knowledge:** This code is written for advanced Python users. 
The [Python homepage](https://www.python.org/doc/) contains links to tutorials and references for learning Python. 
A non-spatially explicit version of this model has been published as an [R package](https://my.usgs.gov/bitbucket/projects/UMESC/repos/carpipm/browse).
This R package would be more friendly for beginners.
A Python beginner could likely adapt existing models by changing the input CSV files, but adapting the model requires an understanding of multiple inheritance and class construction in Python.

## Description of files and folders 

0. `README.md`: this file
1. `LICENSE`: USGS required license, also see Diesclaimer at the end of this page
2. `UMLdocuments`: folder contains the UML Diagram for the model
  - `uml-inherited.tex`: The LaTeX file used to generate the diagram
  - `uml-inherited.pdf`: The PDF of the UML Diagram
3. `inputParameters`: A folder with input parameter tables used for model testing. 
4. `modelFiles`: A folder with the Python source files
   - `networkMode.py`: Contains files to build a basic network-node model
   - `networkModelPopulated.py`: Adds in groups and populations to a network model
   - `networkModelPopulateSex.py`: Adds in sex to groups model 
   - `networkModelPopulateSterileMale.py`: Allows a class with sterile males to be inherited as a Python class 
   - `networkModelPopulatedYYmale.py`: Allows a class with YY-males to be inheretited as a Python class
   - `netowrkModelTimePeriods.py`: Allows within year time periods to be included within the model
   - `nodeHarvest.py`: Allows nodes to include harvest
5. `testFiles`: Contains test files including unit tests and graphic tests that plot results (and are not formal unit tests)
   - Formal unit tests:
     - `unitTestNetwork.py`: Tests the `networkModel` module
     - `unitTestNetworkPopulate.py`: Tests the `networkModelPopulate` module
     - `unitTestNetworkPopulateSex.py`: Tests the `networkModelPopulateSex` module
     - `unitTestNetworkPopulateYY.py`: Tests the `networkModelPopulateYY` module
     - `unitTestNetworkPopulateSterile.py`: Tests the `networkModelPopulateSterileMale` module
     - `unitTestNetworkPopulateProjectionFunction.py`: Tests the `networkModelPopulateProjectionFunction` module
     - `unitTestNetworkTimePeriods.py`: Tests the `networkModelTimePeriods` module
     - `unitTestNetworkHarvest.py`: Tests the `nodeHarvest` module
   - Graphic test (non-unit tests, created to test plotting functions and visualize outputs from test cases)
	 - `populatedMovementNetworkNonUnitTest.py`: Tests movement within the `networkModelPopulate` module
	 - `populatedNetworkNonUnitTest.py`: Tests the `networkModelPopulate` module
	 - `populatedNetworkSexNonUnitTest.py`: Tests the `networkModelPopulateSex` module
	 - `populatedNetworkYYNonUnitTest.py`: Tests the `networkModelPopulateYYmale` module
	 - `populatedNetworkSterileNonUntTest.py`: Tests the `networkModelPopulateSterileMale` module
6. `simulationsPaper`: Contains simulations used for the manuscript
  -  `lake_Scn_*.py` contains the lake scenarios
  -  `river_Scenarios.py` runs the river scenarios
  -  `plotSimulationOutputs.R` plots the results using `R`
  -  `modelOutputs` contains csv files of the model's outputs
  -  `summaryFigures` contains the summary output figures
  -  `inputParameters` contains csv files that are used as the model's inputs

## Code contact

This code was developed by Richard A. Erickson (rerickson@usgs.gov).

## Disclaimer

This software is in the public domain because it contains materials that originally came from the U.S. Geological Survey, an agency of the United States Department of Interior. For more information, see the [official USGS copyright policy](https://www2.usgs.gov/visual-id/credit_usgs.html#copyright/).


This software has been approved for release by the U.S. Geological Survey (USGSW). Although the software has been subjected to rigorous review, the USGS reserves the right to update the software as needed pursuant to further analysis and review. No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. Furthermore, the software is released on condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from its authorized or unauthorized use."

This software is provided "AS IS".

