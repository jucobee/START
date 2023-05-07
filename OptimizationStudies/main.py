import numpy as np
import sys
import openmdao.api as om

# format = [GT,GB,P1,EM1,PM,EM2,P2]
# value justification
# P1,P2 = 0.85 (Constant Speed, Gudmundsson)
# the rest = deVries
eta = [.4,.96,.85,.97,.99,.97,.85]
# [0,0,0,0,0,0,0,0,0,0]
# Constraints
'''
wp_tofl
wp_tofl_5kft
wp_climb_TO
wp_climb_TC
wp_climb_SSC
wp_climb_ERC
wp_climb_BLC_AEO
wp_climb_BLC_OEI
wp_ceil
wp_cruise_min
wp_cruise_target
wp_approach_SLp18
wp_approach_p18_5kft
wp_landing_SLp18
wp_landing_p18_5kft

'''

def PTinvert(ERatio,PRatio,eta):
    PTmatrix = np.array([[-eta[0],1,0,0,0,0,0,0,0,0],
                        [0,-eta[1],1,1,0,0,0,0,0,0],
                        [0,0,0,-eta[2],0,0,0,0,1,0],
                        [0,0,-eta[3],0,1,0,0,0,0,0],
                        [0,0,0,0,-eta[4],-eta[4],1,0,0,0],
                        [0,0,0,0,0,0,-eta[5],1,0,0],
                        [0,0,0,0,0,0,0,-eta[6],0,1],
                        [ERatio,0,0,0,0,ERatio-1,0,0,0,0],
                        [0,0,0,PRatio,0,0,0,PRatio-1,0,0],
                        [0,0,0,0,0,0,0,0,1,1]])
    P_p = [0,0,0,0,0,0,0,0,0,1] # bhp/lbm
    PTvector = np.linalg.solve(PTmatrix,P_p) 
    return PTvector

## Weight Estimation
pilots = 2 # Number of pilots
attend = 1 # Number of attendants
crew = pilots + attend # Total crew
passengers = 50 # Number of passengers
wt_crew = 190 # Weight of each crew member, lbf
wt_passengers = 200 # Weight of each passenger, lbf
wt_crew_baggage = 30 # Weight of baggage for each crew member, lbf
wt_pass_baggage = 40 # Weight of baggage for each passenger, lbf
W_payload = (passengers * (wt_passengers + wt_pass_baggage)) # Total payload weight, lbf
W_crew = crew * (wt_crew + wt_crew_baggage) # Total crew weight, lbf
R = 1000*6076.11549 # Mission range of 1000 nmi
h = 25000 # Cruise altitude 25000 ft
ROC = 8*3.2808399*60 # rate of climb/descent 8 m/s, ft/min
eta_p = 0.85 # Propeller Efficiency of 0.85, gudmundsson
g = 32.17 # Force of gravity in ft/s^2
L_D = 17 # Lift to drag ratio 
V = 275*1.6878098571 # Target cruise speed in knots, assume 275 ktas, ft/s
E = 45*60 # Assume an endurance of 45 min, s
e_f= 43.15*(1e6/1.3558179483314/0.06852177) # Jet A-1 Fuel 43.15 MJ/kg: https://en.wikipedia.org/wiki/Jet_fuel, fpf/slug
e_b= 500*(3600/1.3558179483314/0.06852177) # Assume battery density to be 500 Wh/kg in 2035: https://reader.elsevier.com/reader/sd/pii/S2590116822000698?token=728115593061DB6FAEEBBF7967B91F80780D14E41FCCC4ED6F1359B5F2C28EF47DDEF912CC9F474FADFB0C7CF229CB8E&originRegion=us-east-1&originCreation=20230227073828, fpf/slug

# efficiencies
# eta = [.4,.96,.85,.97,.99,.97,.85]
# format = [GT,GB,P1,EM1,PM,EM2,P2]
eta_GB = eta[1] # de Vries
eta_GT = eta[0] # de Vries, advanced 2035 
eta_PM = eta[4] # de Vries
eta_EM1 = eta[3]  # de Vries

# format for hybridization parameter:
# PHIvec = [Taxi&Takeoff, Climb, Cruise, Descent, Loiter, Landing]

