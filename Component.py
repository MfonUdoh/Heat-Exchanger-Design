class Component():
    def __init__(self, Cp, m, Rho, Ti, To):
        self.Cp = float(Cp) # Heat Capacity, J/kg
        self.m = float(m) # Mass Flowrate, kg/s
        self.Rho = float(Rho) # Density, kg/m3
        self.Ti = float(Ti) # Hot Inlet Temperature, K
        self.To = float(To) # Hot Oulet Temperature, K
        self.TH = [] # Temperature-Enthalpy data for the component in a nx2 array

    def lookup(self, prop, value):
        """Function uses the Temperature-Enthalpy data to lookup the corresponding enthalpy\\
        for a given temperature or vice-versa.\\
        prop = input property type; 'temp' or 'enth'\\
        value = value of input property"""

        min = []
        if prop == 'temp':
            ref = 1
        elif prop == 'enth':
            ref = 0
        else:
            print('invalid lookup')
        
        for i in range(self.TH):
            if min == [] or value - self.TH[i][ref] < min[1]:
                min = ([i, value - self.TH[i][ref]])
        
        return min[1]

