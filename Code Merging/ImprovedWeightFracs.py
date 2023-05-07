from matplotlib import pyplot as plt
import numpy as np
from dragpolar import dragpolar

def ImprovedWeightFracs(MTOW):
    #*** stealing these values from drag polar estimate, may need to change
    c_f = 0.0026                    # skin friction coefficient, Raymer 12.3
    C_D0 = c_f * 5                  # 
    AR = 16.22                   # aspect ratio, from openVSP model
    e_v = 0.80                      # span efficiency factor
    K = 1 / (np.pi * AR * e_v)   

    ############ Fuel Fractions ################
    # Naming convention: W_{flight segment} = Weight at the *END* of 'flight segment'

    W_initial = MTOW               # initial weight at start of taxi
    PSFC_hp = (1.80371945e-07) * (3600 * 550)                 # Power Specific Fuel Consumption in lbm/(hp*hr)
    PSFC = 1.80371945e-07  # lbm/(fpf*s)
    max_takeoff_power = 6000        # Carlos told me this value
    eta_p = 0.8                     # Propeller Efficiency of 0.8
    g = 32.17                       # Force of gravity in ft/s^2

    ##### Taxi #####
    idle_time = 15 * 60                     # 15 minutes converted to seconds?
    idle_power = max_takeoff_power * 0.05   # 5% of max takeoff power
    taxi_Wfraction = 1 - idle_time * (PSFC / eta_p) * (idle_power / W_initial)
    W_taxi = taxi_Wfraction * W_initial

    ##### Takeoff #####
    takeoff_time = 60                     # 1 minute converted to seconds?
    takeoff_Wfraction = 1 - takeoff_time * (PSFC / eta_p) * (max_takeoff_power / W_taxi)
    W_takeoff = takeoff_Wfraction * W_taxi

    ##### Climb #####
    RoC = 1800/60                   # rate of climb  1800 ft/min converted to ft/s
    S_ref = 826.134                 # reference area (wing area) in ft^2
    rho = 10.66e-4                  #* density should be changed
    H = 25000                       # final altitude of 25,000 ft

    def getClimbWfrac(num_segments):
        seg_h = H / num_segments                # range of each segment
        W = np.empty(num_segments + 1)              # Weight array  
        W[0] = W_takeoff                        # Weight at start of climb (AKA weight at end of takeoff)
        seg_Wfraction = np.empty(num_segments)      # Weight fraction of each segment
        climb_Wfraction = np.empty(num_segments + 1) # Total weight fraction
        climb_Wfraction[0] = 1.0                   # Initialize at 1.0
        eta_GB = 0.96 # de Vries
        eta_GT = 0.40 # de Vries, 2035
        eta_PM = 0.99 # de Vries
        eta_EM1 = 0.97  # de Vries
        e_f = 43.15*(1e6/1.3558179483314/0.06852177) 
        e_b= 500*(3600/1.3558179483314/0.06852177) # fpf/slug
        hybrid_ratio = 0.36
        for i in range(num_segments):
            # Hybrid PSFC
            PSFC_hybrid = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(hybrid_ratio/(1-hybrid_ratio))))
            # Breguet equation for each segment
            V_inf = np.sqrt(2 * W[i] / (rho * S_ref) * np.sqrt(K / (3 * C_D0)))
            C_L = 2*W[i] / (rho * V_inf**2 * S_ref)
            # C_D = C_D0 + K * C_L**2
            C_D = dragpolar(2,C_L)
            D = (rho * V_inf**2 / 2) * S_ref * C_D
            delta_he = seg_h + V_inf**2 / g
            seg_Wfraction[i] = np.exp(-(delta_he * PSFC_hybrid) / (eta_p * (1 - D/(max_takeoff_power * V_inf))))
            W[i+1] = seg_Wfraction[i] * W[i] # modify weight value for next segment

            # Total climb weight fraction is multiplied by current segment's weight fraction
            climb_Wfraction[i+1] = climb_Wfraction[i] * seg_Wfraction[i]
            #print(cruise_Wfraction[i+1])
        
        return climb_Wfraction[:-1]

    climb_Wfraction = getClimbWfrac(101)[-1]          
    W_climb = climb_Wfraction * W_takeoff               # weight at the end of climb/start of cruise in lbs
    '''
    # Plot Climb
    for seg in [2,11,21,101]:
        climb_range = np.linspace(0,25000,seg)
        plt.plot(climb_range, getClimbWfrac(seg), label='{} segments'.format(seg-1), marker='.')

    plt.legend(loc='best')
    plt.title('Climb Fuel Weight Fraction')
    plt.xlabel('Climb Altitude (ft)')
    plt.ylabel('Weight Fraction')
    plt.show()
    '''

    ##### Cruise (multi-segment approach) #####
    # cruise range is not 1000nmi, we need to change this value
    R = 800*6076.11549             # Cruise range of 1000 nmi converted to ft
    h = 25000                       # Cruise altitude 25000 ft
    LoD = 17                        # Lift to drag ratio depending on aircraft design
    E = 45*60                       # Assume endurance of 45 min converted to seconds

    #*** need to change this to density at 25,000 ft
    rho = 10.66e-4                  # air density at cruise altitude of 25,000 ft
    V_inf = 275*1.6878098571        # cruise airspeed 275 kts converted to ft/s

    def getCruiseWfrac(num_segments):
        seg_range = R / num_segments                # range of each segment
        W = np.empty(num_segments + 1)              # Weight array  
        W[0] = W_climb                        # Weight at start of cruise (AKA weight at end of climb)
        seg_Wfraction = np.empty(num_segments)      # Weight fraction of each segment
        cruise_Wfraction = np.empty(num_segments + 1) # Total weight fraction
        cruise_Wfraction[0] = 1.0                   # Initialize at 1.0

        for i in range(num_segments):
            # Breguet equation for each segment
            C_L = 2*W[i] / (rho * V_inf**2 * S_ref)
            LoD = C_L / dragpolar(1,C_L)
            seg_Wfraction[i] = np.exp(-(seg_range * PSFC) / (eta_p * LoD))
            W[i+1] = seg_Wfraction[i] * W[i] # modify weight value for next segment

            # Total cruise weight fraction is reduced by amount of current segment's weight fraction
            # cruise_Wfraction[i+1] = cruise_Wfraction[i] - (1 - seg_Wfraction[i])
            cruise_Wfraction[i+1] = cruise_Wfraction[i] * seg_Wfraction[i]
            #print(cruise_Wfraction[i+1])
        
        return cruise_Wfraction[:-1]

    def getCruiseFuelBurn(num_segments):
        seg_range = R / num_segments                # range of each segment
        W = np.empty(num_segments + 1)              # Weight array  
        T = np.empty(num_segments + 1)              # Thrust array
        W[0] = W_climb                        # Weight at start of cruise (AKA weight at end of climb)
        seg_Wfraction = np.empty(num_segments)      # Weight fraction of each segment
        cruise_fuelburn = np.empty(num_segments+1)  # Total fuel consumed
        seg_fuelburn = np.empty(num_segments)       # Fuel consumed of each segment

        for i in range(num_segments):
            # Breguet equation for each segment
            C_L = 2*W[i] / (rho * V_inf**2 * S_ref) # Lift varies based on weight loss from fuel burn
            T[i] = (W[i]/C_L) * (dragpolar(1,C_L)) # Induced drag is reduced so thrust is reduced

            seg_fuelburn[i] = -PSFC*T[i]*V_inf*seg_range/eta_p
            cruise_fuelburn[i+1] = cruise_fuelburn[i] - seg_fuelburn[i]

            seg_Wfraction[i] = np.exp(-(seg_range * PSFC) / (eta_p * LoD))
            W[i+1] = seg_Wfraction[i] * W[i] # modify weight value for next segment
        
        return T[:-1], cruise_fuelburn[:-1]

    # Plot Cruise
    for seg in [2,11,21,101]:
        cruise_range = np.linspace(0,R / 6076.11549,seg)
        plt.plot(cruise_range, getCruiseWfrac(seg), label='{} segments'.format(seg-1), marker='.')

    plt.legend(loc='best')
    plt.title('Cruise Fuel Weight Fraction')
    plt.xlabel('Cruise Range (nmi)')
    plt.ylabel('Weight Fraction')
    # plt.show()

    # Plot Fuel Burn Consumption
    for seg in [2,11,21,101]:
        cruise_range = np.linspace(0,1000,seg)
        T, fuelburn = getCruiseFuelBurn(seg)
        plt.plot(cruise_range, fuelburn, label='{} segments'.format(seg-1), marker='.')

    plt.legend(loc='best')
    plt.title('Fuel Burn Consumption')
    plt.xlabel('Cruise Range km')
    plt.ylabel('Fuel Burn Consumption lbs')
    # plt.show()

    # Plot Thrust
    for seg in [2,11,21,101]:
        cruise_range = np.linspace(0,1000,seg)
        T, fuelburn = getCruiseFuelBurn(seg)
        plt.plot(cruise_range, T, label='{} segments'.format(seg-1), marker='.')

    plt.legend(loc='best')
    plt.title('Thrust')
    plt.xlabel('Cruise Range km')
    plt.ylabel('Thrust lbs')
    # plt.show()

    cruise_Wfraction = getCruiseWfrac(101)[-1]
    W_cruise = cruise_Wfraction * W_climb  #End of cruise weight

    ##### Loiter #####
    V_loiter = 150*1.6878098571        # loiter speed kts converted to ft/s given by Raymer
    E = 20*60                       # Assume endurance of 20 min converted to seconds (Raymer)
    loiter_Wfraction = np.exp(-E*V_loiter*PSFC/(eta_p*LoD))
    W_loiter = W_cruise * loiter_Wfraction

    ##### Descent #####
    # use previous methods based on statistics (Raymer 6.22)
    W_descent = W_loiter * 0.995

    ##### Landing #####
    # use previous methods based on statistics (Raymer 6.23)
    W_landing = W_descent * 0.997

    '''
    print('Fuel Fractions:')
    print('Taxi: {}'.format(taxi_Wfraction))
    print('Takeoff: {}'.format(takeoff_Wfraction))
    print('Climb: {}'.format(climb_Wfraction))
    print('Cruise: {}'.format(cruise_Wfraction))
    print('Loiter: {}'.format(loiter_Wfraction))
    print('Descent: {}'.format(0.995))
    print('Landing: {}'.format(0.997))
    print()
    '''
    total_Wfraction = taxi_Wfraction * takeoff_Wfraction * climb_Wfraction * cruise_Wfraction * loiter_Wfraction * 0.995 * 0.997
    Wi_W0 = np.array([taxi_Wfraction, takeoff_Wfraction, climb_Wfraction, cruise_Wfraction, loiter_Wfraction, 0.995], float)
    #print(Wi_W0)
    PHIvec = np.array([0, 0.1, # Taxi&Takeoff
          0.36, # Climb
          0, # Cruise
          0, # Descent
          0 # Loiter
          ],float) # Landing
    e_f = 43.15*(1e6/1.3558179483314/0.06852177) 
    e_b= 500*(3600/1.3558179483314/0.06852177) # fpf/slug
    for i in range(len(Wi_W0)-1):
        Wi_W0[i+1] = Wi_W0[i]*Wi_W0[i+1]
    #print(Wi_W0[:-1])
    #print(Wi_W0[1:])
    Wb_W0 = sum(e_f/e_b*(Wi_W0[:-1]-Wi_W0[1:])*(PHIvec[:-1]/(1-PHIvec[:-1]))) / 0.8 # battery fraction, divide by .8 for min charge
    #print(Wb_W0)
    Wb_W0 = 0.09
    W_bat = Wb_W0 * MTOW
    W_final = W_landing
    W_fuel = W_initial - W_final
    
    print('Final Fuel Fraction: {}'.format(total_Wfraction))
    print('Landing Weight:', W_final)
    print('Fuel Weight:', W_fuel)
    
    plt.show()
    return W_fuel, W_bat

#a,b=ImprovedFuelFrac(70000)
#print(a)
#print(b)

ImprovedWeightFracs(55000)  # Run at least twice