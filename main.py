import numpy as np
import matplotlib.pyplot as plt
from data import *

print("Which mode do you want to use? (L)MTD or (H)TU?")
mode = 'h' # input()

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
        """.format((i+1), LMTD, areaLMTD, Q/1000, tubes))

if mode == "H" or mode == "h":
    ### HTU Estimation ###
    n = [x for x in range(0, 51, 5)]
    for i in n:
        A, tubes = HEX1.sizeHTU('hot', i)
        print("""
        Using {} slices
        HEX area: {} m^2
        Tubes required: {}""".format(i, A, tubes))