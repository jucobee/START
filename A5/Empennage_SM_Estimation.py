import numpy as np
import math

def Empennage_Sizing(Cvt,Cht,Lvt,Lht,bw,cw,S_w):
    Svt = (Cvt * bw * S_w) / Lvt  # Planform area of vertical tail
    Sht = (Cht * cw * S_w) / Lht  # Planform area of horizantle tail
    print("Vertical Tail Surface Area = {}".format(Svt))
    print("Horizontal Tail Surface Area = {}".format(Sht))

# Empennage sizing #
Cvt = 0.05  - 0.05*0.05  # Verticle tail volume coefficient from Raymer table 6.4 + End plate effect
Cht = 0.9     # Horizantle tail volume coefficient from Raymer table 6.4

Lvt =  30 + (11.12500/4) - (5.41837/4)      # Verticle tail moment arm (Quarter chord length used to find AC)
Lht =  43 + (4.50000/4) - (5.41837/4)      # Horizantle tail moment arm (Quarter chord length used to find AC)
bw =  115.77869      # Projected Span of wing
cw =  5.41837      # Wing mean chord

S_w = 826.13454    # Surface area of wing in ft^2

Empennage_Sizing(Cvt,Cht,Lvt,Lht,bw,cw,S_w)

AR_w =  16.22581  # Wing Aspect Ratio
AR_h =  4.44444  # Horizantle Stabilizer Aspect Ratio
eta = 0.97    # section lift curve difference coefficient
M = 0.6      # Cruise mach number
gam_w = 5  # Sweep angle of wing in degrees
gam_h = 0.285  # Sweep angle of horizontal stabilizer in degrees
S_w =  144.56888401941083   # Surface area of wing in ft^2
Svt = (Cvt * bw * S_w) / Lvt  # Planform area of vertical tail
Sht = (Cht * cw * S_w) / Lht  # Planform area of horizantle tail
S_h =  94.19298487511068   # Surface area of horizantle tail in ft^2
eta_h = 0.9  # tail efficiency (0.9 is typical for low tails, so we probably want to change this value)
Kf = 0.344     # Empirical factor, 0.344 is the value for a quarter chord position on the body at 0.3 of the body length
Lf = 79       # Fuselage length
Wf = 9       # Maximum width of fuselage
Xcg = 10.773      # Aircraft center of gravity
Lh =  30 + 10 - Xcg     # Distance from CG back to tail
X25mac = 11.12500   # Not too sure what this term means, maybe something related to aerodynamic center (Quarter chord length)

CL_al_w = (2 * np.pi * AR_w) / (2 + np.sqrt(((AR_w / eta)**2) * (1 + (np.tan(gam_w))**2 - M**2)) + 4)   # List curve slope of wing, / radian
CL_al_h0 = (2 * np.pi * AR_h) / (2 + np.sqrt(((AR_h / eta)**2) * (1 + (np.tan(gam_h))**2 - M**2)) + 4)   # List curve slope of horizantle tail, / radian

de_dal = (2 * CL_al_w) / (np.pi * AR_w)    # Wing downwash with respect to alpha, / radian
CL_al_h = CL_al_h0 * (1 - de_dal) * eta_h   # Correct tail lift curve slope

dCmf_dCL = (Kf * (Wf ** 2) * Lf) / (S_w * cw * CL_al_w)

SM = ((Xcg - X25mac) / cw) - ((CL_al_h * S_h * Lh) / (CL_al_w * S_w * cw)) + dCmf_dCL   # Static Margin estimation
print("Static margin SM = {}".format(SM))
