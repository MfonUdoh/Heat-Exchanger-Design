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
(R)eport
(HP) Heat Plot
(HM) Heat Map""")
mode = input().upper()

if mode == "L":
    ### LMTD Estimation ###

    process = [[HEX1, 'hot'], [HEX2, 'hot'], [HEX3, 'hot']]
    for i in range(len(process)):
        LMTD, areaLMTD, Q = process[i][0].sizeLMTD(process[i][1])
        x = process[i][0].number_required(areaLMTD)
        print("""
        {}
        LMTD: {}
        LMTD Area Estimation: {} m$^2$
        Heat Duty: {} kW
        Number of {}s required: {}
        """.format(str(process[i][0]), LMTD, areaLMTD, Q/1000, process[i][0].type, x))

if mode == "H":
    ### HTU Estimation ###

    n = [50]
    t = []
    area = []
    for slices in n:
        A = HEX2.sizeHTU('hot', slices)
        x = HEX2.number_required(A)
        t.append(x)
        area.append(A)
        print("""
        {}
        Using {} slices
        Area: {} m^2
        {}s: {}
        Duty: {} kW""".format(str(HEX3), slices, A, HEX2.type, x, sum(HEX2.Qs)/1000))

if mode == "C":
    ### Compares accuracy of HTU estimation ###
    n = [x+1 if x == 0 else x for x in range(6,101,1)]
    t = []
    area = []
    for slices in n:
        A = HEX2.sizeHTU('hot', slices)
        x = HEX2.number_required(A)
        t.append(x)
        area.append(A)

    plt.figure(str(HEX3) + " area estimation")
    plt.plot(n, area)
    plt.ylabel('Heat Exchange Area [m$^2$]')
    plt.xlabel('Number of Differential Units [-]')
    plt.show()


if mode == "M":
    ### Calculates required mass flow rate for specified outlet temperature ###

    n = [100]
    t = []
    area = []
    for slices in n:
        HEX3.find_mass(293)
        A = HEX3.sizeHTU('hot', slices)
        x = HEX3.number_required(A)
        t.append(x)
        area.append(A)
        print("""
        {}
        Using {} slices
        Area: {} m^2
        {}s: {}
        Duty: {} kW
        Cold: {} -> {}
        Hot: {} -> {}
        """.format(str(HEX3), slices, A, HEX3.type, x, sum(HEX3.Qs)/1000, HEX3.coldFluid.Tdistro[0], HEX3.coldFluid.Tdistro[-1], HEX3.hotFluid.Tdistro[0], HEX3.hotFluid.Tdistro[-1]))
    

if mode == "O":
    ### HTU Optimisation for cold fluid flow ###
    n = 1000
    
    length = [x for x in np.arange(0.2,3.1,0.05)]
    width = [x for x in np.arange(0.1,1.4,0.05)]
    port_diameter = [0.1] #[x for x in np.arange(0.05,1,0.01)]
    thickness = [0.002]
    enlargement = [1.2] #  1.15, 1.2, 1.25
    chevronAngles = [65]
    channelThick = [0.005]
    passes = [1] # 1, 2, 3, 4
    yes_counter = 0
    no_counter = 0
    U, dPc, dPh = HEX3.analysis(n)
    # print("""
    # {}
    # Area: {} m$^2$
    # Number of plates: {}
    # Overall Coeff: {} W/m$^2$K
    # Pressure Drop: {} bar
    # """.format(str(HEX3), HEX3.A, HEX3.channels+1, np.average(U), np.average(dP)/100000))
    
    # with open('analysis.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow([str(HEX3)])
    #     writer.writerow(['Number of Plates', 'Area', 'Overall Coeff', 'Width', 'Length', 'Enlargement', 'Channel Thickness', 'Plate Thickness', 'Port Diameter', 'Chevron Angle', 'Correction Factor', 'Passes', 'Pressure Drop Cold', 'Pressure Drop Hot'])
    #     for l in length:
    #         for w in width:
    #             for d_p in port_diameter:
    #                 if l >= 2*w and l <= 3*w and w > 2*d_p:
    #                     for t_p in thickness:
    #                         for phi in enlargement:
    #                             for angle in chevronAngles:
    #                                 for b in channelThick:
    #                                     for p in passes:
    #                                         if p == 2:
    #                                             HEX3.corrFac = 0.9
    #                                         elif p == 3:
    #                                             HEX3.corrFac = 0.98
    #                                         else:
    #                                             HEX3.corrFac = 0.95

    #                                         HEX3.L = l
    #                                         HEX3.W = w
    #                                         HEX3.t_p = t_p
    #                                         HEX3.Phi = phi
    #                                         HEX3.chevAngle = angle
    #                                         HEX3.b = b
    #                                         HEX3.passes = p
    #                                         HEX3.d_p = d_p
    #                                         U, dPc, dPh = HEX3.analysis(n)
    #                                         if np.average(U) >= 25 and np.average(U) <= 35:
    #                                             writer.writerow([HEX3.channels+1, HEX3.A, np.average(U), HEX3.W, HEX3.L, HEX3.Phi, HEX3.b, HEX3.t_p, HEX3.d_p, HEX3.chevAngle, HEX3.corrFac, HEX3.passes, np.average(dPc), np.average(dPh)])
    #                                             yes_counter += 1
    #                                         else:
    #                                             writer.writerow([HEX3.channels+1, HEX3.A, np.average(U), HEX3.W, HEX3.L, HEX3.Phi, HEX3.b, HEX3.t_p, HEX3.d_p, HEX3.chevAngle, HEX3.corrFac, HEX3.passes, np.average(dPc), np.average(dPh)])
    #                                             no_counter += 1
    #                                         print('Done {}!'.format(no_counter + yes_counter))
    # print('Finished, total of {}, {} failed, {} passed!'.format(no_counter + yes_counter, no_counter, yes_counter))
    As = HEX3.As
    i = 0
    A = [0]
    for x in As:
        i += x
        A.append(i)
    plt.figure("detailed pressure")
    plt.plot(A, U)
    plt.xlabel('Heat Exchange Area [m$^2$]')
    plt.ylabel('Overall Heat Transfer Coefficient [W m$^{-2}$ K$^{-1}$]')
    plt.show()
    plt.figure("detailed coeff")
    plt.plot(A, dPc)
    plt.xlabel('Heat Exchange Area [m$^2$]')
    plt.ylabel('Cold Stream Pressure Drop [Pa]')
    plt.show()
    plt.figure("detailed reynolds")
    plt.plot(A, HEX3.coldFluid.Re)
    plt.xlabel('Heat Exchange Area [m$^2$]')
    plt.ylabel('Cold Stream Reynolds Number [-]')
    plt.show()
    plt.figure("detailed prandtl")
    plt.plot(A, HEX3.coldFluid.Pr)
    plt.xlabel('Heat Exchange Area [m$^2$]')
    plt.ylabel('Cold Stream Prandtl Number [-]')
    plt.show()
    plt.figure("detailed nusselt")
    plt.plot(A, HEX3.coldFluid.Nu)
    plt.xlabel('Heat Exchange Area [m$^2$]')
    plt.ylabel('Cold Stream Nusselt Number [-]')
    plt.show()
    plt.figure("detailed convec")
    plt.plot(A, HEX3.coldFluid.convec)
    plt.xlabel('Heat Exchange Area [m$^2$]')
    plt.ylabel('Cold Stream Convective Coefficient [W m$^{-2}$ K$^{-1}$]')
    plt.show()
    print(np.average(dPc))

