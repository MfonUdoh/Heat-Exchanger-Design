import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from data import *

print("""Which mode do you want to use?
(L)MTD area estimation
(H)TU area estimation
(ST) Sensitivity analysis on temperature
(SM) Sensitivity analysis on mass flowrate
(SL) Sensitivity analysis on length""")
mode = input().upper()

if mode == "L":
    ### LMTD Estimation ###

    process = [[HEX1, 'hot'], [HEX2, 'cold'], [HEX3, 'hot'], [HEX4, 'hot']]
    for i in range(len(process)):
        LMTD, areaLMTD, Q = process[i][0].sizeLMTD(process[i][1])
        tubes = process[i][0].tubes_required(areaLMTD)
        print("""
        HEX{}
        LMTD: {}
        LMTD Area Estimation: {} m^2
        Heat Duty: {} kW
        Number of tubes required: {}
        """.format((i+1), LMTD, areaLMTD, Q/1000, tubes))

if mode == "H":
    ### HTU Estimation ###

    n = [x+1 if x == 0 else x for x in range(0, 51, 5)]
    for slices in n:
        A = HEX1.sizeHTU('hot', slices)
        tubes = HEX1.tubes_required(A)
        print("""
        Using {} slices
        Area: {} m^2
        Tubes: {} """.format(slices, A, tubes))

if mode == "SM":
    ### HTU Sensitivity Analysis on mass flowrate###

    m = np.arange(0.05, 3, 0.05)
    U = np.arange(10, 150, 5)
    T = HEX1.hotFluid.To
    n = 50

    U, m = np.meshgrid(U, m)
    Z = HEX1.sensitivity_area('hot', n, U, T, m)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(m, U, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
    ax.set_xlabel('Air Mass Flowrate [kg/s]')
    ax.set_ylabel('Overall Heat Transfer Coefficient [W/m^2K]')
    ax.set_zlabel('Heat Exchanger Area [m^2]')
    ax.set_title('Sensitivity Analysis')
    plt.show()

if mode == "ST":
    ### HTU Sensitivity Analysis on outlet temperature ###

    T = np.arange(289, 297, 0.05)
    U = np.arange(10, 155, 5)
    m = HEX1.hotFluid.m
    n = 50

    U, T = np.meshgrid(U, T)
    Z = HEX1.sensitivity_area('hot', n, U, T, m)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(T, U, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
    ax.set_xlabel('Air Outlet Temperature [K]')
    ax.set_ylabel('Overall Heat Transfer Coefficient [W/m^2K]')
    ax.set_zlabel('Heat Exchanger Area [m^2]')
    ax.set_title('Sensitivity Analysis')
    plt.show()

if mode == "SL":
    ### HTU Sensitivity Analysis on length ###

    L = np.arange(0.5, 1.55, 0.05)
    Di = np.arange(0.01, 0.055, 0.005)
    A = 10
    n = 50

    L, Di = np.meshgrid(L, Di)
    Z = HEX1.sensitivity_length('hot', n, A, L, Di)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(L, Di, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
    ax.set_xlabel('Length [m]')
    ax.set_ylabel('Diameter [m]')
    ax.set_zlabel('Tubes Required [-]')
    ax.set_title('Sensitivity Analysis')
    plt.show()