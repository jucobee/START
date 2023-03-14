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
MTOW = 56990
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


Wcrew = wt_crew * crew  # Total weight of crew
Wpass = passengers * wt_passengers  # Total weight of passengers
Wbaggage = (wt_crew_baggage * crew) + (wt_pass_baggage * passengers)  # Total weight of baggage in hold
Wfuel = MTOW * 0.11  # Fuel weight
Wbattery = MTOW * 0.09  # Battery weight
gas_turb = (((5950 / 2)**0.9306) * 10**(-0.1205)) * 2  # Total gas turbine engine weight
EM = (5950 / (5.22*1.34102209/2.20462262)) * 2  # Total electric motor weight
Wengine = 2.575 * (((gas_turb + EM)/2)**0.922) * 2 # TOTAL ENGINE WEIGHT


Sw = 826.134   # Wing area
Wfw = Wfuel  # Weight of fuel in wing
ARw = 16.22  # Aspect ratio of wing
Gammaw = 5   # Wing sweep angle
lambdaw = 0.4 # Wing taper ratio
tcw =     # Thickness to chord ratio of wing root
Nz = 2.458 * 1.5    # Ultimate load factor; 1.5 x limit load factor
Wdg = MTOW  # Design gross weight
q = (0.0343 * (590.733 ** 2)) / 2   # Dynamic pressure at cruise

Wwing = 0.036 * (Sw**0.758) * (Wfw**0.0035) * ((ARw / (np.cos(Gammaw))**2)**0.6) * (q**0.006) * (lambdaw**0.04) * (((100 * tcw) / np.cos(Gammaw))**-0.3) * ((Nz * Wdg)**0.49) * 0.82

Sht = 94.19  # Area of horizantle tail
Gammaht = 16  # Sweep angle of horizontal tail
lambdah = 0.4  # Taper ratio of horizontal tail
tch =       # Thickness to chord ratio of horizontal tail root
ARh = 4.4      # Aspect ratio of horizontal tail
Wht = (0.016 * (Nz * Wdg)**0.414) * (q**0.168) * (Sht**0.896) * (((100 * tch) / np.cos(Gammaht))**-0.12) * (((ARh) / np.cos(Gammaht)**2)**0.043) * (lambdah**-0.02) * 0.83

Svt = 146.09  # Area of vertical tail
Gammavt = 30  # Sweep angle of vertical tail
lambdavt = 0.8 # Taper ratio of vertical tail
tcv =   # Thickness to chord ratio of vertical tail root
ARvt = 1.127 # Aspect ratio of vertical tail
Wvt = 0.073 * (1 + 0.2) * ((Nz * Wdg)**0.376) * (q**0.122) * (Svt**0.873) * (((100 * tcv) / np.cos(Gammavt))**-0.49) * (((ARvt) / np.cos(Gammavt)**2)**0.357) * (lambdavt**0.039) * 0.83

Lt =    # Tail length; wing quarter-MAC to tail quarter-MAC, ft
L = 79   # Fuselage structural length, ft
D =     # Fuselage structural depth, ft
Sf =    # Fuselage wetted area, ft^2
Vpr =   # Volume of pressurized area
Wpress = 11.9 + (Vpr * 8)**0.271

Wfusel = ((0.052 * (Sf**1.086) * ((Nz * Wdg)**0.177) * (Lt**-0.051) * ((L/D)**-0.072) * (q**0.241)) + Wpress) * 0.9

Nl = 3.8 * 1.5  # ultimate landing load factor
Wl = MTOW - (0.9 * Wfuel)   # Landing design gross weight
Lm = 60  # Length of main landing gear, in
Ln = 54  # Lenght of nose landing gear, in

W_mainlanding = 0.095 * (Nl * Wl)**0.768 * (Lm / 12)**0.409 * 0.95
W_noselanding = 0.125 * (Nl * Wl)**0.566 * (Ln / 12)**0.845 * 0.95


# Xcg values in feet measured from leading edge of wing
wingXcg = 5.41 * 0.3
fuelXcg = 5.41 * 0.2
passengersXcg = 
crewXcg = 
baggageXcg = 
batteryXcg = 
engineXcg = 
horizontalXcg = 
verticalXcg = 
noselandingXcg = 
mainlandingXcg = 
fuselageXcg = 


sum1 = (Wwing * wingXcg) + (Wfuel * fuelXcg) + (Wpass * passengersXcg) + (Wcrew * crewXcg) + (Wbaggage * baggageXcg) + (Wbattery * batteryXcg) + (Wengine * engineXcg) + (Wht * horizontalXcg) + (Wvt * verticalXcg) + (W_noselanding * noselandingXcg) + (W_mainlanding * mainlandingXcg) + (Wfusel * fuselageXcg)
sum2 = Wwing + Wfuel + Wpass + Wcrew + Wbaggage + Wbattery + Wengine + Wht + Wvt + W_noselanding + W_mainlanding + Wfusel
XCG = sum1 / sum2
print('Center of gravity from wing LE: {} ft'.format(XCG))