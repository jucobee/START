from matplotlib import pyplot as plt
import numpy as np
from dragpolar import dragpolar
from ambiance import Atmosphere


def ImprovedWeightFracsV2(MTOW,WS,WP,PHIvec,R_req=500,Rmax=1000):
    '''
    now using variable hybridization:
    PHIvec = np.array([[0, 0], # Taxi
            [0.36, 0.36], # Takeoff
            [0.2, 0.2], # Climb
            [0, 0],     # Cruise
            [0, 0],     # Descent
            [0, 0],     # Divert Climb
            [0, 0],     # Divert
            [0, 0],     # Divert First Descent
            [0, 0],     # Loiter
            [0, 0],     # Divert Final Descent
            [0, 0]],    # Landing
            float) 

    also, use nmi for range
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
    # print(PSFC_hybrid)
    ## Dimensionalize:
    S = MTOW/WS
    P = MTOW/WP*550

    ## Defining Weight Fraction Functions
    def WF_SWT(Wi,t,PHI): # Startup, Warmup, Taxi
        eta_p = 0.50 # assumed, Gudmundsson
        PSFC = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHI[0]/(1-PHI[0]))))
        Wip1_Wi = 1-t*PSFC/eta_p*(550*0.05/WP)
        return Wip1_Wi
    
    def WF_TO(Wi,t,PHI): # Takeoff
        eta_p = 0.50 # assumed, Gudmundsson
        PSFC = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHI[0]/(1-PHI[0]))))
        Wip1_Wi = 1-t*PSFC/eta_p*(550/WP)
        return Wip1_Wi

    def WF_climb(Wi,H,PHI,seg): # Climb
        eta_p = 0.75 # assumed, Gudmundsson
        V = 275*1.6878098571   # needs update
        h=np.linspace(H[0],H[-1],seg+1) # height vector
        dh = (H[-1]-H[0])/seg # change in height per segment

        PHI = np.linspace(PHI[0],PHI[-1],seg)
        P_ratio = PHI/(1-PHI)
        PSFC = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(P_ratio)))
        
        Wi = [Wi]
        NCR = 0
        for i in range(seg):
            throttle = .9
            rho = Atmosphere(h[i]/3.2808399).density[0]*0.00194032033 # initial density
            # print(rho)
            q = rho/2*V**2 # dynamic pressure
            C_L = Wi[i]/(S*q);
            D = q*S*dpobj.CD(2,C_L)
            # print(rho,h[i],Wi[i],C_L)
            Wjp1_Wj = np.exp(-PSFC[i]*dh/((1-D/(throttle*eta_p*P/V))))
            # print(Wjp1_Wj)
            Wi.append(Wjp1_Wj*Wi[-1])
            # print(0.9*eta_p*P/V)
            Ps = V*(throttle*eta_p*P/V-D)/Wi[i]
            # print(Ps)
            NCR += dh/Ps*V
        return (Wi[-1]/Wi[0]), NCR/6076.11549 
        
    def WF_cruise(Wi,h,R,PSFC,seg): # Cruise
        eta_p = 0.85 # assumed, Gudmundsson
        V = 275*1.6878098571   # needs update
        PSFC = np.linspace(PSFC[0],PSFC[1],seg+1)
        Wi = [Wi]
        R = 6076.11549*np.linspace(0,R,seg+1) # range vector
        dR = (R[-1]-R[0])/seg # change in range per segment
        for i in range(seg):
            rho = Atmosphere(h/3.2808399).density[0]*0.00194032033 # initial density
            # print(rho)
            q = rho/2*V**2 # dynamic pressure
            C_L = Wi[i]/(S*q);
            LoD = C_L / dpobj.CD(1,C_L)
            Wjp1_Wj = np.exp(-PSFC[i]*dR/(eta_p * LoD))
            # print(Wjp1_Wj)
            Wi.append(Wjp1_Wj*Wi[-1])
        return (Wi[-1]/Wi[0])
    
    def WF_descent(Wi,H,PSFC,seg): # Descent
        throttle = 0.1
        eta_p = 0.75 # assumed, Gudmundsson
        V = 275*1.6878098571   # needs update
        h=np.linspace(H[0],H[-1],seg+1) # height vector
        dh = (H[-1]-H[0])/seg # change in height per segment
        PSFC_hp = np.linspace(PSFC[0],PSFC[1],seg+1) * (3600 * 550)
        Wi = [Wi]
        NCR = 0
        for i in range(seg):
            RoD = -V*np.sin(3*np.pi/180) # Rate of Descent estimation, 3 deg
            # rho = Atmosphere(h[i]/3.2808399).density[0]*0.00194032033 # initial density
            # # print(rho)
            # q = rho/2*V**2 # dynamic pressure
            # C_L = Wi[i]/(S*q);
            # D = q*S*dpobj.CD(2,C_L)
            Wjp1_Wj = 1-dh*PSFC_hp[i]*throttle/(3600*RoD)
            Wi.append(Wjp1_Wj*Wi[-1])
        return (Wi[-1]/Wi[0])

    def WF_loiter(Wi,h,E,PSFC,seg): # Cruise
        eta_p = 0.85 # assumed, Gudmundsson
        V = 275*1.6878098571   # needs update
        PSFC = np.linspace(PSFC[0],PSFC[1],seg+1)
        Wi = [Wi]
        E=np.linspace(0,E,seg+1) # time vector
        dE = (E[-1]-E[0])/seg # change in time per segment
        for i in range(seg):
            rho = Atmosphere(h/3.2808399).density[0]*0.00194032033 # initial density
            q = rho/2*V**2 # dynamic pressure
            C_L = Wi[i]/(S*q);
            LoD = C_L / dpobj.CD(1,C_L)
            Wjp1_Wj = np.exp(-dE*V*PSFC[i]/(eta_p * LoD))
            Wi.append(Wjp1_Wj*Wi[-1])
        return (Wi[-1]/Wi[0])
    
    ## Run the design mission
    print('Ramp Weight: {:.3f}'.format(MTOW))
    # Startup, Warmup, Taxi
    t_SWT = 15 * 60 # seconds
    Wip1_Wi_SWT = WF_SWT(MTOW,t_SWT,PHIvec[0])
    Wf = MTOW*Wip1_Wi_SWT
    print('MTOW: {:.3f}'.format(Wf))
    # Takeoff
    t_TO = 60 # seconds
    Wip1_Wi_TO = WF_TO(Wf,t_TO,PHIvec[1])
    Wf = Wf*Wip1_Wi_TO
    print('Post Takeoff: {:.3f}'.format(Wf))
    # Climb
    H = [0,25000] # ft
    Wip1_Wi_Climb,NCR = WF_climb(Wf,H,PHIvec[2],101)
    Wf = Wf*Wip1_Wi_Climb
    print('Post Climb: {:.3f}'.format(Wf))
    # Cruise
    R = 1000-NCR
    h=25000
    Wip1_Wi_Cruise = WF_cruise(Wf,h,R,PSFC_hybrid[3],101)
    Wf = Wf*Wip1_Wi_Cruise
    print('Post Cruise: {:.3f}'.format(Wf))
    # Descent 
    H = [25000,5000] # ft
    Wip1_Wi_Descent = WF_descent(Wf,H,PSFC_hybrid[4],101)
    Wf = Wf*Wip1_Wi_Descent
    print('Post Descent: {:.3f}'.format(Wf))
    # Short hold (ignore)

    # Divert Climb
    H = [5000,15000] # ft
    Wip1_Wi_DClimb,NCR = WF_climb(Wf,H,PSFC_hybrid[6],101)
    Wf = Wf*Wip1_Wi_DClimb
    print('Post Divert Climb: {:.3f}'.format(Wf))
    # Divert Cruise
    R = 200-NCR
    h= 15000
    Wip1_Wi_DCruise = WF_cruise(Wf,h,R,PSFC_hybrid[7],101)
    Wf = Wf*Wip1_Wi_DCruise
    print('Post Divert Cruise: {:.3f}'.format(Wf))
    # Divert 1st Descent 
    H = [15000,0] # ft
    Wip1_Wi_D1Descent = WF_descent(Wf,H,PSFC_hybrid[8],101)
    Wf = Wf*Wip1_Wi_D1Descent
    print('Post Divert 1st Descent: {:.3f}'.format(Wf))
    # Loiter 
    E = 30*60 # s
    Wip1_Wi_Loiter = WF_loiter(Wf,h,E,PSFC_hybrid[8],101)
    Wf = Wf*Wip1_Wi_Loiter
    print('Post Loiter: {:.3f}'.format(Wf))
    # Divert Last Descent 
    H = [5000,0] # ft
    Wip1_Wi_D2Descent = WF_descent(Wf,H,PSFC_hybrid[9],101)
    Wf = Wf*Wip1_Wi_D2Descent
    print('Landing Weight: {:.3f}'.format(Wf))
    print(Wf/MTOW)
    

   

if __name__ == "__main__":
    MTOW = 54000
    PHIvec = np.array([[0, 0], # Taxi
            [0.36, 0.36],      # Takeoff
            [0.2, 0.2],        # Climb
            [0, 0],            # Cruise
            [0, 0],            # Descent
            [0, 0],            # Divert Climb
            [0, 0],            # Divert
            [0, 0],            # Divert First Descent
            [0, 0],            # Loiter
            [0, 0],            # Divert Final Descent
            [0, 0]],           # Landing
            float)
    ImprovedWeightFracsV2(MTOW,69.36423531558572,8.564498702867692,PHIvec)