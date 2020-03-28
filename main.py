import numpy as np
import matplotlib.pyplot as plt
from data import *

print("Which mode do you want to use? (L)MTD or (H)TU?")
mode = input()

if mode == "L" or mode == "l":
    ### LMTD Estimation ###

    process = [[HEX1, 'hot'], [HEX2, 'cold'], [HEX3, 'hot'], [HEX4, 'hot']]
    for i in range(len(process)):
        LMTD, areaLMTD, Q, tubes = process[i][0].sizeLMTD(process[i][1])
        print("""
        HEX{}
        LMTD: {}
        LMTD Area Estimation: {} m^2
        Heat Duty: {} kW
        Number of tubes required: {}
        """.format((i+1), LMTD, areaLMTD, Q/1000, int(tubes)))

if mode == "H" or mode == "h":
    ### HTU Estimation ###