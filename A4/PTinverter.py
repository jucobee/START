import numpy as np


Pf_W = 1 / 

# value justification
# P1,P2 = 0.85 (Constant Speed, Gudmundsson)
# the rest = deVries
# format = [GT,GB,P1,EM1,PM,EM2,P2]
eta = [.3,.96,.9,.96,.99,.96,.9]
# [0,0,0,0,0,0,0,0,0,0]

PRatio = 0 # 1 is fully electric
ERatio = 0.5 # 1 is fully battery
PTmatrix = np.array([[-eta[0],1,0,0,0,0,0,0,0,0],
                    [0,-eta[1],1,1,0,0,0,0,0,0],
                    [0,0,0,-eta[2],0,0,0,0,1,0],
                    [0,0,-eta[3],0,1,0,0,0,0,0],
                    [0,0,0,0,-eta[4],-eta[4],1,0,0,0],
                    [0,0,0,0,0,0,-eta[5],1,0,0],
                    [0,0,0,0,0,0,0,-eta[6],0,1],
                    [ERatio,0,0,0,0,ERatio-1,0,0,0,0],
                    [0,0,0,PRatio,0,0,0,PRatio-1,0,0],
                    [0,0,0,0,0,0,0,0,1,1]])

print(PTmatrix)


P_p = [0,0,0,0,0,0,0,0,0, 1 / ] # bhp
PTvector = np.linalg.solve(PTmatrix,P_p)
print(PTvector)

print('Power Supplied by Fuel: {:.3f} bhp'.format(PTvector[0]))
print('Power Supplied by Battery: {:.3f} bhp'.format(PTvector[5]))