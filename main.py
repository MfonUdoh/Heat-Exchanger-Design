import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from data import *

print("""Which mode do you want to use?
(L)MTD area estimation
(H)TU area estimation
(O)ptimise
(ST) Sensitivity analysis on temperature
(SM) Sensitivity analysis on mass flowrate
(SL) Sensitivity analysis on length
(HP) Heat Plot
(HM) Heat Map""")
mode = input().upper()

if mode == "L":
    ### LMTD Estimation ###

    process = [[HEX1, 'hot'], [HEX2, 'hot']]
    for i in range(len(process)):
        LMTD, areaLMTD, Q = process[i][0].sizeLMTD(process[i][1])
        x = process[i][0].number_required(areaLMTD)
        print("""
        {}
        LMTD: {}
        LMTD Area Estimation: {} m^2
        Heat Duty: {} kW
        Number of {}s required: {}
        """.format(str(process[i][0]), LMTD, areaLMTD, Q/1000, process[i][0].type, x))

if mode == "H":
    ### HTU Estimation ###

    n = [x+1 if x == 0 else x for x in range(6,101,1)]
    t = []
    area = []
    for slices in n:
        A = HEX2.sizeHTU('hot', slices)
        x = HEX2.number_required(A)
        t.append(x)
        area.append(A)
        # print("""
        # {}
        # Using {} slices
        # Area: {} m^2
        # {}s: {}
        # Duty: {} kW""".format(str(HEX2), slices, A, HEX2.type, x, sum(HEX2.Qs)/1000))
    percent = [100*(abs(i - t[-1])/t[-1]) for i in t]
    # fig = plt.figure(str(HEX1))
    # ax1 = plt.subplot(2,1,1)
    # ax2 = plt.subplot(2,1,2)
    # ax1.plot(n, percent)
    # ax1.set_ylabel('Error [%]')
    plt.figure(str(HEX1))
    plt.plot(n, area)
    plt.ylabel('Heat Exchange Area [m^2]')
    plt.xlabel('Number of units [-]')
    plt.show()

if mode == "O":
    ### HTU Optimisation for cold fluid flow ###

    m = [2.03576, 0.89]#np.arange(0.5, 0.91, 0.10)
    for mass in m:
        HEX1.hotFluid.m = mass
        n = [100]
        for slices in n:
            repeat = True
            while repeat:
                A = HEX1.sizeHTU('hot', slices)
                x = HEX1.number_required(A)
                tolerance = 1
                if HEX1.hotFluid.Tdistro[-1] >= HEX1.hotFluid.Ti - tolerance and HEX1.hotFluid.Tdistro[-1] <= HEX1.hotFluid.Ti + tolerance:
                    repeat = False
                elif HEX1.hotFluid.Tdistro[-1] >= HEX1.hotFluid.Ti - tolerance:
                    HEX1.coldFluid.m -= 0.0001
                    # print('got {} K, add, trying {} kg/s'.format(HEX1.hotFluid.Tdistro[-1], HEX1.coldFluid.m))
                elif HEX1.hotFluid.Tdistro[-1] <= HEX1.hotFluid.Ti + tolerance:
                    HEX1.coldFluid.m += 0.0001
                    # print('got {} K, sub, trying {} kg/s'.format(HEX1.hotFluid.Tdistro[-1], HEX1.coldFluid.m))
            
            print("""
            {}
            Using {} slices
            Overall Coeff: {}
            Area: {} m^2
            Duty: {} W
            {}s: {}
            Hot Temps: {} -> {}
            Hot Flow: {} kg s^-1
            Cold Temps: {} -> {}
            Cold Flow: {} kg s^-1""".format(str(HEX1), slices, HEX1.U, A, sum(HEX1.Qs), HEX1.type, x, HEX1.hotFluid.Tdistro[-1], HEX1.hotFluid.Tdistro[0], HEX1.hotFluid.m, HEX1.coldFluid.Tdistro[0], HEX1.coldFluid.Tdistro[-1], HEX1.coldFluid.m))