if mode == "FIG1":
    ### Optimise Channel Thickness and Chevron Angle ###
    n = 50

    length = [0.7]
    width = [0.3]
    port_diameter = [0.1] #[x for x in np.arange(0.05,1,0.01)]
    thickness = [0.002]
    enlargement = [1.2] #  1.15, 1.2, 1.25
    chevronAngles = [30, 45, 50, 60, 65]
    channelThick = [x for x in np.arange(0.0015,0.0051,0.0001)]
    passes = [1] # 1, 2, 3, 4
    unit = 1
    
    for l in length:
        for w in width:
            for d_p in port_diameter:
                if l >= 2*w and l <= 3*w and w > 2*d_p:
                    for t_p in thickness:
                        for phi in enlargement:
                            for angle in chevronAngles:
                                solution = []
                                solution2 = []
                                solution3 = []
                                for b in channelThick:
                                    for p in passes:
                                        if p == 2:
                                            HEX3.corrFac = 0.91
                                        elif p == 3:
                                            HEX3.corrFac = 0.98
                                        else:
                                            HEX3.corrFac = 0.95

                                        HEX3.L = l
                                        HEX3.W = w
                                        HEX3.t_p = t_p
                                        HEX3.Phi = phi
                                        HEX3.chevAngle = angle
                                        HEX3.b = b
                                        HEX3.passes = p
                                        HEX3.d_p = d_p
                                        U, dPc, dPh = HEX3.analysis(n)
                                        solution.append((np.average(dPc) + np.average(dPh))/(10**5))
                                        solution2.append(np.average(U))
                                        cold_cost = (((np.average(dPc)*unit*((HEX3.coldFluid.m*unit)/0.8061))/(0.9*1000))*0.15*3*365*20)
                                        hot_cost = (((np.average(dPh)*unit*((HEX3.hotFluid.m*unit)/1.184))/(0.9*1000))*0.15*3*365*20)
                                        cost = hot_cost + cold_cost + (1600 + 210*(HEX3.A)**0.95)*unit
                                        solution3.append(np.average(cost)/10**6)
                                plt.figure("channel vs angle pressure")
                                plt.plot(channelThick, solution, label="{}$^\circ$".format(angle))
                                plt.xlabel('Channel Thickness [m]')
                                plt.ylabel('Total Pressure Drop [bar]')
                                plt.legend(loc='best', shadow=True, fancybox=True)
                                plt.figure("channel vs angle coeff")
                                plt.plot(channelThick, solution2, label="{}$^\circ$".format(angle))
                                plt.xlabel('Channel Thickness [m]')
                                plt.ylabel('Overall Heat Transfer Coefficient [W m$^{-2}$ K$^{-1}$]')
                                plt.legend(loc='best', shadow=True, fancybox=True)
                                plt.figure("channel vs angle cost")
                                plt.plot(channelThick, solution3, label="{}$^\circ$".format(angle))
                                plt.xlabel('Channel Thickness [m]')
                                plt.ylabel('Whole-life Cost [£1m]')
                                plt.legend(loc='best', shadow=True, fancybox=True)

    plt.show()

