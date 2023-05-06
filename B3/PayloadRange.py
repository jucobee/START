import numpy as np
import matplotlib.pyplot as plt
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
MPW2 = 21428.57
MFW = 4972  # Max fuel weight
PPF = MTOW - OEW    # Payload + Fuel

payloads = [0, 0, 0, 0]
ranges = [0, 0, 0, 0]

## Harmonic Range
FW = MTOW - OEW - 13000
NCF = 2198
HDF = 0.805 * 2198
print(FW)
MFW2 = (1 - 0.05) * (FW - HDF) 
CFW = MFW2 - 2198
TCD = 1000  # Total cruise distance (nm)
TCF = 2774.78  # Total cruise fuel (lb)
CSR = TCD / TCF     # Cruise Specific Range (nm/lb)
TCD = CFW * CSR
NCR = 234      # Non-cruise Range
TR = TCD + NCR  # Total range
payloads[0] = MPW2
payloads[1] = MPW2
ranges[1] = TR

# Fuel Range #
FW = MTOW - OEW - 5500
MFW = 0.95 * (5500 - HDF)
CFW = MFW - NCF
CR = CFW * CSR
TR = CR + NCR
payloads[2] = FW
ranges[2] = TR

# Ferry #
CFW = 5500 - NCF
CR = CFW * CSR
TR = CR + NCR
ranges[3] = TR
print(payloads)
print(ranges)

plt.figure()
plt.plot(ranges,payloads)
plt.xlabel('Range (nmi)')
plt.ylabel('Payload (lbs)')
plt.title('Payload Range')
plt.show()

  



