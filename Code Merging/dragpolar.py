
import STARTG01_AVLmodel
import numpy as np
import Drag_Build_Up # python file that calculates individual components zero lift drag
import MiscDrag
import matplotlib.pyplot as plt
# import FlapDrag



class dragpolar:
    def __init__(self,AR=17.51):
        '''
        Legend for flight_stg:

        1 = clean
        2 = takeoff flaps, gear up
        3 = takeoff flaps, gear down
        4 = landing flaps, gear up
        5 = landing flaps, gear down

        '''

        CL1=[]
        CDi1=[]
        for i in range(-15,15+1):
            CL,CDi = STARTG01_AVLmodel.STARTG01_AVL(1,i,1)
            CL1 += [CL]
            CDi1 += [CDi]

        CL2=[]
        CDi2=[]
        for i in range(-15,15+1):
            CL,CDi = STARTG01_AVLmodel.STARTG01_AVL(2,i,1)
            CL2 += [CL]
            CDi2 += [CDi]

        CL3=[]
        CDi3=[]
        for i in range(-15,15+1):
            CL,CDi = STARTG01_AVLmodel.STARTG01_AVL(3,i,1)
            CL3 += [CL]
            CDi3 += [CDi]

        CL4=[]
        CDi4=[]
        for i in range(-15,15+1):
            CL,CDi = STARTG01_AVLmodel.STARTG01_AVL(4,i,1)
            CL4 += [CL]
            CDi4 += [CDi]

        CL5=[]
        CDi5=[]
        for i in range(-15,15+1):
            CL,CD = STARTG01_AVLmodel.STARTG01_AVL(5,i,1)
            CL5 += [CL]
            CDi5 += [CDi]



        # Define parameters
        S_ref = 826.13454               # reference area

        
        flight_stages = [1, 2, 3, 4, 5]

        # Flight conditions for each flight condition
        M =     [0.457, 0.183, 0.183, 0.15, 0.15]                                                 # Mach Numbers
        rho =   [0.1152e-02, 0.0023769, 0.0023769, 0.0023769, 0.0023769]                  # Densities
        V =     [275*1.6878099,  1.3*157.3,  1.3*157.3, 1.3*128.4, 1.3*128.4]     # Velocities
        mu =    [3.246e-7, 3.784e-7, 3.784e-7, 3.784e-7, 3.784e-7]                             # Dynamic Viscosities



        '''
        We need to put the following code into a for loop to get an array of Cd0 values that correspond 
        to the five flight stages. Then we can combine the CD0 values with the avl values to get our full 
        drag polars 
        '''


        # Loop that ouputs an array of CD0 values corresponding to our 5 flight stages
        CD0s = []
        for i in range(len(flight_stages)):
            all_components = Drag_Build_Up.dragDragComponents(M[i], rho[i], V[i], mu[i])
            Sumcomps = (1/S_ref) * sum([component.CalculateDrag() for component in all_components])
            C_D_leakpro = 0.07 * Sumcomps
            C_D_missing = MiscDrag.miscDrag(M[i], flight_stages[i])

            # print("Flight Stage", flight_stages[i])
            # print("Wing: ", all_components[0].CalculateDrag() / S_ref)
            # print("hTail: ", all_components[1].CalculateDrag() / S_ref)
            # print("vTail: ", all_components[2].CalculateDrag() / S_ref)
            # print("Fuselage: ", all_components[3].CalculateDrag() / S_ref)
            # print("Nacelle: ", all_components[4].CalculateDrag() / S_ref)

            CD0s.append(Sumcomps + C_D_leakpro + C_D_missing)
        # print(CD0s)

        # for i in range(len(flight_stages)):
        #     Cdflap = FlapDrag.flapDrag(flight_stages[i])

        # Cl's corresponding to the flight stages defined above
        # cl1 = 
        # cl2 = 
        # cl3 = 
        # cl4 = 
        # cl5 = 





        # plt.plot(CL1,CD1)
        # plt.plot(CL2,CD2)
        # plt.plot(CL3,CD3)
        # plt.plot(CL4,CD4)
        # plt.plot(CL5,CD5)

        # plt.figure()

        CD1=CD0s[0]+np.array(CDi1)*17.51/AR
        CD2=CD0s[1]+np.array(CDi2)*17.51/AR
        CD3=CD0s[2]+np.array(CDi3)*17.51/AR
        CD4=CD0s[3]+np.array(CDi4)*17.51/AR
        CD5=CD0s[4]+np.array(CDi5)*17.51/AR
        self.CLs = [CL1,CL2,CL3,CL4,CL5]
        self.CDs = [CD1,CD2,CD3,CD4,CD5]

    def CD(self,flight_stg_req=1,CL_req=0):
        return np.interp(CL_req,self.CLs[flight_stg_req-1],self.CDs[flight_stg_req-1])
    


# if __name__ == "__main__":
# # print('PING')
#     dpobj = dragpolar()
#     CD = dpobj.CD(flight_stg_req=1,CL_req=0)
#     print(CD)
# # plt.plot(CL1,(CD1),label='Clean')
# plt.plot(CL2,(CD2),label='Takeoff w/ Landing Gear Up')
# plt.plot(CL3,(CD3),'--',label='Takeoff w/ Landing Gear Down')
# plt.plot(CL4,(CD4),label='Landing w/ Landing Gear Up')
# plt.plot(CL5,(CD5),'--',label='Landing w/ Landing Gear Down')
# plt.xlabel('$C_L$')
# plt.ylabel('$C_D$')
# plt.title('Drag Polar')
# plt.legend()


# plt.figure()
# plt.plot(range(-15,15+1),CL1/(CD1),label='Clean')
# plt.plot(range(-15,15+1),CL2/(CD2),label='Takeoff w/ Landing Gear Up')
# plt.plot(range(-15,15+1),CL3/(CD3),'--',label='Takeoff w/ Landing Gear Down')
# plt.plot(range(-15,15+1),CL4/(CD4),label='Landing w/ Landing Gear Up')
# plt.plot(range(-15,15+1),CL5/(CD5),'--',label='Landing w/ Landing Gear Down')
# plt.xlabel('$\\alpha$')
# plt.ylabel('$C_L/C_D$')
# plt.title('$C_L/C_D$ Polar')
# plt.legend()


# plt.show()