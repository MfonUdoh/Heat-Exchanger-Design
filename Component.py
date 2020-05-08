class Component():
    def __init__(self, Cp, m, Rho, Ti, To, mu, mu_w, R_f, k):
        self.Cp = float(Cp) # Heat Capacity, J/kg
        self.m = float(m) # Mass Flowrate, kg/s
        self.rho = float(Rho) # Density, kg/m3
        self.Ti = float(Ti) # Hot Inlet Temperature, K
        self.To = float(To) # Hot Oulet Temperature, K
        self.mu = float(mu) # Viscosity, Pa s
        self.mu_w = float(mu_w) # Viscosity at wall
        self.R_f = float(R_f) # Fouling factors
        self.k = float(k) # Conductivity
        self.data = {
            'enth' : [],
            'rho' : [],
            'Cp' : [],
            'mu' : [],
            'k' : []
        } # Temperature data for the component in a nx2 array
        self.Tdistro = [] # Temperature distribution across the Heat Exchanger

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
            if counter == 2: # Selects the enthalpy column from the NIST data
                rho = i
                self.data['rho'].append([float(temp), float(rho)])
            if counter == 5: # Selects the enthalpy column from the NIST data
                enth = i
                self.data['enth'].append([float(temp), float(enth)])
            if counter == 8: # Selects the enthalpy column from the NIST data
                Cp = i
                self.data['Cp'].append([float(temp), float(Cp)*1000])
            if counter == 11: # Selects the enthalpy column from the NIST data
                mu = i
                self.data['mu'].append([float(temp), float(mu)/1000000])
            if counter == 12: # Selects the enthalpy column from the NIST data
                k = i
                self.data['k'].append([float(temp), float(k)])
            if counter < 13: # Loops back at the end of the NIST data table
                counter += 1
            else:
                counter = 0

    def lookup(self, prop, value):
        """Function uses the NIST data to lookup the corresponding property data for input value.
        prop = input property type; 'temp' or 'enth'
        value = value of input property"""

        for i in range(len(self.data[prop])-1): # Loop finds the closest value in the data to the input value
            x1 = self.data[prop][i][0]
            x2 = self.data[prop][i+1][0]
            y1 = self.data[prop][i][1]
            y2 = self.data[prop][i+1][1]
            if value - x1 >= 0 and value - x2 <= 0:
                gradient = (y2 - y1) / (x2 - x1)
                result = y1 + (value-x1)*gradient
        
        return result

