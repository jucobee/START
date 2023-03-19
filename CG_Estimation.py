import numpy as np
import math

'''
Weight categories:

wing
horizontal tail
vertical tail
fuselage
engine
crew
fuel
battery
passengers
baggage/cargo
nose landing gear
main landing gear

'''
MTOW = 57006
# Number of pilots
pilots = 2
# Number of attendants
attend = 1
# Total crew
crew = pilots + attend
# Number of passengers
passengers = 50
# Weight of each crew member in lbs
wt_crew = 190
# Weight of each passenger in lbs
wt_passengers = 200
# Weight of baggage for each crew member in lbs
wt_crew_baggage = 30
# Weight of baggage for each passenger in lbs
wt_pass_baggage = 40
diam = 9


Wcrew = wt_crew * crew  # Total weight of crew
Wpass = passengers * wt_passengers  # Total weight of passengers
Wbaggage = (wt_crew_baggage * crew) + (wt_pass_baggage * passengers)  # Total weight of baggage in hold
Wfuel = MTOW * 0.11  # Fuel weight
Wbattery = MTOW * 0.09  # Battery weight
gas_turb = (((5950 / 2)**0.9306) * 10**(-0.1205)) * 2  # Total gas turbine engine weight
EM = (5950 / (5.22*1.34102209/2.20462262)) * 2  # Total electric motor weight
Wengine = 2.575 * (((gas_turb + EM)/2)**0.922) * 2 # TOTAL ENGINE WEIGHT


Sw = 826.134   # Wing area
bw = 115.76
Wfw = Wfuel  # Weight of fuel in wing
ARw = 16.22  # Aspect ratio of wing
Gammaw = 5 * (np.pi / 180)   # Wing sweep angle
lambdaw = 0.4 # Wing taper ratio
tcw = 0.16    # Thickness to chord ratio of wing root 
Nz = 2.458 * 1.5    # Ultimate load factor; 1.5 x limit load factor
Wdg = MTOW  # Design gross weight
q = (0.0343 * (590.733 ** 2)) / 2   # Dynamic pressure at cruise
Scsw = 0.2 * Sw

Wwing = 0.0051 * ((Wdg * Nz)**0.758) * (Sw**0.649) * (ARw**0.5) * (tcw**-0.4) * ((1+lambdaw)**0.1) * ((np.cos(Gammaw))**-1) * (Scsw**0.1) * 0.82

Sht = 94.19  # Area of horizantle tail
Gammaht = 16 * (np.pi / 180)  # Sweep angle of horizontal tail
lambdah = 0.4  # Taper ratio of horizontal tail
tch = 0.14      # Thickness to chord ratio of horizontal tail root
ARh = 4.4      # Aspect ratio of horizontal tail
Fw = 4.5
bh = 20.36
Lt = 41.71
Ky = 0.3 * Lt
Se = 0.1 * Sht
Wht = 0.0379 * (1.143) * ((1+(Fw/bh))**-0.25) * (Wdg**0.639) * (Nz**0.1) * (Sht**0.75) * (Lt**-1) * (Ky**0.704) * ((np.cos(Gammaht))**-1) * (ARh**0.166) * ((1+(Se/Sht))**0.1) * 0.83

Svt = 146.09  # Area of vertical tail
Gammavt = 30 * (np.pi / 180)  # Sweep angle of vertical tail
lambdavt = 0.8 # Taper ratio of vertical tail
tcv = 0.14  # Thickness to chord ratio of vertical tail root
ARvt = 1.127 # Aspect ratio of vertical tail
Wvt = 0.0026 * (2**0.225) * (Wdg**0.556) * (Nz**0.536) * (Lt**-0.5) * (Svt**0.5) * (Lt**0.875) * ((np.cos(Gammavt))**-1) * (ARvt**0.35) * (tcv**-0.5) * 0.83

Lt = 40 + 1.5  # Tail length; wing quarter-MAC to tail quarter-MAC, ft
L = 79   # Fuselage structural length, ft
D = 0.5    # Fuselage structural depth, ft
Sf = 1775.85   # Fuselage wetted area, ft^2
Vpr = 3919.81   # Volume of pressurized area
Wpress = 11.9 + (Vpr * 8)**0.271
Kd = 1.06
Klg = 1.12
Kws = 0.75 * ((1+2*lambdaw)/(1+lambdaw))*(bw*np.tan(Gammaw/L))

Wfusel = 0.3280 * (Kd) * (Klg) * ((Wdg * Nz)**0.5) * (L**0.25) * (Sf**0.302) * ((1+Kws)**0.04) * ((L/D)**0.1) * 0.9

Nl = 3.8 * 1.5  # ultimate landing load factor
Wl = MTOW - (0.9 * Wfuel)   # Landing design gross weight
Lm = 60  # Length of main landing gear, in
Ln = 54  # Lenght of nose landing gear, in
Nmw = 8
Nnw = 2
Nmss = 4
Vstall = 141

W_mainlanding = 0.0106 * (Wl**0.888) * (Nl**0.25) * (Lm**0.4) * (Nmw**0.321) * (Nmss**-0.5) * (Vstall ** 0.1)
W_noselanding = 0.032 * (Wl**0.646) * (Nl**0.2) * (Ln**0.5) * (Nnw**0.45)


# Xcg values in feet measured from leading edge of wing(Calculated if leading edge of wing moved forward by 2.1ft)
wingXcg = 5.41 * 0.25
fuelXcg = 5.41 * 0.35
passengersXcg = 6.27 + 2.1
crewXcg = -22.25 + 2.1
baggageXcg = 20 + 2.1
batteryXcg = 5.41*0.35
engineXcg = 0.05
horizontalXcg = 44.59 + 2.1
verticalXcg = 33.3375 + 2.1
noselandingXcg = -20 + 2.1
mainlandingXcg = 5 + 2.1
fuselageXcg = 3.55 + 2.1


sum1 = (Wwing * wingXcg) + (Wfuel * fuelXcg) + (Wpass * passengersXcg) + (Wcrew * crewXcg) + (Wbaggage * baggageXcg) + (Wbattery * batteryXcg) + (Wengine * engineXcg) + (Wht * horizontalXcg) + (Wvt * verticalXcg) + (W_noselanding * noselandingXcg) + (W_mainlanding * mainlandingXcg) + (Wfusel * fuselageXcg)
sum2 = Wwing + Wfuel + Wpass + Wcrew + Wbaggage + Wbattery + Wengine + Wht + Wvt + W_noselanding + W_mainlanding + Wfusel
XCG = sum1 / sum2
print('Center of gravity from wing LE: {} ft'.format(XCG))
print(' ')
print(Wwing)
print(Wfuel)
print(Wpass)
print(Wcrew)
print(Wbaggage)
print(Wbattery)
print(Wengine)
print(Wht)
print(Wvt)
print(W_noselanding)
print(W_mainlanding)
print(Wfusel)
print(' ')
print(wingXcg)
print(fuelXcg)
print(passengersXcg)
print(crewXcg)
print(baggageXcg)
print(batteryXcg)
print(engineXcg)
print(horizontalXcg)
print(verticalXcg)
print(noselandingXcg)
print(mainlandingXcg)
print(fuselageXcg)