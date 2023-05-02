import numpy as np
import math


MRW =   # Maximum ramp weight
MTOW =  # Maximum Takeoff Weight
MLW =   # Maximum landing weight
MZFW =  # Max. zero fuel weight
OEW =   # Operating empty weight
npass = # Number of passengers
wpass = # Weight per passenger



MPW = MZFW - OEW    # Max Payload Weight
MFW =   # Max fuel weight
PPF = MTOW - OEW    # Payload + Fuel


### MISSION BREAKDOWN ###
TCD =   # Total cruise distance (nm)
TCF =   # Total cruise fuel (lb)
CSR = TCD / TCF     # Cruise Specific Range (nm/lb)
NCR =       # Non-cruise Range
NCF =       # Non-cruise fuel

FWT =       # Fuel for warmup and taxi
FNC =       # Fuel for non-cruise segments
CF =        # Contingency fuel
RF =        # Reserve fuel

