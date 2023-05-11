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
MFW = 4972  # Max fuel weight

payloads = [0, 0, 0, 0]
designPaylods = [12000, 12000, 12000, 12000]
ranges = [0, 0, 0, 0]

TDR = 1000  # Total design range (nm)
TCF = 2774.78  # Total cruise fuel (lb)
NCF = 2198
NCR = 234      # Non-cruise Range
CSR = (TDR - NCR) / TCF     # Cruise Specific Range (nm/lb)


## Harmonic Range
FW = MTOW - OEW - MPW
HDF = 0.205 * 2198
MFW2 = (1 - 0.05) * (FW - HDF) 
CFW = MFW2 - NCF
TCD = CFW * CSR
TR = TCD + NCR  # Total range
payloads[0] = MPW
payloads[1] = MPW
ranges[1] = TR

# Fuel Range #
FW = MTOW - OEW - 6200
MFW = 0.95 * (6200 - HDF)
CFW = MFW - NCF
CR = CFW * CSR
TR = CR + NCR
payloads[2] = FW
ranges[2] = TR

# Ferry #
CFW = 6200 - NCF
CR = CFW * CSR 
TR = CR + NCR
ranges[3] = TR
print(payloads)
print(ranges)


plt.figure()
plt.plot(ranges,payloads)
plt.plot(ranges, designPaylods, color = 'r', label = '50 pass @ 200 lbs each')
plt.xlabel('Range (nmi)')
plt.ylabel('Payload (lbs)')
plt.title('Payload Range')
plt.legend()
#plt.savefig('payloadrange.svg')
plt.show()

  



