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


### Fuel Fractions ###
# Naming convention: W_{flight segment} = Weight at the end of 'flight segment'

W_initial = 55030               # initial weight at start of taxi
PSFC_hp = 0.483                 # Power Specific Fuel Consumption in lbm/(hp*hr)
PSFC = (0.483) / (3600 * 550)   # lbm/(fpf*s)
max_takeoff_power = 6000        # Carlos told me this value
eta_p = 0.8                     # Propeller Efficiency of 0.8
g = 32.17                       # Force of gravity in ft/s^2

## Taxi ##
idle_time = 15 * 60                     # 15 minutes converted to seconds?
idle_power = max_takeoff_power * 0.05   # 5% of max takeoff power
taxi_Wfraction = 1 - idle_time * (PSFC / eta_p) * (idle_power / W_initial)
W_taxi = taxi_Wfraction * W_initial

## Takeoff ##
# Use above equation with 1 min. at maximum takeoff thrust (or power).
# Or use the takeoff analysis shown in Chapter 17 of Raymer and break this phase into several constant-speed segments.
takeoff_time = 60                     # 1 minute converted to seconds?
takeoff_Wfraction = 1 - idle_time * (PSFC / eta_p) * (max_takeoff_power / W_taxi)
W_takeoff = takeoff_Wfraction * W_taxi

## Climb ##
RoC = 1800/60                   # rate of climb  1800 ft/min converted to ft/s

W_climb = 50000                 # weight at the end of climb/start of cruise in lbs

## Cruise (multi-segment approach) ##
# cruise range is not 1000nmi, we need to change this value
R = 1000*6076.11549             # Cruise range of 1000 nmi converted to ft
h = 25000                       # Cruise altitude 25000 ft
LoD = 17                        # Lift to drag ratio depending on aircraft design
E = 45*60                       # Assume endurance of 45 min converted to seconds

### need to change this to density at 25,000 ft
rho = 10.66e-4                  # air density at cruise altitude of 28,000 ft
V_inf = 275*1.6878098571        # cruise airspeed 275 kts converted to ft/s
S_ref = 826.134                 # reference area (wing area) in ft^2

#### stealing these values from drag polar estimate, may need to change
c_f = 0.0026                    # skin friction coefficient, Raymer 12.3
C_D0 = c_f * 5                  # 
AR = 18.44588                   # aspect ratio, from openVSP model
e_v = 0.80                      # span efficiency factor
K = 1 / (np.pi * AR * e_v)   

def getCruiseWfrac(num_segments):
    seg_range = R / num_segments                # range of each segment
    W = np.empty(num_segments + 1)              # Weight array  
    W[0] = W_climb                        # Weight at start of cruise (AKA weight at end of climb)
    seg_Wfraction = np.empty(num_segments)      # Weight fraction of each segment
    cruise_Wfraction = np.empty(num_segments+1) # Total weight fraction
    cruise_Wfraction[0] = 1.0                   # Initialize at 1.0

    for i in range(num_segments):
        # Breguet equation for each segment
        C_L = 2*W[i] / (rho * V_inf**2 * S_ref)
        LoD = C_L / (C_D0 + K*C_L**2)
        seg_Wfraction[i] = np.exp(-(seg_range * PSFC) / (eta_p * LoD))
        W[i+1] = seg_Wfraction[i] * W[i] # modify weight value for next segment

        # Total cruise weight fraction is reduced by amount of current segment's weight fraction
        cruise_Wfraction[i+1] = cruise_Wfraction[i] - (1 - seg_Wfraction[i])
        #print(cruise_Wfraction[i+1])
    
    return cruise_Wfraction[:-1]

for seg in [2,11,21,101]:
    cruise_range = np.linspace(0,R / 6076.11549,seg)
    plt.plot(cruise_range, getCruiseWfrac(seg), label='{} segments'.format(seg-1), marker='.')

plt.legend(loc='best')
plt.title('Cruise Fuel Weight Fraction')
plt.xlabel('Cruise Range (nmi)')
plt.ylabel('Weight Fraction')
plt.show()

## Loiter ##

## Descent ##
# use previous methods based on statistics

## Landing ##
# use previous methods based on statistics


print('Fuel Fractions:')
print('Taxi: {}'.format(taxi_Wfraction))
print('Takeoff: {}'.format(takeoff_Wfraction))
# print('Climb: {}'.format(climb_Wfraction))
# print('Cruise: {}'.format(taxi_Wfraction))
# print('Loiter: {}'.format(loiter_Wfraction))
# print('Descent: {}'.format(descent_Wfraction))
# print('Landing: {}'.format(landing_Wfraction))