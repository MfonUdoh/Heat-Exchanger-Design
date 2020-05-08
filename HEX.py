import numpy as np

class HeatExchanger():
    def __init__(self, name, config, cold, hot, U, basis, cF):
        self.name = name
        self.type = config
        self.coldFluid = cold
        self.hotFluid = hot
        self.U = float(U) # Overall Heat Transfer Coeff, W/m2K
        self.corrFac = cF # LMTD Correction Factor
    
    def __str__(self):
        return self.name

    def LMTD(self, Thi, Tho, Tci, Tco):
        dT1 = Thi - Tco
        dT2 = Tho - Tci
        T_lm = (dT1 - dT2)/np.log(dT1/dT2)

        return T_lm*self.corrFac

    def sizeLMTD(self, basis):
        """This function uses the LMTD method to give an estimate of the required heat transfer area of the heat exchanger.
        The basis of the estimation is the fluid that is stable enough to assumed to have a constant Cp throughout the process."""

        T_lm = self.LMTD(self.hotFluid.Ti, self.hotFluid.To, self.coldFluid.Ti, self.coldFluid.To)
        
        # Q = m * Cp * deltaTlm
        if basis == 'hot':
            Q = self.hotFluid.m * self.hotFluid.Cp * (self.hotFluid.Ti - self.hotFluid.To)
        elif basis == 'cold':
            Q = self.coldFluid.m * self.coldFluid.Cp * (self.coldFluid.To - self.coldFluid.Ti)
        else:
            print('Invalid basis')

        A_lm = Q/(self.U*T_lm)

        return T_lm, A_lm, Q

    def sizeHTU(self, basis, slices):
        """This function gives and estimation of the required heat transfer area of the heat exchanger using the heat transfer units method.
        This method makes use of enthalpy data from NIST, a number of slices are defined and the area is approximated as linear across these slices."""
        
        if slices == 0:
            return 0, 0
        dt = (self.coldFluid.To - self.coldFluid.Ti)/slices
        coldTs = [self.coldFluid.Ti]
        coldHs = [self.coldFluid.lookup('enth', self.coldFluid.Ti)]
        Tx = self.coldFluid.Ti + dt
        
        while coldTs[-1] + (dt/2) < self.coldFluid.To:
            coldTs.append(Tx)
            coldHs.append(self.coldFluid.lookup('enth', Tx))
            Tx += dt
        coldTs[-1] = self.coldFluid.To
        coldHs[-1] = self.coldFluid.lookup('enth', self.coldFluid.To)

        Qs = []
        hotTs = [self.hotFluid.To]
        h = []
        for i in range(1, len(coldHs)):
            h.append(coldHs[i] - coldHs[i-1])
            Q = (coldHs[i] - coldHs[i-1]) * self.coldFluid.m * 1000
            Qs.append(Q)
            hotTs.append((Q/(self.hotFluid.m * self.hotFluid.Cp)+hotTs[-1]))
        
        As = []
        for i in range(1, len(hotTs)):
            hoti = hotTs[i-1]
            hoto = hotTs[i]
            coldo = coldTs[i-1]
            coldi = coldTs[i]
            Q = Qs[i-1]
            T_lm = self.LMTD(hoti, hoto, coldi, coldo)
            A_lm = Q/(self.U*T_lm)
            As.append(A_lm)
        self.h = sum(h)
        self.coldFluid.Tdistro = coldTs
        self.hotFluid.Tdistro = hotTs
        self.Qs = Qs
        self.As = As
        self.A = sum(As)

        return sum(As)

    def sensitivity_area(self, basis, slices, U, T, m):
        self.U = U
        self.hotFluid.To = T
        self.hotFluid.m = m
        
        return self.sizeHTU(basis, slices)

    def heat_map(self, basis, slices):
        self.sizeHTU(basis, slices)
        ADistro = [0]
        ASum = 0
        for i in self.As:
            ASum += i
            ADistro.append(ASum)
        return self.coldFluid.Tdistro, self.hotFluid.Tdistro, ADistro

class STHE(HeatExchanger):
    def define(self, L, Di):
        self.type = 'tube'
        self.L = float(L) # Length of tube, m
        self.Di = float(Di) # Internal Diameter, m
    
    def number_required(self, A):
        self.A = A
        tubes = self.A / (np.pi * self.L * self.Di)
        return tubes

    def sensitivity_length(self, basis, slices, L, Di):
        self.L = L
        self.Di = Di
        return self.number_required(self.A)