if mode == "FIG2":
    ### Compares plate lengths and widths ###
    n = 50

    length = [x for x in np.arange(0.4,2.01,0.1)]
    width = [x for x in np.arange(0.2,1.1,0.1)]
    port_diameter = [0.05] # change to 0.15 for figure 2.5
    thickness = [0.002]
    enlargement = [1.2] #  1.15, 1.2, 1.25
    chevronAngles = [65]
    channelThick = [0.005]
    passes = [1] # 1, 2, 3, 4
    unit = 1

    for w in width:
        solution = []
        solution2 = []
        solution3 = []
        axis = []
        for l in length:
            for d_p in port_diameter:
                if l >= 2*w and l <= 3*w and w >= 2*d_p:
                    for t_p in thickness:
                        for phi in enlargement:
                            for angle in chevronAngles:
                                for b in channelThick:
                                    for p in passes:
                                        if p == 2:
                                            HEX3.corrFac = 0.91
                                        elif p == 3:
                                            HEX3.corrFac = 0.98
                                        else:
                                            HEX3.corrFac = 0.95

                                        HEX3.L = l
                                        HEX3.W = w
                                        HEX3.t_p = t_p
                                        HEX3.Phi = phi
                                        HEX3.chevAngle = angle
                                        HEX3.b = b
                                        HEX3.passes = p
                                        HEX3.d_p = d_p
                                        U, dPc, dPh = HEX3.analysis(n)
                                        if (np.average(dPc) + np.average(dPh))/(10**5) > 0:
                                            solution.append((np.average(dPc) + np.average(dPh))/(10**5))
                                            axis.append(l)
                                            solution2.append(np.average(U))
                                            cold_cost = (((np.average(dPc)*unit*((HEX3.coldFluid.m*unit)/0.8061))/(0.9*1000))*0.15*3*365*20)
                                            hot_cost = (((np.average(dPh)*unit*((HEX3.hotFluid.m*unit)/1.184))/(0.9*1000))*0.15*3*365*20)
                                            cost = hot_cost + cold_cost + (1600 + 210*(HEX3.A)**0.95)*unit
                                            solution3.append(np.ceil(HEX3.plates))
        if solution != []:
            plt.figure("plate sizes pressure")
            plt.plot(axis, solution, label="{}m".format(np.around(w, decimals=2)))
            plt.xlabel('Plate Length [m]')
            plt.ylabel('Total Pressure Drop [bar]')
            plt.legend(loc='best', shadow=True, fancybox=True)
            plt.figure("plate sizes coeff")
            plt.plot(axis, solution2, label="{}m".format(np.around(w, decimals=2)))
            plt.xlabel('Plate Length [m]')
            plt.ylabel('Overall Heat Transfer Coefficient [W m$^{-2}$ K$^{-1}$]')
            plt.legend(loc='best', shadow=True, fancybox=True)
            plt.figure("plate sizes plates")
            plt.plot(axis, solution3, label="{}m".format(np.around(w, decimals=2)))
            plt.xlabel('Plate Length [m]')
            plt.ylabel('Number of Plates [-]')
            plt.legend(loc='best', shadow=True, fancybox=True)
    
    
    plt.show()

