class Component():
    def __init__(self, Cp, m, Rho, Ti, To):
        self.Cp = float(Cp) # Heat Capacity, J/kg
        self.m = float(m) # Mass Flowrate, kg/s
        self.Rho = float(Rho) # Density, kg/m3
        self.Ti = float(Ti) # Hot Inlet Temperature, K
        self.To = float(To) # Hot Oulet Temperature, K
        self.TH = [] # Temperature-Enthalpy data for the component in a nx2 array

    def add_data(self, datafile):
        txt = open(str(datafile+".txt"), "r")
        txtData = txt.read()
        data = txtData.split()

        counter = 0
        for i in data:
            if counter == 0:
                temp = i
            if counter == 5:
                enth = i
                self.TH.append([temp, enth])
            if counter < 13:
                counter += 1
            else:
                counter = 0

    def lookup(self, prop, value):
        """Function uses the Temperature-Enthalpy data to lookup the corresponding enthalpy\\
        for a given temperature or vice-versa.\\
        prop = input property type; 'temp' or 'enth'\\
        value = value of input property"""

        min = []
        if prop == 'temp':
            ref = 0
        elif prop == 'enth':
            ref = 1
        else:
            print('invalid lookup')
        for i in range(len(self.TH)):
            if min == [] or float(value - float(self.TH[i][ref]))**2 < min[1]:
                min = [i, float(value - float(self.TH[i][ref]))**2]
        minVal = min[0]

        return self.TH[minVal]