def weightEst0(PHIvec,W0_guess):
    PSFCvec = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHIvec/(1-PHIvec))))
    print(PSFCvec)
    # PSFCvec_HP = (3600 * 550) * PSFCvec
    L_D  = 17 + (PHIvec[0]+PHIvec[1])/2*(22-17)
    print(PSFCvec)
    print(L_D)
    # Obtain Mission Weight fractions
    Wi_Wi1 = np.array([1 - 0.0004*PSFCvec[0]*(3600 * 550), # Taxi&Takeoff
        1 - h*PSFCvec[1]*(3600*550)*0.15/ROC/60, # Climb
        np.exp((-R*PSFCvec[2] )/ (0.85*L_D)), # Cruise
        1 - h*PSFCvec[3]*(3600*550)*0.15/ROC/60, # Descent
        np.exp((-E*V*PSFCvec[4]) / (0.85*L_D))],np.float64) # Loiter
    print(Wi_Wi1)
    Wi_W0 = np.append(1,Wi_Wi1.copy())

    for i in range(len(Wi_W0)-1): # obtain cumulative weight fraction Wi_W0
        Wi_W0[i+1] = Wi_W0[i]*Wi_W0[i+1]

    print(Wi_W0)
    Wf_W0 = 1-Wi_W0[-1] # get fuel weight fraction
    # get battery weight fraction due to hybridization (carlos method 😎)
    Wb_W0 = sum(e_f/e_b*(Wi_W0[:-1]-Wi_W0[1:])*(PHIvec[:-1]/(1-PHIvec[:-1]))) / 0.8 # battery fraction, divide by .8 for min charge

    #print(Wi_W0[:-1])
    # Calculate Weight via iteration and statistical model
    W0_list = []
    W0 = W0_guess
    A = 0.96 # from turboprop empty weight
    C = -0.05
    error = 1e-6
    delta  = (2 * error)

    while delta > error:
        W0_list.append(W0)
        # iterables
        We_W0 = A*W0**C # everything else
        # W_engine = 2*((W0/WP_ICE/2)**0.9306*10**-0.1205 + (W0/WP_EM1/2)/(5.22*1.34102209/2.20462262)) # lbm, 5.2kW/kg electric engine from Martins
        # W_pg = 1.35*(W_engine+0.24*W0*(1/WP_ICE+1/WP_EM1))
        W0_New = (W_crew + W_payload) / (1 - We_W0 - Wf_W0 - Wb_W0 )
        delta = abs((W0_New - W0)/W0_New)
        W0 = W0_New
        
    print(np.isnan(W0))
    if np.isnan(W0):
        return 1e10,1,1,1
    else:
        W_empty_W0 = (1-Wf_W0-((W_crew + W_payload)/W0))
        return W0,W_empty_W0,Wf_W0,Wb_W0

# format for hybrid parameter:
# PHIvec = [Taxi&Takeoff, Climb, Cruise, Descent, Loiter, Landing]
# PHIvec = np.array([0.2, # Taxi&Takeoff
#           0.36, # Climb
#           0, # Cruise
#           0, # Descent
#           0, # Loiter
#           0],np.float64) # Landing

# # from prelim sizing: Wing Loading: 69.364lbm/ft2, Power Loading: 9.578lbm/bhp
# # WS = 69.364
# # WP_ICE = 9.578*2
# # WP_EM1 = 9.578*2

# W0_guess = 50000 # lbm
# W0,We_W0,Wf_W0,Wb_W0 = weightEst0(PHIvec,W0_guess)

# # # m_batt = (R * W0) / (eta_p * e * L_D)
# # We = We_W0 * W0
# # # # W_elec = W0 - w_crew - w_payload - We
# # W_elec = W0*Wb_W0
# print('battery fraction {:.3f}'.format(Wb_W0))
# '''
# print("Fuel Fraction: {:3f}".format(Wf_W0))
# print("Fuel Weight: {:3f} lbm".format(Wf_W0*W0))
# print("Battery Fraction: {:3f}".format(Wb_W0))
# print("Takeoff Gross Weight: {:3f} lbm".format(W0))
# print("Empty Weight: " + str(round(We)) + " lbm")
# print("Empty Weight Fraction: {:.3f}".format(We_W0))
# print("Battery & Motor Weight: {:.3f} lbm".format(W_elec))
# print("Battery & Motor Weight Fraction: {:.3f}".format(W_elec/W0))
# print("Weight of Crew and Payload {:.3f} lbm".format(W_crew+W_payload))
# print(W_payload)
# '''
# # From 1st estimate: 821.836ft2, 5113.424bhp, 4398.445 ft2 wet


class weightEstOpt0(om.ExplicitComponent):
    """ 
    Estimates the weight of the aircraft based on hybridization (in terms of supplied and shaft energy)
    """

    def setup(self):
        self.add_input('PHIvec', val= np.array([0.2, # Taxi&Takeoff
          0.36, # Climb
          0.1, # Cruise
          0, # Descent
          0, # Loiter
          0],np.float64)) # Landing
        self.add_output('fuel', val=1)

    def setup_partials(self):
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):

        # WS = 69.364 # lbm/ft2
        # WP_ICE = 9.578 # lbm/bhp
        # WP_EM1 = 1e-6 # lbm/bhp

        PHIvec = inputs['PHIvec']
        W0,W_empty_W0,Wf_W0,Wb_W0 = weightEst0(PHIvec,5e4)
        outputs['fuel'] = W0*Wf_W0

        print('PHIVec: {}'.format(prob['weightEst0.PHIvec']))
        print('MTOW: {}'.format(W0))
        print('empty weight fraction: {}'.format(W_empty_W0))
        print('empty weight: {}'.format(W0*W_empty_W0))
        print('battery fraction: {}'.format(Wb_W0))
        print('battery weight: {}'.format(W0*Wb_W0))
        print('fuel fraction: {}'.format(Wf_W0))
        print('fuel weight: {}'.format(W0*Wf_W0))
        

if __name__ == "__main__":

        prob = om.Problem()
        prob.model.add_subsystem('weightEst0', weightEstOpt0(), promotes_inputs=['PHIvec'])

        prob.model.set_input_defaults('PHIvec', np.array([0.0, # Taxi&Takeoff
          0.0, # Climb
          0, # Cruise
          0, # Descent
          0, # Loiter
          0],np.float64)) # Landing

        prob.driver = om.ScipyOptimizeDriver()
        prob.driver.options['optimizer'] = 'SLSQP'
        prob.driver.options['maxiter'] = 1e3

        prob.model.add_design_var('PHIvec',lower = 0, upper = 1)
        prob.model.add_objective('weightEst0.fuel',scaler=1)

        prob.setup()
        prob.run_driver();