if mode == "FIG3":
    ### Compares Port Diameter for smallest plates ###
    n = 50
    
    sizes = [[0.4, 0.2], [0.6, 0.3], [0.8, 0.4]]
    port_diameter = [x for x in np.arange(0.05,0.5,0.005)]
    thickness = [0.002]
    enlargement = [1.15] #  1.15, 1.2, 1.25
    chevronAngles = [65]
    channelThick = [0.005]
    passes = [1]

    for p in passes:
        for i in sizes:
            solution = []
            axis = []
            for d_p in port_diameter:
                if i[0] >= 2*i[1] and i[0] <= 3*i[1] and 2*d_p + 0.05 <= i[1]:
                    for t_p in thickness:
                        for phi in enlargement:
                            for angle in chevronAngles:
                                for b in channelThick:
                                    if p == 2:
                                        HEX3.corrFac = 0.91
                                    elif p == 3:
                                        HEX3.corrFac = 0.98
                                    else:
                                        HEX3.corrFac = 0.95

                                    HEX3.L = i[0]
                                    HEX3.W = i[1]
                                    HEX3.t_p = t_p
                                    HEX3.Phi = phi
                                    HEX3.chevAngle = angle
                                    HEX3.b = b
                                    HEX3.passes = p
                                    HEX3.d_p = d_p
                                    U, dPc, dPh = HEX3.analysis(n)
                                    if (np.average(dPc) + np.average(dPh))/(10**5) > 0:
                                        solution.append((np.average(dPc) + np.average(dPh))/(10**5))
                                        axis.append(d_p)
            if solution != []:
                plt.figure("Port Diameter vs sizes")
                plt.plot(axis, solution, label="{}m x {}m".format(HEX3.L, HEX3.W))
    
    plt.xlabel('Port Diameter [m]')
    plt.ylabel('Total Pressure Drop [bar]')
    plt.legend(loc='best', shadow=True, fancybox=True)
    plt.show()

if mode == "FIG31":
    ### Compares Port Diameter for smallest plates ###
    n = 50
    
    sizes = [[0.6, 0.3], [0.7, 0.3], [0.8, 0.3], [0.9, 0.3]]
    port_diameter = [x for x in np.arange(0.05,0.5,0.005)]
    thickness = [0.002]
    enlargement = [1.15] #  1.15, 1.2, 1.25
    chevronAngles = [65]
    channelThick = [0.005]
    passes = [1]

    for p in passes:
        for i in sizes:
            solution = []
            axis = []
            for d_p in port_diameter:
                if i[0] >= 2*i[1] and i[0] <= 3*i[1] and 2*d_p + 0.05 <= i[1]:
                    for t_p in thickness:
                        for phi in enlargement:
                            for angle in chevronAngles:
                                for b in channelThick:
                                    if p == 2:
                                        HEX3.corrFac = 0.91
                                    elif p == 3:
                                        HEX3.corrFac = 0.98
                                    else:
                                        HEX3.corrFac = 0.95

                                    HEX3.L = i[0]
                                    HEX3.W = i[1]
                                    HEX3.t_p = t_p
                                    HEX3.Phi = phi
                                    HEX3.chevAngle = angle
                                    HEX3.b = b
                                    HEX3.passes = p
                                    HEX3.d_p = d_p
                                    U, dPc, dPh = HEX3.analysis(n)
                                    if (np.average(dPc) + np.average(dPh))/(10**5) > 0:
                                        solution.append((np.average(dPc) + np.average(dPh))/(10**5))
                                        axis.append(d_p)
            if solution != []:
                plt.figure("port diameter vs length")
                plt.plot(axis, solution, label="{}m x {}m".format(HEX3.L, HEX3.W))
    
    plt.xlabel('Port Diameter [m]')
    plt.ylabel('Total Pressure Drop [bar]')
    plt.legend(loc='best', shadow=True, fancybox=True)
    plt.show()

