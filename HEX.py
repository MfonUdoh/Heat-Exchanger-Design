import numpy as np

class HeatExchanger():
    def __init__(self, config, cold, hot, U, Di, L):
        self.type = config
        self.coldFluid = cold
        self.hotFluid = hot
        self.U = float(U) # Overall Heat Transfer Coeff, W/m2K
        self.Di = float(Di) # Internal Diameter, m
        self.L = float(L) # Length of tubes, m

    def sizeLMTD(self, basis):
        dT1 = self.hotFluid.Ti - self.coldFluid.To
        dT2 = self.hotFluid.To - self.coldFluid.Ti
        T_lm = (dT1 - dT2)/np.log(dT1/dT2)
        if basis == 'hot':
            Q = self.hotFluid.m * self.hotFluid.Cp * (self.hotFluid.Ti - self.hotFluid.To)
        elif basis == 'cold':
            Q = self.coldFluid.m * self.coldFluid.Cp * (self.coldFluid.To - self.coldFluid.Ti)
        else:
            print('Invalid basis')
        
        A_lm = Q/(self.U*T_lm)

        tubes = A_lm / (np.pi*self.Di*self.L)

        return T_lm, A_lm, Q, tubes

    def sizeHTU(self, basis, slices):

        self.coldFluid.To
        self.coldFluid.Ti
        T_lm = (dT1 - dT2)/np.log(dT1/dT2)
        if basis == 'hot':
            Q = self.hotFluid.m * self.hotFluid.Cp * (self.hotFluid.Ti - self.hotFluid.To)
        elif basis == 'cold':
            Q = self.coldFluid.m * self.coldFluid.Cp * (self.coldFluid.To - self.coldFluid.Ti)
        else:
            print('Invalid basis')
        
        A_lm = Q/(self.U*T_lm)

        tubes = A_lm / (np.pi*self.Di*self.L)

        return A_lm, Q, tubes