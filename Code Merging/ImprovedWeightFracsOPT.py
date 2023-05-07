from matplotlib import pyplot as plt
import numpy as np
import openmdao.api as om
from ambiance import Atmosphere

n = 11 # segments

class WeightFractionOpt(om.ExplicitComponent):
    """
    Mission Analysis
    """

    def setup(self):

        # Global Design Variable
        self.add_input('h_b', val = np.zeros(n-1))
        self.add_output('Wn_W0', val = 1)
        # self.add_input('z', val=np.zeros(2))


    def setup_partials(self):
        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
        """
        Evaluates the equation
        y1 = z1**2 + z2 + x1 - 0.2*y2
        """

        x = R*6076.11549*(1-np.cos(np.linspace(0,np.pi,n+1)))/2 # distance nodes
        h = np.concatenate([[0],inputs['h_b'],[0]],axis=0)

        # print(h)

        V_so = 1
        Wip1_Wi,Wn_W0 = WeightFraction(V_so, x,h)
        
        # outputs['Wip1_Wi'] = Wip1_Wi
        outputs['Wn_W0'] = Wn_W0

def WeightFraction(V_so, x,h):
    # print('PING')
    '''
    V_so : V_so (lmao)
    n: Number of Segments
    R: Range (nmi)
    '''
    # ASSUMED VARAIBLES:
    eta_p = 0.8
    # LoD = 30
    V_inf = 275*1.6878098571 
    S_ref = 826
    C_D0 = 0.01
    eAR = 17*.98
    K = 1/(np.pi*eAR)


    PSFC = 1.80371512e-07
    Wip1_Wi = [] # weight fractions Wi+1_Wi
    Wn_W0 = 1
    
    for i in range(n-2):
        fcon = Atmosphere(0.3048*(h[i]+h[i+1])/2)
        rho = fcon.density[0]*0.00194032033
        C_L = 2*Wn_W0*50000 / (rho * V_inf**2 * S_ref)
        LoD = C_L / (C_D0 + K*C_L**2)
        # print(C_L)
        Wip1_Wi.append(np.exp(-( (x[i+1]-x[i]) * PSFC * ( (h[i+1]-h[i])/(x[i+1]-x[i]) + 1/LoD ) )/eta_p))
        Wn_W0 = Wn_W0*Wip1_Wi[i]
    # print(h)
    print(Wn_W0)
    return Wip1_Wi,Wn_W0





# V_so = 150 * 1.7
# n = 101 # segments
# R = 1000 # nmi
# x = np.linspace(0,R*6076.11549,n+1) # distance nodes
# h = 25000*np.sin(np.pi*x/(R*6076.11549)) # distance nodes
# # print(x,h)
# # plt.plot(x,h)
# # plt.show()
# Wip1_Wi,Wn_W0 = WeightFraction(V_so, x,h)
# print(Wn_W0)
# plt.plot(Wip1_Wi)
# plt.show()


if __name__ == '__main__':
    # build the model
    prob = om.Problem()
    prob.model.add_subsystem('WFO', WeightFractionOpt(), promotes_inputs=['h_b'])

    # # define the component whose output will be constrained
    # prob.model.add_subsystem('const', om.ExecComp('g = x + y'), promotes_inputs=['x', 'y'])

    # Design variables 'x' and 'y' span components, so we need to provide a common initial
    # value for them.
    
    R = 1000 # nmi
    x = R*6076.11549*(1-np.cos(np.linspace(0,np.pi,n+1)))/2 # distance nodes
    h = 25000*np.sin(np.pi*x/(R*6076.11549)) 
    # prob.model.set_input_defaults('x', x)
    prob.model.set_input_defaults('h_b', h[1:-1])

    # setup the optimization 
    prob.driver = om.ScipyOptimizeDriver()
    prob.driver.options['optimizer'] = 'SLSQP'
    prob.driver.options['maxiter'] = 1e5
    prob.driver.options['tol'] = 1e-16

    prob.model.add_design_var('h_b', lower=0, upper=25000)
    # prob.model.add_design_var('y', lower=-50, upper=50)
    prob.model.add_objective('WFO.Wn_W0',scaler=-1)
    
    # # to add the constraint to the model
    # prob.model.add_constraint('const.g', lower=0, upper=10.)

    prob.setup()
    prob.run_driver();

    # print(x,h)
    plt.plot(x,np.concatenate([[0],prob.get_val('h_b'),[0]],axis=0))
    plt.figure()
    # plt.plot(x,np.concatenate([[0],prob.get_val('h_b'),[0]],axis=0))
    plt.show()
    
