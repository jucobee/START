from matplotlib import pyplot as plt
import numpy as np

pilots = 2              # Number of pilots
attend = 1              # Number of attendants
crew = pilots + attend  # Total crew
passengers = 50         # Number of passengers
W_crew = 190           # Weight of each crew member in lbs
W_passengers = 200     # Weight of each passenger in lbs
W_crew_baggage = 30    # Weight of baggage for each crew member in lbs
W_pass_baggage = 40    # Weight of baggage for each passenger in lbs

# Total payload weight; Total crew weight
W_payload = (passengers * (W_passengers + W_pass_baggage)) 
W_crew = crew * (W_crew + W_crew_baggage) 


### Fuel Fractions
# Climb

RoC = 1800/60                   # rate of climb  1800 ft/min converted to ft/s

W_startCruise = 50000 # weight at the start of cruise in lbs

# Cruise (multi-segment approach)
### cruise range is not 1000nmi, we need to change this value
R = 1000*6076.11549             # Cruise range of 1000 nmi converted to ft
h = 25000                       # Cruise altitude 25000 ft
eta_p = 0.8                     # Propeller Efficiency of 0.8
g = 32.17                       # Force of gravity in ft/s^2
LoD = 17                        # Lift to drag ratio depending on aircraft design
E = 45*60                       # Assume endurance of 45 min converted to seconds
PSFC_hp = 0.483                 # Power Specific Fuel Consumption in lbm/(hp*hr)
PSFC = (0.483) / (3600 * 550)   # lbm/(fpf*s)

### need to change this to density at 25,000 ft
rho = 10.66e-4                  # air density at cruise altitude of 28,000 ft
V_inf = 275*1.6878098571        # cruise airspeed 275 kts converted to ft/s
S_ref = 826.134                 # reference area (wing area) in ft^2

#### stealing these values from drag polar estimate, may need to change
c_f = 0.0026                    # skin friction coefficient, Raymer 12.3
C_D0 = c_f * 5                  # 
AR = 18.44588                   # aspect ratio, from openVSP model
e_v = 0.80                      # span efficiency factor
K = np.pi * AR * e_v           

def getFuelBurn(num_segments):
    seg_range = R / num_segments                # range of each segment
    T = np.empty(num_segments + 1)              # Thrust array  
    W = np.empty(num_segments + 1)              # Weight array  
    W[0] = W_startCruise                        # Weight at start of cruise (AKA weight at end of climb)
    seg_Wfraction = np.empty(num_segments)      # Weight fraction of each segment
    seg_Wfraction = np.empty(num_segments)      # Weight fraction of each segment
    cruise_fuelburn = np.empty(num_segments+1)  # Total fuel consumed
    seg_fuelburn = np.empty(num_segments)       # Fuel consumed of each segment

    for i in range(num_segments):
        # Breguet equation for each segment
        C_L = 2*W[i] / (rho * V_inf**2 * S_ref) # Lift varies based on weight loss from fuel burn
        T[i] = (W[i]/C_L) * (C_D0+K*C_L**2) # Induced drag is reduced so thrust is reduced

        seg_fuelburn[i] = -PSFC*T[i]*seg_range/V_inf
        cruise_fuelburn[i+1] = cruise_fuelburn[i] - seg_fuelburn[i]

        seg_Wfraction[i] = np.exp(-(seg_range * PSFC) / (V_inf * LoD))
        W[i+1] = seg_Wfraction[i] * W[i] # modify weight value for next segment
    
    return T[:-1], cruise_fuelburn[:-1]

for seg in [2,11,21,101]:
    cruise_range = np.linspace(0,1000,seg)
    T, fuelburn = getFuelBurn(seg)
    plt.plot(cruise_range, fuelburn, label='{} segments'.format(seg-1), marker='.')

plt.legend(loc='best')
plt.title('Fuel Burn Consumption')
plt.xlabel('Cruise Range km')
plt.ylabel('Fuel Burn Consumption lbs')
plt.show()

print(getFuelBurn(101)[1][-1]/1000/0.539957/6.99)

for seg in [2,11,21,101]:
    cruise_range = np.linspace(0,1000,seg)
    T, fuelburn = getFuelBurn(seg)
    plt.plot(cruise_range, T, label='{} segments'.format(seg-1), marker='.')

plt.legend(loc='best')
plt.title('Fuel Burn Consumption')
plt.xlabel('Cruise Range km')
plt.ylabel('Fuel Burn Consumption lbs')
plt.show()