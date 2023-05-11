from matplotlib import pyplot as plt
import numpy as np
from dragpolar import dragpolar
from ambiance import Atmosphere


def MissionFractions(MTOW,WS,WP,PHIvec,R_req=500,Rmax=1000):
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
    # PSFC_hybrid = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHIvec/(1-PHIvec))))
    # print(PSFC_hybrid)
    ## Dimensionalize:
    S = MTOW/WS
    P = MTOW/WP*550

    ## Defining Weight Fraction Functions
    def WF_SWT(Wi,t,PHI): # Startup, Warmup, Taxi
        eta_p = 0.50 # assumed, Gudmundsson
        PSFC = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHI[0]/(1-PHI[0]))))
        Wip1_Wi = 1-t*PSFC/eta_p*(550*0.05/WP)

        Wbi_Wi = e_f/e_b*(1-Wip1_Wi)*(PHI[0]/(1-PHI[0]))
        
        return Wip1_Wi,Wbi_Wi
    
    def WF_TO(Wi,t,PHI): # Takeoff
        eta_p = 0.50 # assumed, Gudmundsson
        PSFC = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(PHI[0]/(1-PHI[0]))))
        Wip1_Wi = 1-t*PSFC/eta_p*(550/WP)

        Wbi_Wi = e_f/e_b*(1-Wip1_Wi)*(PHI[0]/(1-PHI[0]))
        
        return Wip1_Wi,Wbi_Wi

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


        Wb = []
        Wf = []
        for i in range(seg):
            Wf.append(Wi[i]-Wi[i+1])
            Wb.append(Wf[i]*e_f/e_b*P_ratio[i])

        return (Wi[-1]/Wi[0]), (np.sum(Wb)/Wi[0]), NCR/6076.11549 
        
    def WF_cruise(Wi,h,R,PHI,seg): # Cruise
        eta_p = 0.85 # assumed, Gudmundsson
        V = 275*1.6878098571   # needs update
        Wi = [Wi]
        R = 6076.11549*np.linspace(0,R,seg+1) # range vector
        dR = (R[-1]-R[0])/seg # change in range per segment

        PHI = np.linspace(PHI[0],PHI[-1],seg)
        P_ratio = PHI/(1-PHI)
        PSFC = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(P_ratio)))

        for i in range(seg):
            rho = Atmosphere(h/3.2808399).density[0]*0.00194032033 # initial density
            # print(rho)
            q = rho/2*V**2 # dynamic pressure
            C_L = Wi[i]/(S*q);
            LoD = C_L / dpobj.CD(1,C_L)
            Wjp1_Wj = np.exp(-PSFC[i]*dR/(eta_p * LoD))
            # print(Wjp1_Wj)
            Wi.append(Wjp1_Wj*Wi[-1])

        Wb = []
        Wf = []
        for i in range(seg):
            Wf.append(Wi[i]-Wi[i+1])
            Wb.append(Wf[i]*e_f/e_b*P_ratio[i])
        return (Wi[-1]/Wi[0]), (np.sum(Wb)/Wi[0])
    
    def WF_descent(Wi,H,PHI,seg): # Descent
        throttle = 0.05
        eta_p = 0.75 # assumed, Gudmundsson
        V = 275*1.6878098571   # needs update
        h=np.linspace(H[0],H[-1],seg+1) # height vector
        dh = (H[-1]-H[0])/seg # change in height per segment

        PHI = np.linspace(PHI[0],PHI[-1],seg)
        P_ratio = PHI/(1-PHI)
        PSFC = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(P_ratio)))
        PSFC_hp = np.linspace(PSFC[0],PSFC[1],seg+1) * (3600 * 550)

        Wi = [Wi]
        for i in range(seg):
            RoD = -V*np.sin(3*np.pi/180) # Rate of Descent estimation, 3 deg
            # rho = Atmosphere(h[i]/3.2808399).density[0]*0.00194032033 # initial density
            # # print(rho)
            # q = rho/2*V**2 # dynamic pressure
            # C_L = Wi[i]/(S*q);
            # D = q*S*dpobj.CD(2,C_L)
            Wjp1_Wj = 1-dh*PSFC_hp[i]*throttle/(3600*RoD)
            Wi.append(Wjp1_Wj*Wi[-1])

        Wb = []
        Wf = []
        for i in range(seg):
            Wf.append(Wi[i]-Wi[i+1])
            Wb.append(Wf[i]*e_f/e_b*P_ratio[i])

        return (Wi[-1]/Wi[0]), (np.sum(Wb)/Wi[0])

    def WF_loiter(Wi,h,E,PHI,seg): # Cruise
        eta_p = 0.85 # assumed, Gudmundsson
        V = 275*1.6878098571   # needs update
        Wi = [Wi]
        E=np.linspace(0,E,seg+1) # time vector
        dE = (E[-1]-E[0])/seg # change in time per segment

        PHI = np.linspace(PHI[0],PHI[-1],seg)
        P_ratio = PHI/(1-PHI)
        PSFC = 1/(eta_GB*e_f/g*(eta_GT+eta_PM*eta_EM1*(P_ratio)))
        PSFC_hp = np.linspace(PSFC[0],PSFC[1],seg+1) * (3600 * 550)

        for i in range(seg):
            rho = Atmosphere(h/3.2808399).density[0]*0.00194032033 # initial density
            q = rho/2*V**2 # dynamic pressure
            C_L = Wi[i]/(S*q);
            LoD = C_L / dpobj.CD(1,C_L)
            Wjp1_Wj = np.exp(-dE*V*PSFC[i]/(eta_p * LoD))
            Wi.append(Wjp1_Wj*Wi[-1])

        Wb = []
        Wf = []
        for i in range(seg):
            Wf.append(Wi[i]-Wi[i+1])
            Wb.append(Wf[i]*e_f/e_b*P_ratio[i])
            
        return (Wi[-1]/Wi[0]), (np.sum(Wb)/Wi[0])
    
    def runMission(PHIvec,R_req=1000):
        ## Run the design mission
        Wi = [MTOW]
        Wip1_Wi = []
        Wbip1_Wi = []
        # print('Ramp Weight: {:.3f}'.format(MTOW))

        # Startup, Warmup, Taxi
        t_SWT = 15 * 60 # seconds
        Wip1_Wi_SWT,Wbi_Wi = WF_SWT(MTOW,t_SWT,PHIvec[0])
        Wi.append(MTOW*Wip1_Wi_SWT)
        Wip1_Wi.append(Wip1_Wi_SWT)
        Wbip1_Wi.append(Wbi_Wi)
        # print('MTOW: {:.3f}'.format(Wi[-1]))

        # Takeoff
        t_TO = 60 # seconds
        Wip1_Wi_TO,Wbi_Wi = WF_TO(Wi[-1],t_TO,PHIvec[1])
        Wi.append(Wi[-1]*Wip1_Wi_TO)
        Wip1_Wi.append(Wip1_Wi_TO)
        Wbip1_Wi.append(Wbi_Wi)
        # print('Post Takeoff: {:.3f}'.format(Wi[-1]))

        # Climb
        H = [0,25000] # ft
        Wip1_Wi_Climb,Wbi_Wi,NCR = WF_climb(Wi[-1],H,PHIvec[2],101)
        Wi.append(Wi[-1]*Wip1_Wi_Climb)
        Wip1_Wi.append(Wip1_Wi_Climb)
        Wbip1_Wi.append(Wbi_Wi)
        # print('Post Climb: {:.3f}'.format(Wi[-1]))

        # Cruise
        R = R_req-NCR
        h=25000
        Wip1_Wi_Cruise,Wbi_Wi = WF_cruise(Wi[-1],h,R,PHIvec[3],101)
        Wi.append(Wi[-1]*Wip1_Wi_Cruise)
        Wip1_Wi.append(Wip1_Wi_Cruise)
        Wbip1_Wi.append(Wbi_Wi)
        # print('Post Cruise: {:.3f}'.format(Wi[-1]))

        # Descent 
        H = [25000,5000] # ft
        Wip1_Wi_Descent,Wbi_Wi = WF_descent(Wi[-1],H,PHIvec[4],101)
        Wi.append(Wi[-1]*Wip1_Wi_Descent)
        Wip1_Wi.append(Wip1_Wi_Descent)
        Wbip1_Wi.append(Wbi_Wi)
        # print('Post Descent: {:.3f}'.format(Wi[-1]))

        # Short hold (ignore)

        # Divert Climb
        H = [5000,15000] # ft
        Wip1_Wi_DClimb,Wbi_Wi,NCR = WF_climb(Wi[-1],H,PHIvec[5],101)
        Wi.append(Wi[-1]*Wip1_Wi_DClimb)
        Wip1_Wi.append(Wip1_Wi_DClimb)
        Wbip1_Wi.append(Wbi_Wi)
        # print('Post Divert Climb: {:.3f}'.format(Wi[-1]))

        # Divert Cruise
        R = 200-NCR
        h= 15000
        Wip1_Wi_DCruise,Wbi_Wi = WF_cruise(Wi[-1],h,R,PHIvec[7],101)
        Wi.append(Wi[-1]*Wip1_Wi_DCruise)
        Wip1_Wi.append(Wip1_Wi_DCruise)
        Wbip1_Wi.append(Wbi_Wi)
        # print('Post Divert Cruise: {:.3f}'.format(Wi[-1]))

        # Divert 1st Descent 
        H = [15000,0] # ft
        Wip1_Wi_D1Descent,Wbi_Wi = WF_descent(Wi[-1],H,PHIvec[8],101)
        Wi.append(Wi[-1]*Wip1_Wi_D1Descent)
        Wip1_Wi.append(Wip1_Wi_D1Descent)
        Wbip1_Wi.append(Wbi_Wi)
        # print('Post Divert 1st Descent: {:.3f}'.format(Wi[-1]))

        # Loiter 
        E = 30*60 # s
        Wip1_Wi_Loiter,Wbi_Wi = WF_loiter(Wi[-1],h,E,PHIvec[8],101)
        Wi.append(Wi[-1]*Wip1_Wi_Loiter)
        Wip1_Wi.append(Wip1_Wi_Loiter)
        Wbip1_Wi.append(Wbi_Wi)
        # print('Post Loiter: {:.3f}'.format(Wi[-1]))

        # Divert Last Descent 
        H = [5000,0] # ft
        Wip1_Wi_D2Descent,Wbi_Wi = WF_descent(Wi[-1],H,PHIvec[9],101)
        Wi.append(Wi[-1]*Wip1_Wi_D2Descent)
        Wip1_Wi.append(Wip1_Wi_D2Descent)
        Wbip1_Wi.append(Wbi_Wi)
        print('Landing Weight: {:.3f}'.format(Wi[-1]))
        
        Wb_W0 = sum(np.array(Wbip1_Wi)*np.array(Wi[0:-1])/Wi[0])
        Wf_W0 = (Wi[0]-Wi[-1])/Wi[0]

        return Wb_W0,Wf_W0



    Wb_W0,Wf_W0 = runMission(PHIvec,R_req)
    print('{:.0f} nmi block fuel: {:.3f}'.format(R_req,Wf_W0*MTOW))

    # Wb_W0,Wf_W0 = runMission(PHIvec,R_req=500)
    # print('500 nmi block fuel: {:.3f}'.format(Wf_W0*MTOW))

    return Wb_W0,Wf_W0
    

    

    

    

   

if __name__ == "__main__":
    MTOW = 1
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
    Wb_W0,Wf_W0 = MissionFractions(MTOW,69.36423531558572,8.564498702867692,PHIvec)