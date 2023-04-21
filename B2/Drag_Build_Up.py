import numpy as np

class Component:
    def __init__(self, C_f=None, FF=None, Q=None, S_wet=None):
        self.C_f = C_f
        self.FF = FF
        self.Q = Q
        self.S_wet = S_wet
    
    def CalculateDrag(self):
        return self.C_f * self.FF * self.Q * self.S_wet
    

def dragComponents(M, rho, V, mu):
    wing = Component()
    hTail = Component()
    vTail = Component()
    nacelle = Component()
    fuselage = Component()

    wing.Q = 1
    hTail.Q = 1.05
    vTail.Q = 1.05
    nacelle.Q = 1.3
    fuselage.Q = 1

    wing.S_wet = 
    hTail.S_wet = 
    vTail.S_wet = 
    nacelle.S_wet = 
    fuselage.S_wet = 
    # Reference Lengths for Cf
    fuselage_L = 
    nacelle_L = 
    wing_L = 
    h_tail_L = 
    v_tail_L = 

    ReW = (rho * V * wing_L) / mu
    ReH = (rho * V * h_tail_L) / mu
    ReV = (rho * V * v_tail_L) / mu
    ReN = (rho * V * nacelle_L) / mu
    ReF = (rho * V * fuselage_L) / mu

    # Max thickness of wings and tails
    tc_wing = 
    tc_h_tail = 
    tc_v_tail = 

    # Chordwise location of max thickness
    xc_wing = 
    xc_h_tail = 
    xc_v_tail = 

    # Sweep angle of wings and tails IN RADIANS
    gammaW = 
    gammaH = 
    gammaV = 

    # Fuselage form factor
    Amax =  # Maximum cross sectional area of fuselage
    f = fuselage_L / (np.sqrt((4/np.pi)*Amax)) # Fineness Ratio
    if f < 6:
        fuselage.FF = (0.9 + (5 / (f**1.5)) + (f/400))
    else:
        fuselage.FF = (1 + (60 / (f**3)) + (f/400))


    # Nacelle form factor
    nacelle.FF = (1 + (0.35/f))


    # Wings and tails
    wing.FF = (1 + (0.6 / xc_wing)*tc_wing + 100*(tc_wing**4)) * (1.34 * (M**0.18)*(np.cos(gammaW)**0.28))
    vTail.FF = (1 + (0.6 / xc_v_tail)*tc_v_tail + 100*(tc_v_tail**4)) * (1.34 * (M**0.18)*(np.cos(gammaV)**0.28))
    hTail.FF = (1 + (0.6 / xc_h_tail)*tc_h_tail + 100*(tc_h_tail**4)) * (1.34 * (M**0.18)*(np.cos(gammaH)**0.28))


    def Cfcalc(Re, wL, wT):
        Cfl = 1.328 / np.sqrt(Re)
        Cft = 0.455 / ((np.log10 * Re)**2.58 * (1 + 0.144*M**2)**0.65)
        Cf = (Cfl * wL) + (Cft * wT)
        return Cf
    
    wing.C_f = Cfcalc(ReW, 0.5, 0.5)
    hTail.C_f = Cfcalc(ReH, 0.5, 0.5)
    vTail.C_f = Cfcalc(ReV, 0.5, 0.5)
    fuselage.C_f = Cfcalc(ReF, 0.25, 0.75)
    nacelle.C_f = Cfcalc(ReN, 0.1, 0.9)

    return [wing, hTail, vTail, fuselage, nacelle]
    