if mode == "FIG32":
    ### Compares Port Diameter for smallest plates ###
    n = 50
    
    sizes = [[0.6, 0.2], [0.6, 0.25], [0.6, 0.3]]
    port_diameter = [x for x in np.arange(0.05,0.5,0.005)]
    thickness = [0.002]
    enlargement = [1.15] #  1.15, 1.2, 1.25
    chevronAngles = [65]
    channelThick = [0.005]
    passes = [1]

    for p in passes:
        for i in sizes:
            solution = []
            axis = []
            for d_p in port_diameter:
                if i[0] >= 2*i[1] and i[0] <= 3*i[1] and 2*d_p + 0.05 <= i[1]:
                    for t_p in thickness:
                        for phi in enlargement:
                            for angle in chevronAngles:
                                for b in channelThick:
                                    if p == 2:
                                        HEX3.corrFac = 0.91
                                    elif p == 3:
                                        HEX3.corrFac = 0.98
                                    else:
                                        HEX3.corrFac = 0.95

                                    HEX3.L = i[0]
                                    HEX3.W = i[1]
                                    HEX3.t_p = t_p
                                    HEX3.Phi = phi
                                    HEX3.chevAngle = angle
                                    HEX3.b = b
                                    HEX3.passes = p
                                    HEX3.d_p = d_p
                                    U, dPc, dPh = HEX3.analysis(n)
                                    if (np.average(dPc) + np.average(dPh))/(10**5) > 0:
                                        solution.append((np.average(dPc) + np.average(dPh))/(10**5))
                                        axis.append(d_p)
            if solution != []:
                plt.figure("port diameter vs width")
                plt.plot(axis, solution, label="{}m x {}m".format(HEX3.L, HEX3.W))
    
    plt.xlabel('Port Diameter [m]')
    plt.ylabel('Total Pressure Drop [bar]')
    plt.legend(loc='best', shadow=True, fancybox=True)
    plt.show()

if mode == "FIG4":
    ### Compares Port Diameter and passes ###
    n = 50

    length = [0.6]
    width = [0.3]
    port_diameter = [0.125] #[x for x in np.arange(0.05,0.5,0.005)]
    thickness = [0.002]
    enlargement = [1.2]
    chevronAngles = [65]
    channelThick = [0.005]
    passes = [1, 2, 3, 4]
    unit = 1

    solution = []
    solution2 = []
    solution3 = []
    axis = []

    for p in passes:
        for w in width:
            for l in length:
                for d_p in port_diameter:
                    if l >= 2*w and l <= 3*w and w > 2*d_p:
                        for t_p in thickness:
                            for phi in enlargement:
                                for angle in chevronAngles:
                                    for b in channelThick:
                                        if p == 2:
                                            HEX3.corrFac = 0.91
                                        elif p == 3:
                                            HEX3.corrFac = 0.98
                                        else:
                                            HEX3.corrFac = 0.95

                                        HEX3.L = l
                                        HEX3.W = w
                                        HEX3.t_p = t_p
                                        HEX3.Phi = phi
                                        HEX3.chevAngle = angle
                                        HEX3.b = b
                                        HEX3.passes = p
                                        HEX3.d_p = d_p
                                        U, dPc, dPh = HEX3.analysis(n)
                                        if (np.average(dPc) + np.average(dPh))/(10**5) > 0:
                                            axis.append(p)
                                            solution.append((np.average(dPc) + np.average(dPh))/(10**5))
                                            solution2.append(np.average(U))
                                            cold_cost = (((np.average(dPc)*unit*((HEX3.coldFluid.m*unit)/0.8061))/(0.9*1000))*0.15*3*365*20)
                                            hot_cost = (((np.average(dPh)*unit*((HEX3.hotFluid.m*unit)/1.184))/(0.9*1000))*0.15*3*365*20)
                                            cost = hot_cost + cold_cost + (1600 + 210*(HEX3.A)**0.95)*unit
                                            solution3.append(np.average(cost)/10**3)
    if solution != []:
        plt.figure("passes pressure")
        plt.plot(axis, solution)
        plt.xlabel('Number of Passes')
        plt.ylabel('Total Pressure Drop [bar]')

    plt.show()