class PHE(HeatExchanger):
    def define(self, L, W, tp, phi, passes, angle, b, D_port, k_plate):
        self.type = 'plate'
        self.L = float(L) # Length of plate, m
        self.W = float(W) # Width of plate, m
        self.t_p = float(tp) # Plate thickness [m]
        self.Phi = float(phi)
        self.passes = float(passes)
        self.chevAngle = float(angle)
        self.b = float(b) # Channel thickness [m]
        self.d_p = float(D_port) # Diameter of port [m]
        self.k_p = float(k_plate) # Conductivity of plate

    def number_required(self, A):
        self.A = A
        plates = self.A / (self.L*self.W*self.Phi)
        self.plates = plates
        return plates

    def sensitivity_length(self, basis, slices, A, L, W):
        self.L = L
        self.W = W
        return self.number_required(A)

    def get_chevron_parameters(self, angle, Re):
        params = {
            30 : {
                0 : [0.718, 0.349],
                10 : [0.348, 0.663]
            },
            45 : {
                0 :[0.718, 0.349],
                10 : [0.4, 0.598],
                100 : [0.3, 0.663]
            },
            50 : {
                0 : [0.63, 0.333],
                20 : [0.291, 0.591],
                300 : [0.130, 0.732]
            },
            60 : {
                0 : [0.562, 0.326],
                20 : [0.306, 0.529],
                400 : [0.108, 0.703]
            },
            65 : {
                0 : [0.562, 0.326],
                20 : [0.331, 0.503],
                500 : [0.087, 0.718]
            }
        }
        ranges = [i for i in params[angle]]
        for i in range(1,len(ranges)):
            if Re >= ranges[-1]:
                self.Ch = params[angle][ranges[i]][0]
                self.n = params[angle][ranges[i]][1]
            elif Re >= ranges[i-1] and Re <= ranges[i]:
                self.Ch = params[angle][ranges[i-1]][0]
                self.n = params[angle][ranges[i-1]][1]
        
        pressureParams = {
            30 : {
                0 : [50.0, 1.0],
                10 : [19.4, 0.589],
                100 : [2.99, 0.183]
            },
            45 : {
                0 :[47.0, 1.0],
                15 : [18.29, 0.652],
                300 : [1.441, 0.206]
            },
            50 : {
                0 : [34.0, 1.0],
                20 : [11.25, 0.631],
                300 : [0.772, 0.161]
            },
            60 : {
                0 : [24.0, 1.0],
                40 : [3.24, 0.457],
                400 : [0.760, 0.215]
            },
            65 : {
                0 : [24.0, 1.0],
                50 : [2.8, 0.451],
                500 : [0.639, 0.213]
            }
        }
        ranges = [i for i in pressureParams[angle]]
        for i in range(1,len(ranges)):
            if Re >= ranges[-1]:
                self.Kp = pressureParams[angle][ranges[i]][0]
                self.m = pressureParams[angle][ranges[i]][1]
            elif Re >= ranges[i-1] and Re <= ranges[i]:
                self.Kp = pressureParams[angle][ranges[i-1]][0]
                self.m = pressureParams[angle][ranges[i-1]][1]

    def fluid_analysis(self, fluid, T):
        m_c = fluid.m/self.channels
        G_c = m_c / (self.W * self.b)

        if fluid == self.coldFluid:
            Re = (G_c * self.D_e)/ fluid.lookup('mu', T)
            self.get_chevron_parameters(self.chevAngle, Re)
            Pr = (fluid.lookup('Cp', T) * fluid.lookup('mu', T)) / fluid.lookup('k', T)
            Nu = self.Ch * (Re ** self.n) * (Pr ** (1/3)) * (fluid.lookup('mu', T) / fluid.mu_w) ** 0.17
            h = (Nu * fluid.lookup('k', T)) / self.D_e

            G_p = (4 * fluid.m)/(np.pi * self.d_p**2)
            f = self.Kp / (Re ** self.m)
            dP_g = (fluid.lookup('rho', T) * 9.81 * (self.d_p + self.L))
            dP_port = 4 * (G_p ** 2 / (2 * fluid.lookup('rho', T)))
            dP_plate = ((2 * f * (self.d_p + self.L) * self.passes * G_c ** 2) / (fluid.lookup('rho', T) * self.D_e)) + 1
            dP = dP_g + dP_port + dP_plate

        else:
            Re = (G_c * self.D_e)/ fluid.mu
            self.get_chevron_parameters(self.chevAngle, Re)
            Pr = (fluid.Cp * fluid.mu) / fluid.k
            Nu = self.Ch * (Re ** self.n) * (Pr ** (1/3)) * (fluid.mu / fluid.mu_w) ** 0.17
            h = (Nu * fluid.k) / self.D_e

            G_p = (4 * fluid.m)/(np.pi * self.d_p**2)
            f = self.Kp / (Re ** self.m)
            dP_plate = ((2 * f * (self.d_p + self.L) * self.passes * G_c ** 2) / (fluid.rho * self.D_e)) + 1
            dP_port = 4 * (G_p ** 2 / (2 * fluid.rho))
            dP_g = (fluid.rho * 9.81 * (self.d_p + self.L))
            dP = dP_g + dP_port + dP_plate

        return h, dP

    def analysis(self, slices):
        self.number_required(self.sizeHTU('hot', slices))
        self.channels = np.ceil(self.plates) - 1
        self.D_e = (2 * self.b) / self.Phi
        Us = []
        dPs = []
        for i in range(len(self.coldFluid.Tdistro)):
            Th = self.hotFluid.Tdistro[-1-i]
            Tc = self.coldFluid.Tdistro[i]
            cold_h, cold_dp = self.fluid_analysis(self.coldFluid, Tc)
            hot_h, hot_dp = self.fluid_analysis(self.hotFluid, Th)
            U = 1/((1/hot_h) + (self.t_p/self.k_p) + (1/cold_h) + self.hotFluid.R_f + self.coldFluid.R_f)
            Us.append(U)
            dPs.append(cold_dp + hot_dp)

        return Us, dPs