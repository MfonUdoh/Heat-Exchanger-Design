import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from data import *

print("""Which mode do you want to use?
(L)MTD area estimation
(H)TU area estimation
(O)ptimise
(HP) Heat Plot
(HM) Heat Map""")
mode = 'O'#input().upper()

if mode == "L":
    ### LMTD Estimation ###

    process = [[HEX1, 'hot'], [HEX2, 'hot'], [HEX3, 'hot']]
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
    n = 20
    
    length = [x for x in np.arange(0.1,1.6,0.1)]
    width = [x for x in np.arange(0.2,3.1,0.1)]
    thickness = [0.0005, 0.002, 0.003]
    enlargement = [1.15, 1.2, 1.25]
    chevronAngles = [30, 45, 50, 60, 65]
    channelThick = [x for x in np.arange(0.0015,0.0051,0.0005)]
    passes = [1, 2, 3, 4]
    factors = [0.90, 0.95]
    yes_counter = 0
    no_counter = 0
    U, dP = HEX3.analysis(n)
    # print("""
    # {}
    # Area: {} m^2
    # Number of plates: {}
    # Overall Coeff: {} W/m^2K
    # Pressure Drop: {} bar
    # """.format(str(HEX3), HEX3.A, HEX3.channels+1, np.average(U), np.average(dP)/100000))
    
    with open('analysis.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(HEX3)])
        writer.writerow(['Number of Plates', 'Area', 'Overall Coeff', 'Width', 'Length', 'Enlargement', 'Channel Thickness', 'Plate Thickness', 'Chevron Angle', 'Correction Factor', 'Pressure Drop'])
        for l in length:
            for w in width:
                if l >= 2*w and l <= 3*w:
                    for t_p in thickness:
                        for phi in enlargement:
                            for angle in chevronAngles:
                                for b in channelThick:
                                    for p in passes:
                                        for ft in factors:
                                            HEX3.L = l
                                            HEX3.W = w
                                            HEX3.t_p = t_p
                                            HEX3.Phi = phi
                                            HEX3.chevAngle = angle
                                            HEX3.b = b
                                            HEX3.passes = p
                                            HEX3.corrFac = ft
                                            # U, dP = HEX3.analysis(n)
                                            if np.average(U) >= 25 and np.average(U) <= 35:
                                                writer.writerow([HEX3.channels+1, HEX3.A, np.average(U), HEX3.W, HEX3.L, HEX3.Phi, HEX3.b, HEX3.t_p, HEX3.chevAngle, HEX3.corrFac, np.average(dP)])
                                                yes_counter += 1
                                            else:
                                                writer.writerow([HEX3.channels+1, HEX3.A, np.average(U), HEX3.W, HEX3.L, HEX3.Phi, HEX3.b, HEX3.t_p, HEX3.chevAngle, HEX3.corrFac, np.average(dP)])
                                                no_counter += 1
                                            print('Done {}!'.format(no_counter + yes_counter))
    print('Finished, total of {}, {} failed, {} passed!'.format(no_counter + yes_counter, no_counter, yes_counter))
    # As = HEX3.As
    # i = 0
    # A = [0]
    # for x in As:
    #     i += x
    #     A.append(i)
    # plt.figure(str(HEX1))
    # plt.plot(A, U)
    # plt.xlabel('Heat Exchange Area [m^2]')
    # plt.ylabel('Overall Heat Transfer Coefficient [W m^-2 K^-1]')
    # plt.show()

if mode == 'HP':
    ### Heat plot of fluids across the heat exchanger ###

    n = [50]
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

    N = [5,10,20,50]
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

# if mode == "SM":
    ### HTU Sensitivity Analysis on mass flowrate###

    # m = np.arange(0.05, 3, 0.05)
    # U = np.arange(10, 150, 5)
    # T = HEX1.hotFluid.To
    # n = 100

    # U, m = np.meshgrid(U, m)
    # Z = HEX1.sensitivity_area('hot', n, U, T, m)

    # fig = plt.figure(str(HEX1))
    # ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(m, U, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
    # ax.set_xlabel('Air Mass Flowrate [kg/s]')
    # ax.set_ylabel('Overall Heat Transfer Coefficient [W/m^2K]')
    # ax.set_zlabel('Heat Exchanger Area [m^2]')
    # ax.set_title('Sensitivity Analysis on ' + str(HEX1))
    # plt.show()

# if mode == "ST":
#     ### HTU Sensitivity Analysis on outlet temperature ###

#     T = np.arange(289, 297, 0.05)
#     U = np.arange(10, 155, 5)
#     m = HEX1.hotFluid.m
#     n = 100

#     U, T = np.meshgrid(U, T)
#     Z = HEX1.sensitivity_area('hot', n, U, T, m)

#     fig = plt.figure(str(HEX1))
#     ax = fig.gca(projection='3d')
#     surf = ax.plot_surface(T, U, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
#     ax.set_xlabel('Air Outlet Temperature [K]')
#     ax.set_ylabel('Overall Heat Transfer Coefficient [W/m^2K]')
#     ax.set_zlabel('Heat Exchanger Area [m^2]')
#     ax.set_title('Sensitivity Analysis on ' + str(HEX1))
#     plt.show()

# if mode == "SL":
#     ### HTU Sensitivity Analysis on length ###

#     L = np.arange(0.5, 1.55, 0.05)
#     Di = np.arange(0.01, 0.055, 0.005)
#     A = 10
#     n = 100

#     L, Di = np.meshgrid(L, Di)
#     Z = HEX1.sensitivity_length('hot', n, A, L, Di)

#     fig = plt.figure(str(HEX1))
#     ax = fig.gca(projection='3d')
#     surf = ax.plot_surface(L, Di, Z, rstride=1, cstride=1, cmap=cm.winter, edgecolor='none')
#     ax.set_xlabel('Length [m]')
#     ax.set_ylabel('Diameter [m]')
#     ax.set_zlabel('{} Required [-]'.format(HEX1.type))
#     ax.set_title('Sensitivity Analysis on ' + str(HEX1))
#     plt.show()