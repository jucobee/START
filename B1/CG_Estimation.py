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
bw = 115.76 # Wing span
Wfw = Wfuel  # Weight of fuel in wing
ARw = 16.22  # Aspect ratio of wing
Gammaw = 5 * (np.pi / 180)   # Wing sweep angle
lambdaw = 0.4 # Wing taper ratio
tcw = 0.16    # Thickness to chord ratio of wing root 
Nz = 2.458 * 1.5    # Ultimate load factor; 1.5 x limit load factor
Wdg = MTOW  # Design gross weight
q = (0.0010651 * (590.733 ** 2)) / 2   # Dynamic pressure at cruise
Scsw = 0.2 * Sw

Wwing = 0.0051 * ((Wdg * Nz)**0.557) * (Sw**0.649) * (ARw**0.5) * (tcw**-0.4) * ((1+lambdaw)**0.1) * ((np.cos(Gammaw))**-1) * (Scsw**0.1) * 0.82

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


Kng = 1 # 1.017 for pylon-mounted nacelle; = 1.0 otherwise
NLt = 20.5 # nacelle length, ft
Nw = 2.5 # nacelle width, ft
Wec = Wengine + 0 # weight of engine and contents, lb (per nacelle)
Nen = 2 # number of engines (total for aircraft)
Sn = 553.299/2 # nacelle wetted area, ft2
W_nacellegroup = 0.6724*Kng*NLt**.1*Nw**0.294*Nz**0.119*Wec**0.611*Nen**0.984*Sn**0.224

Lec = 30 #routing distance from engine front to cockpit,ft
W_enginecontrols = 5*Nen+0.80*Lec

Wen = Wengine + 0 # engine weight, each, lb
W_starter = 49.19*(Nen*Wen/1000)**0.541

Vt= 125.036*7.48051948 # total fuel volume, gal
Vi= 125.036*7.48051948 # integral tanks volume, gal
Vp= 0 # self-sealing tanks, gal
Nt= 4 # number of fuel tanks
W_fuelsystem = 2.405*Vt**.606*(1+Vi/Vt)**-1*(1+Vp/Vt)*Nt**0.5

Nf=7 # number of separate functions performed by surface controls, including rudder, aileron, elevator, flaps, spoiler, and speed brakes
Nm=2 # number of surface controls driven by mechanical actuation instead of hydraulics
Scs=200 # total control surface area, ft2
Iyaw=1 # yawing moment of inertia, lb*ft2
W_flightcontrols = 145.9*Nf**0.554*(1+Nm/Nf)**-1*Scs**.2*(Iyaw*10**-16)**.07

WAPUuninstalled= 115 # weight of APU, uninstalled
W_APUinstalled = 2.2*WAPUuninstalled

Kr= 1 # 1.133 if reciprocating engine; = 1.0 otherwise
Ktp= 0.793 # 0.793 if turboprop; = 1 .0 otherwise
Nc= 3 # number of crew 
Lf= 79 # total fuselage length
Bw= 115.76 # wingspan
W_instruments = 4.509*Kr*Ktp*Nc**.541*Nen*(Lf+Bw)**0.5

W_hydraulics=0.2673*Nf*(Lf+Bw)**.937

Rkva=50 # system electrical rating, typically 40-60 for transports, kV · A 
La=80 # electrical routing distance, generators to avionics to cockpit, ft
Ngen=2 # number of generators (typically = Nen)
W_electrical=7.291*Rkva**0.782*La**.346*Ngen**.1

Wuav=1000 # uninstalled avionics weight, lb (typically = 800-1400 lb)
W_avionics=1.73*Wuav**.983

Wc=Wbaggage+0 # maximum cargo weight, lb
W_furnishings=0.0577*Nc**.1*Wc**.393*Sf**.75

Np=53 # number of personnel onboard (crew and passengers)
W_airconditioning=62.36*Np**.25*(Vpr/1000)**.604*Wuav**.1

W_antiice=.0002**Wdg

W_handlinggear=3.0*10**-4*Wdg


# Xcg values in feet measured from leading edge of wing(Calculated if leading edge of wing moved forward by 2.1ft)
wingXcg = 5.41 * 0.25   # At quarter chord of wing
fuelXcg = 5.41 * 0.35      # Fuel sits about a third of the way along the chord of the wing
passengersXcg = 4.8 # Passenger weight slightly behind wing LE
crewXcg = -4.77
baggageXcg = 15.69
batteryXcg = 5.41*0.55
engineXcg = 0.0
horizontalXcg = 48.17
verticalXcg = 41.854
noselandingXcg = -20.858
mainlandingXcg = 4.444
fuselageXcg = 6.007
nacelleXcg = 4.708    # Nacelle group cg sits almost level with the wing leading edge
engcontXcg = 10.021
starterXcg = 0.0
fuelsysXcg = 5.41 * 0.25
flightcontXcg = 10.021
APUxCG = 46.717
instrumentsXcg = -26.172
hydraulicsXcg = 22.3
electricalXcg = -0.805
avionicsXcg = -26.172
furnishingsXcg = 4.8
airconXcg = 3.461
antiiceXcg = 0
handlinggearXcg = 0

components = dict(zip(['Wwing ', ' Wfuel ', ' Wpass ', ' Wcrew ', ' Wbaggage ', ' Wbattery ', ' Wengine ', ' Wht ', ' Wvt ', ' Wfusel ', ' W_noselanding ', ' W_mainlanding ', 'W_nacellegroup ', ' W_enginecontrols ', ' W_starter ', ' W_fuelsystem ', ' W_flightcontrols ', ' W_APUinstalled ', ' W_instruments ', ' W_hydraulics ', ' W_electrical ', ' W_avionics ', ' W_furnishings ', ' W_airconditioning ', ' W_antiice ', ' W_handlinggear'],
                  [Wwing , Wfuel , Wpass , Wcrew , Wbaggage , Wbattery , Wengine , Wht , Wvt , Wfusel , W_noselanding , W_mainlanding ,W_nacellegroup , W_enginecontrols , W_starter , W_fuelsystem , W_flightcontrols , W_APUinstalled , W_instruments , W_hydraulics , W_electrical , W_avionics , W_furnishings , W_airconditioning , W_antiice , W_handlinggear]))
componentsXcg = dict(zip(['wingXcg','fuelXcg','passengersXcg','crewXcg','baggageXcg','batteryXcg','engineXcg','horizontalXcg','verticalXcg','noselandingXcg','mainlandingXcg','fuselageXcg','nacelleXcg','engcontXcg','starterXcg','fuelsysXcg','flightcontXcg','APUxCG','instrumentsXcg','hydraulicsXcg','electricalXcg','avionicsXcg','furnishingsXcg','airconXcg','antiiceXcg','handlinggearXcg'],
                         [wingXcg,fuelXcg,passengersXcg,crewXcg,baggageXcg,batteryXcg,engineXcg,horizontalXcg,verticalXcg,fuselageXcg,noselandingXcg,mainlandingXcg,nacelleXcg,engcontXcg,starterXcg,fuelsysXcg,flightcontXcg,APUxCG,instrumentsXcg,hydraulicsXcg,electricalXcg,avionicsXcg,furnishingsXcg,airconXcg,antiiceXcg,handlinggearXcg]))

# print(components)
MTOW = sum(components.values())
XCG = sum(np.array([*components.values()])*np.array([*componentsXcg.values()])) / sum(components.values())

print('MTOW: {} lbs'.format(MTOW))
print('Center of gravity from wing LE: {} ft'.format(XCG))
