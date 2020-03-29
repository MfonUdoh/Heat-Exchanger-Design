import numpy as np

class HeatExchanger():
    def __init__(self, config, cold, hot, U, Di, L):
        self.type = config
        self.coldFluid = cold
        self.hotFluid = hot
        self.U = float(U) # Overall Heat Transfer Coeff, W/m2K
        self.Di = float(Di) # Internal Diameter, m
        self.L = float(L) # Length of tubes, m
    
    def LMTD(self, Thi, Tho, Tci, Tco):
        dT1 = Thi - Tco
        dT2 = Tho - Tci
        T_lm = (dT1 - dT2)/np.log(dT1/dT2)

        return T_lm

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
        tubes = A_lm / (np.pi*self.Di*self.L)

        return T_lm, A_lm, Q, int(tubes)

    def sizeHTU(self, basis, slices, m, U):
        """This function gives and estimation of the required heat transfer area of the heat exchanger using the heat transfer units method.
        This method makes use of enthalpy data from NIST, a number of slices are defined and the area is approximated as linear across these slices."""
        
        self.hotFluid.m = m
        self.U = U
        
        if slices == 0:
            return 0, 0
        dt = (self.coldFluid.To - self.coldFluid.Ti)/slices
        coldTs = [self.coldFluid.Ti]
        coldHs = [self.coldFluid.lookup('temp', self.coldFluid.Ti)]
        Tx = self.coldFluid.Ti + dt
        
        while coldTs[-1] <= self.coldFluid.To-dt:
            coldTs.append(Tx)
            coldHs.append(self.coldFluid.lookup('temp', Tx))
            Tx += dt

        Qs = []
        hotTs = [self.hotFluid.To]
        for i in range(1, len(coldHs)):
            Q = (coldHs[i] - coldHs[i-1])*self.coldFluid.m*1000
            Qs.append(Q)
            hotTs.append((Q/(self.hotFluid.m*self.hotFluid.Cp)+hotTs[-1]))
        
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
        
        tubes = sum(As) / (np.pi*self.Di*self.L)

        return sum(As)