if mode == "SM":
    ### HTU Sensitivity Analysis on mass flowrate###

    m = np.arange(0.05, 3, 0.05)
    U = np.arange(10, 150, 5)
    T = HEX1.hotFluid.To
    n = 100

    U, m = np.meshgrid(U, m)
    Z = HEX1.sensitivity_area('hot', n, U, T, m)

    fig = plt.figure(str(HEX1))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(m, U, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
    ax.set_xlabel('Air Mass Flowrate [kg/s]')
    ax.set_ylabel('Overall Heat Transfer Coefficient [W/m^2K]')
    ax.set_zlabel('Heat Exchanger Area [m^2]')
    ax.set_title('Sensitivity Analysis on ' + str(HEX1))
    plt.show()

if mode == "ST":
    ### HTU Sensitivity Analysis on outlet temperature ###

    T = np.arange(289, 297, 0.05)
    U = np.arange(10, 155, 5)
    m = HEX1.hotFluid.m
    n = 100

    U, T = np.meshgrid(U, T)
    Z = HEX1.sensitivity_area('hot', n, U, T, m)

    fig = plt.figure(str(HEX1))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(T, U, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
    ax.set_xlabel('Air Outlet Temperature [K]')
    ax.set_ylabel('Overall Heat Transfer Coefficient [W/m^2K]')
    ax.set_zlabel('Heat Exchanger Area [m^2]')
    ax.set_title('Sensitivity Analysis on ' + str(HEX1))
    plt.show()

if mode == "SL":
    ### HTU Sensitivity Analysis on length ###

    L = np.arange(0.5, 1.55, 0.05)
    Di = np.arange(0.01, 0.055, 0.005)
    A = 10
    n = 100

    L, Di = np.meshgrid(L, Di)
    Z = HEX1.sensitivity_length('hot', n, A, L, Di)

    fig = plt.figure(str(HEX1))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(L, Di, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
    ax.set_xlabel('Length [m]')
    ax.set_ylabel('Diameter [m]')
    ax.set_zlabel('{} Required [-]'.format(HEX1.type))
    ax.set_title('Sensitivity Analysis on ' + str(HEX1))
    plt.show()

if mode == 'HP':
    ### Heat plot of fluids across the heat exchanger ###

    n = [100]
    plt.figure(str(HEX2))
    ax1 = plt.subplot(2,1,1)
    ax2 = plt.subplot(2,1,2)
    for i in n:
        coldDistro, hotDistro, ADistro = HEX2.heat_map('hot', i)
        ax1.plot(ADistro, coldDistro, label="n={}".format(i))
        ax2.plot(ADistro, hotDistro, label="n={}".format(i))
    ax1.legend(loc='best', shadow=True, fancybox=True)
    ax2.legend(loc='best', shadow=True, fancybox=True)
    ax1.set_title(str(HEX2))
    ax1.set_ylabel('Cold Fluid Temperature [K]')
    ax2.set_xlabel('Position in Heat Exchanger [m^2]')
    ax2.set_ylabel('Hot Fluid Temperature [K]')

    plt.show()

if mode == 'HM':
    ### Heat map of fluids across the heat exchanger ###

    N = [5,10,20,100]
    for n in N:
        plt.figure(str(HEX1) + " with n = {}".format(n))
        ax1 = plt.subplot(2,1,1)
        ax2 = plt.subplot(2,1,2)
        coldDistro, hotDistro, ADistro = HEX2.heat_map('hot', n)
        y = np.arange(0,1,0.1)
        y, ADistro = np.meshgrid(y, ADistro)
        y = np.arange(0,1,0.1)
        y, coldDistro = np.meshgrid(y, coldDistro)
        ax1.plot(ADistro, coldDistro)
        ax2.pcolormesh(ADistro, y, coldDistro, cmap='coolwarm')
        ax1.set_title(str(HEX2) + " with n = {}".format(n))
        ax1.set_ylabel('Cold Fluid Temperature [K]')
        ax2.set_xlabel('Position in Heat Exchanger [m^2]')
        ax2.set_yticklabels([])
    plt.show()