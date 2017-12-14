import sys
sys.path.append("../modelFiles")
# import networkModelPopulate as nmp
# import nodeHarvest as nh
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
import riverHarvestWrapper as rhw

'''
Run river scnearios with harvest and barriersA
'''
harvestScn = ["noH", "H1", "H2", "H3", "H4", "H5", "H6"]
scnNumber = ["Scn_0", "Scn_1", "Scn_2"]

for hs in harvestScn:
    for sn in scnNumber:
        print("running: " + hs + "  " + sn)
        rhw.riverWrapper(scnName  = "river",
                         harvestScn = hs,
                         nodeNumber = sn,
                         inputFolder = "./inputParameters/",
                         outputFolder = "./modelOutputs/")

print("Done")



