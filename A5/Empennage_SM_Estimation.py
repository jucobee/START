import numpy as np
import math

# Empennage sizing #
Cvt = 0.09   # Verticle tail volume coefficient from Raymer table 6.4
Cht = 1      # Horizantle tail volume coefficient from Raymer table 6.4

Lvt =       # Verticle tail moment arm
Lht =       # Horizantle tail moment arm
bw =        # Span of wing
cw =        # Wing mean chord


AR_w =    # Wing Aspect Ratio
AR_h =    # Horizantle Stabilizer Aspect Ratio
eta = 0.97    # section lift curve difference coefficient
M =       # Cruise mach number
gam_w =   # Sweep angle of wing in degrees
gam_h =   # Sweep angle of horizantle stabilizer in degrees
S_h =     # Surface area of horizantle tail in ft^2
S_w =     # Surface area of wing in ft^2
Svt = (Cvt * bw * S_w) / Lvt  # Planform area of vertical tail
Sht = (Cht * cw * S_w) / Lht  # Planform area of horizantle tail
eta_h = 0.9  # tail efficiency (0.9 is typical for low tails, so we probably want to change this value)
Kf = 0.344     # Empirical factor, 0.344 is the value for a quarter chord position on the body at 0.3 of the body length
Lf =        # Fuselage length
Wf =        # Maximum width of fuselage
Lh =        # Distance from CG back to tail
Xcg =       # Aircraft center of gravity
X25mac =    # Not too sure what this term means, maybe something related to aerodynamic center

CL_al_w = (2 * np.pi * AR_w) / (2 + np.sqrt(((AR_w / eta)**2) * (1 + (np.tan(gam_w))**2 - M**2)) + 4)   # List curve slope of wing, / radian
CL_al_h0 = (2 * np.pi * AR_h) / (2 + np.sqrt(((AR_h / eta)**2) * (1 + (np.tan(gam_h))**2 - M**2)) + 4)   # List curve slope of horizantle tail, / radian

de_dal = (2 * CL_al_w) / (np.pi * AR_w)    # Wing downwash with respect to alpha, / radian
CL_al_h = CL_al_h0 * (1 - de_dal) * eta_h   # Correct tail lift curve slope

dCmf_dCL = (Kf * (Wf ** 2) * Lf) / (S_w * cw * CL_al_w)

SM = ((Xcg - X25mac) / cw) - ((CL_al_h * S_h * Lh) / (CL_al_w * S_w * cw)) + dCmf_dCL   # Static Margin estimation
print("Static margin SM = {}".format(SM))