if mode == "FIG5":
    ### Compares Enlargement Factor ###
    n = 50

    length = [0.6]
    width = [0.3]
    port_diameter = [0.125]
    thickness = [0.002]
    enlargement = [x for x in np.arange(1.15,1.26,0.01)]
    chevronAngles = [65]
    channelThick = [0.005]
    passes = [1]
    unit = 1

    for p in passes:
        for w in width:
            for l in length:
                for d_p in port_diameter:
                    for t_p in thickness:
                        solution = []
                        solution2 = []
                        solution3 = []
                        axis = []
                        for phi in enlargement:
                            for angle in chevronAngles:
                                for b in channelThick:
                                    if p == 2:
                                        HEX3.corrFac = 0.91
                                    elif p == 3:
                                        HEX3.corrFac = 0.98
                                    else:
                                        HEX3.corrFac = 0.95

                                    HEX3.L = l
                                    HEX3.W = w
                                    HEX3.t_p = t_p
                                    HEX3.Phi = phi
                                    HEX3.chevAngle = angle
                                    HEX3.b = b
                                    HEX3.passes = p
                                    HEX3.d_p = d_p
                                    U, dPc, dPh = HEX3.analysis(n)
                                    if (np.average(dPc) + np.average(dPh))/(10**5) > 0:
                                        solution.append((np.average(dPc) + np.average(dPh))/(10**5))
                                        solution2.append(np.average(U))
                                        cold_cost = (((np.average(dPc)*unit*((HEX3.coldFluid.m*unit)/0.8061))/(0.9*1000))*0.15*3*365*20)
                                        hot_cost = (((np.average(dPh)*unit*((HEX3.hotFluid.m*unit)/1.184))/(0.9*1000))*0.15*3*365*20)
                                        cost = hot_cost + cold_cost + (1600 + 210*(HEX3.A)**0.95)*unit
                                        solution3.append(np.ceil(HEX3.plates))
                                        axis.append(phi)
                        if solution != []:
                            plt.figure("enlargement pressure")
                            plt.plot(axis, solution)
                            plt.xlabel('Enlargement Factor [-]')
                            plt.ylabel('Total Pressure Drop [bar]')
                            plt.figure("enlargement coeff")
                            plt.plot(axis, solution2)
                            plt.xlabel('Enlargement Factor [-]')
                            plt.ylabel('Overall Heat Transfer Coefficient [W m$^{-2}$ K$^{-1}$]')
                            plt.figure("enlargement plates")
                            plt.plot(axis, solution3)
                            plt.xlabel('Enlargement Factor [-]')
                            plt.ylabel('Number of Plates [-]')

    plt.show()

if mode == "FIG6":
    ### Compares Plate Thickness ###
    n = 50

    length = [0.6]
    width = [0.3]
    port_diameter = [0.125]
    thickness = [x for x in np.arange(0.0015, 0.0031, 0.0001)]
    enlargement = [1.15]
    chevronAngles = [65]
    channelThick = [0.005]
    passes = [1]
    unit = 1

    for p in passes:
        for w in width:
            for l in length:
                for d_p in port_diameter:
                    if l >= 2*w and l <= 3*w:
                        solution = []
                        solution2 = []
                        solution3 = []
                        axis = []
                        for t_p in thickness:
                            for phi in enlargement:
                                for angle in chevronAngles:
                                    for b in channelThick:
                                        if p == 2:
                                            HEX3.corrFac = 0.91
                                        elif p == 3:
                                            HEX3.corrFac = 0.98
                                        else:
                                            HEX3.corrFac = 0.95

                                        HEX3.L = l
                                        HEX3.W = w
                                        HEX3.t_p = t_p
                                        HEX3.Phi = phi
                                        HEX3.chevAngle = angle
                                        HEX3.b = b
                                        HEX3.passes = p
                                        HEX3.d_p = d_p
                                        U, dPc, dPh = HEX3.analysis(n)
                                        if (np.average(dPc) + np.average(dPh))/(10**5) > 0:
                                            solution.append(np.average(U))
                                            solution2.append((np.average(dPc) + np.average(dPh))/(10**5))
                                            cold_cost = (((np.average(dPc)*unit*((HEX3.coldFluid.m*unit)/0.8061))/(0.9*1000))*0.15*3*365*20)
                                            hot_cost = (((np.average(dPh)*unit*((HEX3.hotFluid.m*unit)/1.184))/(0.9*1000))*0.15*3*365*20)
                                            cost = hot_cost + cold_cost + (1600 + 210*(HEX3.A)**0.95)*unit
                                            solution3.append(np.average(cost)/10**3)
                                            axis.append(t_p)
                        if solution != []:
                            plt.figure("platethick coeff")
                            plt.plot(axis, solution)
                            plt.xlabel('Plate Thickness [m]')
                            plt.ylabel('Overall Heat Transfer Coefficient [W m$^{-2}$ K$^{-1}$]')
                            plt.figure("platethick pressure")
                            plt.plot(axis, solution2)
                            plt.xlabel('Plate Thickness [m]')
                            plt.ylabel('Total Pressure Drop [bar]')
                            plt.figure("platethick cost")
                            plt.plot(axis, solution3)
                            plt.xlabel('Plate Thickness [m]')
                            plt.ylabel('Whole-life Cost [£1,000]')
    plt.show()

