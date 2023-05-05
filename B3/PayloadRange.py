import numpy as np
import math

# 53437.91767045 53437.80789773 51823.40860772 49048.624581
#  48709.02414001 48465.47901931
MRW = 53437.91767045# Maximum ramp weight
MTOW = 53437.80789773   # Maximum Takeoff Weight
MLW = 49048.624581  # Maximum landing weight
MZFW = 48465.47901931 # Max. zero fuel weight
OEW =  35754.95079960673 # Operating empty weight
npass = 50# Number of passengers
wpass =  200 + 40# Weight per passenger



MPW = MZFW - OEW    # Max Payload Weight
MFW = 3420.54  # Max fuel weight
PPF = MTOW - OEW    # Payload + Fuel


### MISSION BREAKDOWN ###
TCD = 1000  # Total cruise distance (nm)
TCF = 2774.78  # Total cruise fuel (lb)
CSR = TCD / TCF     # Cruise Specific Range (nm/lb)
NCR = 234      # Non-cruise Range
NCF = 126.9      # Non-cruise fuel


