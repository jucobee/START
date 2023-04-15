import numpy as np

# Number of pilots
pilots = 2
# Number of attendants
attend = 1
# Total crew
crew = pilots + attend
# Number of passengers
passengers = 50 # lbm
# Weight of each crew member in lbs
wt_crew = 190 # lbm
# Weight of each passenger in lbs
wt_passengers = 200 # lbm
# Weight of baggage for each crew member in lbs
wt_crew_baggage = 30 # lbm
# Weight of baggage for each passenger in lbs
wt_pass_baggage = 40 # lbm
# Total payload weight
W_payload = (passengers * (wt_passengers + wt_pass_baggage)) 

# Total crew weight
W_crew = crew * (wt_crew + wt_crew_baggage)

# Mission range of 1000 nmi
R = 1000*6076.11549 # ft
# Cruise altitude 25000 ft
h = 25000 # ft
# rate of climb/descent  1800 ft/min
ROC = 1800/60 # ft/s
# Propeller Efficiency of 0.8
eta_p = 0.8
# Force of gravity in ft/s^2
g = 32.17 
# Lift to drag ratio depending on aircraft design
L_D = 17 

# Target cruise speed in knots, assume target 350 ktas
V = 350*1.6878098571 # ft/s
# Assume an endurance of 45 min
E = 45*60 # s

# Jet A-1 Fuel: https://en.wikipedia.org/wiki/Jet_fuel
e_f= 43.15*(1e6/1.3558179483314/0.06852177) # fpf/slug
# Assume battery density to be 500 Wh/kg in 2035: https://reader.elsevier.com/reader/sd/pii/S2590116822000698?token=728115593061DB6FAEEBBF7967B91F80780D14E41FCCC4ED6F1359B5F2C28EF47DDEF912CC9F474FADFB0C7CF229CB8E&originRegion=us-east-1&originCreation=20230227073828
e_b= 500*(3600/1.3558179483314/0.06852177) # fpf/slug

# efficiencies
eta_GB = 0.96 # de Vries
eta_GT = 0.40 # de Vries, 2035
eta_PM = 0.99 # de Vries
eta_EM1 = 0.97  # de Vries

# format for hybridization parameter:
# PHIvec = [Taxi&Takeoff, Climb, Cruise, Descent, Loiter, Landing]

def WeightEstimation(PHIvec,WS,WP_ICE,WP_EM1,W0_guess):

    PSFCvec = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHIvec/(1-PHIvec))))
    # PSFCvec_HP = (3600 * 550) * PSFCvec
    print(PSFCvec)
    # Mission Weight fractions
    Wi_Wi1 = np.array([1 - 0.0004*PSFCvec[0]*(3600 * 550), # Taxi&Takeoff
        1 - h*PSFCvec[1]*0.15*550/ROC, # Climb
        np.exp((-R*PSFCvec[2] )/ (0.85*L_D)), # Cruise
        1 - h*PSFCvec[3]*0.15*550/ROC, # Descent
        np.exp((-E*V*PSFCvec[4]) / (0.85*L_D))],float) # Loiter
    
    Wi_W0 = np.append(1,Wi_Wi1.copy())
    for i in range(len(Wi_W0)-1):
        Wi_W0[i+1] = Wi_W0[i]*Wi_W0[i+1]
    Wf_W0 = 1-Wi_W0[-1]
    Wb_W0 = sum(e_f/e_b*(Wi_W0[:-1]-Wi_W0[1:])*(PHIvec[:-1]/(1-PHIvec[:-1]))) / 0.8 # battery fraction, divide by .8 for min charge

    # Calculate Weight


    

    W0_list = []
    W0 = W0_guess
    A = 1.20212 # from regression model
    C = -0.100611
    error = 1e-6
    delta  = (2 * error)

    while delta > error:
        W0_list.append(W0)
        # defined from direct ratios
        W_wing_W0 = 10/WS # wing loading
        # iterables
        We_W0 = A*W0**C # everything else
        W_engine = 2*((W0/WP_ICE/2)**0.9306*10**-0.1205 + (W0/WP_EM1/2)/(5.22*1.34102209/2.20462262)) # lbm, 5.2kW/kg electric engine from Martins
        # W_pg = 1.35*(W_engine+0.24*W0*(1/WP_ICE+1/WP_EM1))
        W0_New = (W_crew + W_payload + W_engine) / (1 - We_W0 - W_wing_W0 - Wf_W0 - Wb_W0 )
        delta = abs((W0_New - W0)/W0_New)
        W0 = W0_New
    W_empty_W0 = (1-Wf_W0)
    return W0,W_empty_W0,Wf_W0,Wb_W0

# format for hybrid parameter:
# PHIvec = [Taxi&Takeoff, Climb, Cruise, Descent, Loiter, Landing]
PHIvec = np.array([0.2, # Taxi&Takeoff
          0.2, # Climb
          0, # Cruise
          0, # Descent
          0, # Loiter
          0],float) # Landing

# from prelim sizing: Wing Loading: 69.364lbm/ft2, Power Loading: 9.578lbm/bhp

WS = 69.364
WP_ICE = 9.578*2
WP_EM1 = 9.578*2

W0_guess = 50000 # lbm
W0,We_W0,Wf_W0,Wb_W0 = WeightEstimation(PHIvec,WS,WP_ICE,WP_EM1,W0_guess)

# m_batt = (R * W0) / (eta_p * e * L_D)
We = We_W0 * W0
# # W_elec = W0 - w_crew - w_payload - We
W_elec = W0*Wb_W0
print("Fuel Fraction: {:3f}".format(Wf_W0))
print("Fuel Weight: {:3f} lbm".format(Wf_W0*W0))
print("Battery Fraction: {:3f}".format(Wb_W0))
print("Takeoff Gross Weight: {:3f} lbm".format(W0))
print("Empty Weight: " + str(round(We)) + " lbm")
print("Empty Weight Fraction: {:.3f}".format(We_W0))
print("Battery & Motor Weight: {:.3f} lbm".format(W_elec))
print("Battery & Motor Weight Fraction: {:.3f}".format(W_elec/W0))
print("Weight of Crew and Payload {:.3f} lbm".format(W_crew+W_payload))
print(W_payload)

# From 1st estimate: 821.836ft2, 5113.424bhp, 4398.445 ft2 wet