if mode == "FIG7":
    ### Compares Number of Units ###
    n = 10

    length = 0.6
    width = 0.3
    port_diameter = 0.125
    thickness = 0.0015
    enlargement = 1.15
    chevronAngles = 65
    channelThick = 0.005
    passes = 1
    units = [x for x in range(1,11)]

    HEX3.L = length
    HEX3.W = width
    HEX3.t_p = thickness
    HEX3.Phi = enlargement
    HEX3.chevAngle = chevronAngles
    HEX3.b = channelThick
    HEX3.passes = passes
    HEX3.d_p = port_diameter

    solution = []
    solution2 = []
    axis = []
    for unit in units:
        HEX3.coldFluid.m /= unit
        HEX3.hotFluid.m /= unit
        U, dPc, dPh = HEX3.analysis(n)
        if (np.average(dPc) + np.average(dPh))/(10**5) > 0 and HEX3.A > 0.03:
            cold_cost = (((np.average(dPc)*unit*((HEX3.coldFluid.m*unit)/0.8061))/(0.9*1000))*0.15*3*365*20)
            hot_cost = (((np.average(dPh)*unit*((HEX3.hotFluid.m*unit)/1.184))/(0.9*1000))*0.15*3*365*20)
            cost = hot_cost + cold_cost + (1600 + 210*(HEX3.A)**0.95)*unit
            print(cost)
            solution.append(np.average(cost)/10**3)
            solution2.append((np.average(dPc) + np.average(dPh))/10**5)
            axis.append(unit)
    if solution != []:
        plt.figure(str(HEX1) + " cost")
        plt.plot(axis, solution)
        plt.xlabel('Number of Units')
        plt.ylabel('Whole-life Cost [£1,000]')
        plt.figure(str(HEX1) + " pressure")
        plt.plot(axis, solution2)
        plt.xlabel('Number of Units')
        plt.ylabel('Total Pressure Drop [bar]')
    plt.show()

if mode == "FIG8":
    ### Compares Outlet Temperature of Air ###
    n = 50

    length = 0.6
    width = 0.3
    port_diameter = 0.125
    thickness = 0.0015
    enlargement = 1.15
    chevronAngles = 65
    channelThick = 0.005
    passes = 1
    units = [1]#[x for x in range(1,11)]
    temps = [x for x in np.arange(291, 293.05, 0.05)]

    HEX3.L = length
    HEX3.W = width
    HEX3.t_p = thickness
    HEX3.Phi = enlargement
    HEX3.chevAngle = chevronAngles
    HEX3.b = channelThick
    HEX3.passes = passes
    HEX3.d_p = port_diameter

    for unit in units:
        solution = []
        solution2 = []
        solution3 = []
        solution4 = []
        axis = []
        for temp in temps:
            HEX3.coldFluid.m /= unit
            HEX3.hotFluid.m /= unit
            HEX3.find_mass(temp)
            U, dPc, dPh = HEX3.analysis(n)
            if (np.average(dPc) + np.average(dPh))/(10**5) > 0 and HEX3.A > 0.03:
                cold_cost = (((np.average(dPc)*unit*((HEX3.coldFluid.m*unit)/0.8061))/(0.9*1000))*0.15*3*365*20)
                hot_cost = (((np.average(dPh)*unit*((HEX3.hotFluid.m*unit)/1.184))/(0.9*1000))*0.15*3*365*20)
                cost = hot_cost + cold_cost + (1600 + 210*(HEX3.A)**0.95)*unit
                solution.append(np.average(cost)/10**3)
                solution2.append((np.average(dPc) + np.average(dPh))/(10**5))
                solution3.append(HEX3.hotFluid.m)
                solution4.append(np.ceil(HEX3.plates))
                axis.append(temp)
        if solution != []:
            plt.figure("airtemp cost")
            plt.plot(axis, solution, label="{}".format(unit))
            plt.xlabel('Air Outlet Temperature [K]')
            plt.ylabel('Whole-life Cost [£1,000]')
            plt.figure("airtemp pressure")
            plt.plot(axis, solution2, label="{}".format(unit))
            plt.xlabel('Air Outlet Temperature [K]')
            plt.ylabel('Total Pressure Drop [bar]')
            plt.figure("airtemp mass")
            plt.plot(axis, solution3, label="{}".format(unit))
            plt.xlabel('Air Outlet Temperature [K]')
            plt.ylabel('Air Mass Flowrate [kg s$^{-1}$]')
            plt.figure("airtemp plates")
            plt.plot(axis, solution4, label="{}".format(unit))
            plt.xlabel('Air Outlet Temperature [K]')
            plt.ylabel('Number of Plates [-]')
    # plt.legend(loc='best', shadow=True, fancybox=True)
    plt.show()

