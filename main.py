import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
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
    # n = [x+1 if x == 0for x in range(0, 51, 5)]
    m = np.arange(0.01, 3, 0.02)
    U = np.arange(10, 100, 10)
    n = 50

    y = np.array(U)
    x = np.array(m)
    X, Y = np.meshgrid(x, y)
    Z = HEX1.sizeHTU('hot', n, X, Y)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
    ax.set_xlabel('Air Mass Flowrate kg/s')
    ax.set_ylabel('Overall Heat Transfer Coefficient W/m^2K')
    ax.set_zlabel('Heat Exchanger Area m^2')
    ax.set_title('Sensitivity Analysis')
    plt.show()