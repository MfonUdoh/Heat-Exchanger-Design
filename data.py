from Component import Component
from HEX import HeatExchanger

########################
### Fluid Properties ###
########################

### Air 1 ###

Ti = 298
To = 293
Cp = 1003
m = 2.03576
Rho = 1.22

air1 = Component(Cp, m, Rho, Ti, To)

### Air 2 ###

Ti = 298
To = 293
Cp = 1003
m = 1.44700
Rho = 1.22

air2 = Component(Cp, m, Rho, Ti, To)

### Nitrogen ###

Ti = 93
To = 288
Cp = 2000
m = 0.02687
Rho = 100

nitrogen = Component(Cp, m, Rho, Ti, To)
nitrogen.add_data("nitrogen40bar")

### Hot Refrigerant ###

Ti = 344
To = 293
Cp = 1003 
m = 0.04743
Rho = 1.22

refHot = Component(Cp, m, Rho, Ti, To)

### Cold Refrigerant ###

Ti = 253
To = 283
Cp = 1003
m = 0.04743
Rho = 1.22

refCold = Component(Cp, m, Rho, Ti, To)

### Heat Exchanger Fluid ###

Ti = 283
To = 303
Cp = 3320
m = 0.12536
Rho = 1190

hef = Component(Cp, m, Rho, Ti, To)

### Ammonia ###

Ti = 258
To = 273
Cp = 3320
m = 0.255
Rho = 1190

ammonia = Component(Cp, m, Rho, Ti, To)

### Air3 ###

Ti = 293
To = 291
Cp = 1003
m = 0.3675
Rho = 1190

air3 = Component(Cp, m, Rho, Ti, To)

######################
### HEX Properties ###
######################

### HEX 1 ###

name = 'Heat Exchanger 1 (E-3)'
hexType = 'tube'
coldFluid = nitrogen
hotFluid = air1
U = 120
Di = 0.02
L = 0.25

HEX1 = HeatExchanger(name, hexType, coldFluid, hotFluid, U, Di, L)

### HEX 2 ###

name = 'Heat Exchanger 2'
hexType = 'tube'
coldFluid = hef
hotFluid = refHot
U = 300
Di = 0.1
L = 1

HEX2 = HeatExchanger(name, hexType, coldFluid, hotFluid, U, Di, L)

### HEX 3 ###

name = 'Heat Exchanger 3'
hexType = 'tube'
coldFluid = refCold
hotFluid = air2
U = 170
Di = 0.05
L = 0.5

HEX3 = HeatExchanger(name, hexType, coldFluid, hotFluid, U, Di, L)