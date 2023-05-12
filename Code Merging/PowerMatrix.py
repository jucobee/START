import math
import numpy as np



def PowertrainMatrix(ERatio,PRatio):
    eta = [.3,.96,1,.9,.99,.9,.9]
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
    return np.linalg.solve(PTmatrix,[0,0,0,0,0,0,0,0,0,1])


if __name__ == "__main__":
    PT = PowertrainMatrix(.1,0)
    print('Fuel: {:.3f}'.format(PT[0]))
    print('GT: {:.3f}'.format(PT[1]))
    print('GB: {:.3f}'.format(PT[2]))
    print('S1: {:.3f}'.format(PT[3]))
    print('E1: {:.3f}'.format(PT[4]))
    print('BAT: {:.3f}'.format(PT[5]))
    print('E2: {:.3f}'.format(PT[6]))
    print('S2: {:.3f}'.format(PT[7]))
    print('P1: {:.3f}'.format(PT[8]))
    print('P2: {:.3f}'.format(PT[9]))
    