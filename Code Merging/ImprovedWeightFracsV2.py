from matplotlib import pyplot as plt
import numpy as np
from dragpolar import dragpolar
from ambiance import Atmosphere


def ImprovedWeightFracsV2(MTOW,WS,WP,PHIvec):
    '''
    now using variable hybridization:
    PHIvec = np.array([[0, 0], # Taxi
            [0.36, 0.36], # Takeoff
            [0.2, 0.2], # Climb
            [0, 0], # Cruise
            [0, 0], # Descent
            [0, 0], # Loiter
            [0, 0]], # Landing
            float) 
    '''
    
    ## Assumptions:
    dpobj = dragpolar()
    g=32.17 # from Earth, ft/s^2
    eta_GB = 0.96 # de Vries
    eta_GT = 0.40 # de Vries, 2035
    eta_PM = 0.99 # de Vries
    eta_EM1 = 0.97  # de Vries
    e_f = 43.15*(1e6/1.3558179483314/0.06852177) # Jet A-1 Fuel, fpf/slug
    e_b= 500*(3600/1.3558179483314/0.06852177) # fpf/slug
    PSFC_hybrid = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHIvec/(1-PHIvec))))
    print(PSFC_hybrid)
    ## Dimensionalize:
    S = MTOW/WS
    P = MTOW/WP*550

    ## Defining Weight Fraction Functions
    def WF_SWT(Wi,t,PSFC): # Startup, Warmup, Taxi
        eta_p = 0.50 # assumed, Gudmundsson
        Wip1_Wi = 1-t*PSFC[0]/eta_p*(550*0.05/WP)
        return Wip1_Wi
    
    def WF_TO(Wi,t,PSFC): # Takeoff
        eta_p = 0.50 # assumed, Gudmundsson
        Wip1_Wi = 1-t*PSFC[0]/eta_p*(550/WP)
        return Wip1_Wi

    def WF_climb(Wi,H,PSFC,seg): # Climb
        eta_p = 0.75 # assumed, Gudmundsson
        V = 275*1.6878098571   # needs update
        h=np.linspace(H[0],H[-1],seg+1) # height vector
        dh = H[-1]-H[0] # change in height per segment\
        PSFC = np.linspace(PSFC[0],PSFC[1],seg+1)
        # print(PSFC)
        Wi = [Wi]
        NCR = 0
        for i in range(seg+1):
            rho = Atmosphere(h[i]/3.2808399).density[0]*0.00194032033 # initial density
            q = rho/2*V**2 # dynamic pressure
            C_L = Wi[i]/(S*q);
            D = q*S*dpobj.CD(2,C_L)
            # print(rho,h[i],Wi[i],C_L)
            Wjp1_Wj = np.exp(-PSFC[i]*dh/(V*(1-D/(0.9*eta_p*P/V))))
            # print(Wjp1_Wj)
            Wi.append(Wjp1_Wj*Wi[-1])
            # print(0.9*eta_p*P/V)
            Ps = V*(0.9*eta_p*P/V-D)/Wi[i]
            print(Ps)
            NCR += dh/Ps*V
        return (Wi[-1]/Wi[0]), NCR
        
    


    ## Run the mission
    # Startup, Warmup, Taxi
    t_SWT = 15 * 60 # seconds
    Wip1_Wi_SWT = WF_SWT(MTOW,t_SWT,PSFC_hybrid[0])
    Wf = MTOW*Wip1_Wi_SWT

    # Takeoff
    t_TO = 60 # seconds
    Wip1_Wi_TO = WF_TO(Wf,t_TO,PSFC_hybrid[1])
    Wf = Wf*Wip1_Wi_TO
    
    # Climb
    H = [0,25000] # ft
    Wip1_Wi_Climb,NCR = WF_climb(Wf,H,PSFC_hybrid[2],101)

    print(Wip1_Wi_SWT,Wip1_Wi_TO,Wip1_Wi_Climb,NCR)
    
    
    # PSFC_hybrid = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHI/(1-PHI))))

if __name__ == "__main__":
    MTOW = 54000
    PHIvec = np.array([[0, 0], # Taxi
            [0.36, 0.36], # Takeoff
            [0.2, 0.2], # Climb
            [0, 0], # Cruise
            [0, 0], # Descent
            [0, 0], # Loiter
            [0, 0]], # Landing
            float)  
    ImprovedWeightFracsV2(MTOW,69.36423531558572,8.564498702867692,PHIvec)