if mode == 'R':
    ### Report on design ###

    n = 50
    t = []
    area = []

    length = 0.6
    width = 0.3
    port_diameter = 0.125
    thickness = 0.0015
    enlargement = 1.15
    chevronAngles = 65
    channelThick = 0.005
    passes = 1
    units = [1]#[x for x in range(1,11)]
    temp = 291

    HEX3.L = length
    HEX3.W = width
    HEX3.t_p = thickness
    HEX3.Phi = enlargement
    HEX3.chevAngle = chevronAngles
    HEX3.b = channelThick
    HEX3.passes = passes
    HEX3.d_p = port_diameter

    HEX3.find_mass(temp)
    A = HEX3.sizeHTU('hot', n)
    x = np.ceil(HEX3.number_required(A))
    U, dPc, dPh = HEX3.analysis(50)
    print("""
    {}
    Using   {} slices
    Area:   {} m^2
    {}s:    {}
    Duty:   {} kW
    U:      {} W/m2 K
    Cold:   
    {} K -> {} K
    {} kg/s
    {} kg/m3
    {} J/kg K
    {} Re
    {} Pr
    {} Nu
    {} h
    {} Pa

    Hot:   
    {} K -> {} K
    {} kg/s
    {} kg/m3
    {} J/kg K
    {} Re
    {} Pr
    {} Nu
    {} h
    {} Pa

    """.format(str(HEX3), n, A, HEX3.type, x, (sum(HEX3.Qs)/1000), np.average(U),\
        HEX3.coldFluid.Ti, HEX3.coldFluid.To, HEX3.coldFluid.m, np.average(HEX3.coldFluid.rho),\
        np.average(HEX3.coldFluid.Cp), np.average(HEX3.coldFluid.Re), np.average(HEX3.coldFluid.Pr),\
        np.average(HEX3.coldFluid.Nu), np.average(HEX3.coldFluid.convec), np.average(dPc),\
        HEX3.hotFluid.Ti, HEX3.hotFluid.To, HEX3.hotFluid.m, HEX3.hotFluid.rho, HEX3.hotFluid.Cp,\
        np.average(HEX3.hotFluid.Re), np.average(HEX3.hotFluid.Pr), np.average(HEX3.hotFluid.Nu), np.average(HEX3.hotFluid.convec),\
        np.average(dPh)))

if mode == 'HP':
    ### Heat plot of fluids across the heat exchanger ###

    n = [50]
    plt.figure(str(HEX3))
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
    ax2.set_xlabel('Position in Heat Exchanger [m$^2$]')
    ax2.set_ylabel('Hot Fluid Temperature [K]')

    plt.show()

if mode == 'HM':
    ### Heat map of fluids across the heat exchanger ###

    N = [5,10,20,50]
    for n in N:
        plt.figure("n={}".format(n))
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
        ax2.set_xlabel('Heat Exchange Area [m$^2$]')
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
    # ax.set_ylabel('Overall Heat Transfer Coefficient [W/m$^2$K]')
    # ax.set_zlabel('Heat Exchanger Area [m$^2$]')
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
#     ax.set_ylabel('Overall Heat Transfer Coefficient [W/m$^2$K]')
#     ax.set_zlabel('Heat Exchanger Area [m$^2$]')
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