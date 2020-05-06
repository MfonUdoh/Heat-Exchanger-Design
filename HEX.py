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
        coldHs = [self.coldFluid.lookup('temp', self.coldFluid.Ti)]
        Tx = self.coldFluid.Ti + dt
        
        while coldTs[-1] + (dt/2) < self.coldFluid.To:
            coldTs.append(Tx)
            coldHs.append(self.coldFluid.lookup('temp', Tx))
            Tx += dt
        coldTs[-1] = self.coldFluid.To
        coldHs[-1] = self.coldFluid.lookup('temp', self.coldFluid.To)

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
        tubes = A / (np.pi*self.L*self.Di)
        return tubes

    def sensitivity_length(self, basis, slices, A, L, Di):
        self.L = L
        self.Di = Di
        return self.number_required(A)

class PHE(HeatExchanger):
    def define(self, L, W):
        self.type = 'plate'
        self.L = float(L) # Length of plate, m
        self.W = float(W) # Width of plate, m

    def number_required(self, A):
        plates = A / (self.L*self.W)
        return plates

    def sensitivity_length(self, basis, slices, A, L, W):
        self.L = L
        self.W = W
        return self.number_required(A)