## Spatially explicit integral projection model

This file contains the source code and script to run a spatially explicit integral projection (population)  model.

The code has several "test" script files (sort of like a Unit Test, but only qualitative). Reading through these scripts allows for one to see how to use the model with different levels of complexity. 

The basic building blocks of the model are "groups". A group is a collection of fish based upon their sex that share a node. If sex-structure is ignored, there is only one group per node. In addition to females and males, the model currently support YY-males that bias the sex ratio and sterile males that decrease the offspring produced. In theory, the model allows for other groups, but their impact would need to be programmed into the model. 

The guts of the package are hosed in the `networkNodeIPM.py` file, which is loaded by the other scripts. The following test scripts increase in order of complexity:

0. `groupDevelopmentCode.py` loads up a single group via code and runs it through time using a for loop.
1. `nodeDevelopmentCode.py` loads up 3 single group into a node via code and runs it through time using a for loop. This code also includes YY-males.
2. `networkDevelopmentCode.py` loads ups 2 node into a network via code and runs them using the network's functions. 
3. `selfPopulatingCode.py` loads ups simple networks via CSV input files and uses the networks to run them. It also includes YY-male test cases and demonstrates the network's node plotting option.
4. `timePeriodModel.py` loads up a simple 2 node mode that includes forced migration. 

## Disclaimer

This software is in the public domain because it contains materials that originally came from the U.S. Geological Survey, an agency of the United States Department of Interior. For more information, see the [official USGS copyright policy](https://www2.usgs.gov/visual-id/credit_usgs.html#copyright/).


This software has been approved for release by the U.S. Geological Survey (USGSW). Although the software has been subjected to rigorous review, the USGS reserves the right to update the software as needed pursuant to further analysis and review. No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. Furthermore, the software is released on condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from its authorized or unauthorized use."

This software is provided "AS IS".

