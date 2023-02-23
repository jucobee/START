import numpy as np

# format = [GT,GB,P1,EM1,PM,EM2,P2]
# value justification
# P1,P2 = 0.85 (Constant Speed, Gudmundsson)
# the rest = deVries
eta = [.3,.96,.9,.96,.99,.96,.9]
# [0,0,0,0,0,0,0,0,0,0]

PRatio = 0.57 # 1 is fully electric
ERatio = 0.2 # 1 is fully battery
# Constraints
'''
wp_tofl
wp_tofl_5kft
wp_climb_TO
wp_climb_TC
wp_climb_SSC
wp_climb_ERC
wp_climb_BLC_AEO
wp_climb_BLC_OEI
wp_ceil
wp_cruise_min
wp_cruise_target
wp_approach_SLp18
wp_approach_p18_5kft
wp_landing_SLp18
wp_landing_p18_5kft

'''
newLoadings = []
powerLoadings = [wp_tofl, wp_tofl_5kft, wp_climb_TO, wp_climb_TC, wp_climb_SSC, wp_climb_ERC, wp_climb_BLC_AEO, wp_climb_BLC_OEI, wp_ceil, wp_cruise_min, wp_cruise_target, np.flip(wp)[int(N/7):], np.flip(wp)[int(N/6):], np.flip(wp)[int(N/7):], np.flip(wp)[int(N/6):]]
for x in range(0,16):
    constraint = powerLoadings[x]
    loadVals = []
    for ind, y in enumerate(constraint):
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


        P_p = [0,0,0,0,0,0,0,0,0,1/y] # bhp/lbm
        PTvector = np.linalg.solve(PTmatrix,P_p)
        WPvector = PTvector**-1
        setVals = [WPvector[0], WPvector[4], WPvector[5]]
        loadVals[ind] = setVals

    newLoadings[x] = loadVals

ices = []
ems = []
bats = []
for x in range(0,15):
    for y in newLoadings[x]:
        ivals = []
        evals = []
        bvals = []
        for z in range(0, len(y)):
            ivals[z] = y[z][0]
            evals[z] = y[z][1]
            bvals[z] = y[z][2]
    
    ices[x] = ivals
    ems[x] = evals
    bats[x] = bvals


    