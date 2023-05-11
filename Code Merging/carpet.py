import math
import numpy as np
from dragpolar import dragpolar
import matplotlib.pyplot as plt
from labellines import labelLines # pip install matplotlib-label-lines

def carpet(f1,f2,x1,x2,n,N,labelx1,labelx2):
    '''
    n = number of major ticks
    N = number of points in total
    '''
    plt.figure(figsize=(8,7))
    x1n = np.linspace(x1[0],x1[1],n)
    x2n = np.linspace(x2[0],x2[1],n)

    x1N = np.linspace(x1[0],x1[1],N)
    x2N = np.linspace(x2[0],x2[1],N)

    for i in range(n):

        y1 = []
        y2 = []
        for j in range(N): # fix x1 first
            y1.append(f1(x1n[i],x2N[j]))
            y2.append(f2(x1n[i],x2N[j]))
        plt.plot(y1,y2,color='#1F54EA',label='{} = {:.3f}'.format(labelx1,x1n[i]))

    for i in range(n):
        y1 = []
        y2 = []
        for j in range(N): # fix x2
            y1.append(f1(x1N[j],x2n[i]))
            y2.append(f2(x1N[j],x2n[i]))
        plt.plot(y1,y2,color='#7CC646',label='{} = {:.3f}'.format(labelx2,x2n[i]))
    
    labelLines(plt.gca().get_lines(), zorder=2.5,fontsize = 7)
        
if __name__ == "__main__":

    # FIRST CARPET PLOT: 
    # OBJECTIVES: L/D_cruise, MTOW
    # PARAMETERS: Cruise Velocity, AR_e

    def f1(AR,M):
        return np.pi*AR/0.1/2*M
    def f2(AR,M):
        CL = np.sqrt(0.1*np.pi*AR)
        return CL/2*1.4*0.0010651*M**2

    x1= 1.68780986*np.array([275.0,350.0],float) # Cruise Velocity
    labelx1 = 'MTOW'
    x2= [17.51-2,17.51+2] # AR
    labelx2 = 'AR_e'
    n=6
    N=101
    carpet(f1,f2,x1,x2,n,N,labelx1,labelx2)
    plt.show()