class Component():
    def __init__(self, Cp, m, Rho, Ti, To):
        self.Cp = float(Cp) # Heat Capacity, J/kg
        self.m = float(m) # Mass Flowrate, kg/s
        self.Rho = float(Rho) # Density, kg/m3
        self.Ti = float(Ti) # Hot Inlet Temperature, K
        self.To = float(To) # Hot Oulet Temperature, K
        self.TH = [] # Temperature-Enthalpy data for the component in a nx2 array

    def add_data(self, datafile):
        """Use this function to add data from NIST in a delimited table txt format
        datafile = the name of the text file that contains the data"""

        txt = open(str(datafile+".txt"), "r")
        txtData = txt.read()
        data = txtData.split()
        for i in  range(30): # Removes the header from the NIST data
            data.pop(0)
        counter = 0
        for i in data:
            if counter == 0: # Selects the temperature column from the NIST data
                temp = i
            if counter == 5: # Selects the enthalpy column from the NIST data
                enth = i
                self.TH.append([temp, enth])
            if counter < 13: # Loops back at the end of the NIST data table
                counter += 1
            else:
                counter = 0

    def lookup(self, prop, value):
        """Function uses the NIST data to lookup the corresponding property data for input value.
        prop = input property type; 'temp' or 'enth'
        value = value of input property"""

        min = []
        if prop == 'temp':
            ref = 0
        elif prop == 'enth':
            ref = 1
        else:
            print('invalid lookup')

        for i in range(len(self.TH)): # Loop finds the closest value in the data to the input valua
            if min == [] or float(value - float(self.TH[i][ref]))**2 < min[1]:
                min = [i, float(value - float(self.TH[i][ref]))**2]
        minVal = min[0]
        if ref == 0:
            # print("Found reference for {} K, gives {} kJ/kg".format(self.TH[minVal][0], self.TH[minVal][1]))
            return float(self.TH[minVal][1])
        if ref == 1:
            # print("Found reference for {} kJ/kg, gives {} K".format(self.TH[minVal][0], self.TH[minVal][1]))
            return float(self.TH[minVal][0])

