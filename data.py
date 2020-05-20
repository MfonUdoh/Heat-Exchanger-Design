from Component import Component
from HEX import *

########################
### Fluid Properties ###
########################

### Air ###

Ti = 298.0
To = 293.0
Cp = 1012
m = 2.03576
Rho = 1.184
mu = 0.00001983
mu_w = 0.00001983
R_f = 0.0001
k = 0.026055

air = Component(Cp, m, Rho, Ti, To, mu, mu_w, R_f, k)

### Nitrogen ###

Ti = 93.0
To = 288.0
Cp = 1932.8
m = 0.02687
Rho = 183.6
mu = 0.0000234342
mu_w = 0.000012352
R_f = 0.0001
k = 0.034983363

nitrogen = Component(Cp, m, Rho, Ti, To, mu, mu_w, R_f, k)
nitrogen.add_data("nitrogen40bar")

######################
### HEX Properties ###
######################

### HEX 1 ###

name = 'Heat Exchanger 1 (E-3)'
hexType = 'tube'
coldFluid = nitrogen
hotFluid = air
U = 120
Di = 0.02
L = 0.25
basis = 'hot'
correctionFactor = 1

HEX1 = STHE(name, hexType, coldFluid, hotFluid, U, basis, correctionFactor)
HEX1.define(L, Di)

### HEX 2 ###

name = 'Heat Exchanger 1 (E-3)'
hexType = 'plate'
coldFluid = nitrogen
hotFluid = air
U = 30
basis = 'hot'
correctionFactor = 1
W = 0.4
L = 0.8
D_port = 0.1
angle = 65
phi = 1.2
passes = 1
tp = 0.008
b = 0.005
k_plate = 205

HEX2 = PHE(name, hexType, coldFluid, hotFluid, U, basis, correctionFactor)
HEX2.define(L, W, angle, phi, passes, tp, b, D_port, k_plate)

### HEX 3 ###

name = 'Heat Exchanger 1 (E-3)'
hexType = 'plate'
coldFluid = nitrogen
hotFluid = air
U = 30.31
basis = 'hot'
correctionFactor = 0.95
W = 0.3
L = 0.7
D_port = 0.1
angle = 65
phi = 1.2
passes = 1
tp = 0.002
b = 0.005
k_plate = 205

HEX3 = PHE(name, hexType, coldFluid, hotFluid, U, basis, correctionFactor)
HEX3.define(L, W, tp, phi, passes, angle, b, D_port, k_plate)