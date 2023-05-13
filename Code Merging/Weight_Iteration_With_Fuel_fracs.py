import numpy as np
import math
from ImprovedWeightFracs import ImprovedWeightFracs
from ImprovedWeightFracsV2 import MissionFractions
from PreliminarySizing import PrelimSize
import openmdao.api as om
import os 

'''
Weight categories:
wing
horizontal tail
vertical tail
fuselage
engine
crew
fuel
battery
passengers
baggage/cargo
nose landing gear
main landing gear
'''
def WeightBuildUp(WS,WP,WP_GT,WP_EM1,PHIvec,V_cruise=1.68780986*275,ARw=17.5):
    class WeightComponent:
        def __init__(self, W=0, xCG=0, yCG=0, zCG=0,Ixx=0,Iyy=0,Izz=0,Ixz=0,Ixy=0,Iyz=0):
            self.weight = W
            self.xCG = xCG
            self.yCG = yCG
            self.zCG = zCG
            self.Ixx = Ixx
            self.Iyy = Iyy
            self.Izz = Izz
            self.Ixz = Ixz
            self.Ixy = Ixy
            self.Iyz = Iyz

    MTOW = 46000
    pilots = 2 # Number of pilots
    attend = 1  # Number of attendants
    crew = pilots + attend # Total crew
    passengers = 50 # Number of passengers
    wt_crew = 190 # Weight of each crew member, lbs
    wt_passengers = 200 # Weight of each passenger, lbs
    wt_crew_baggage = 30 # Weight of baggage for each crew member, lbs
    wt_pass_baggage = 40 # Weight of baggage for each passenger, lbs


    tol = 1
    err = 1.1
    while err > tol:
        diam = 9

        Wcrew = wt_crew * crew  # Total weight of crew
        
        Wpassengers = passengers * wt_passengers  # Total weight of passengers
        Wbaggage = (wt_crew_baggage * crew) + (wt_pass_baggage * passengers)  # Total weight of baggage in hold

        

        Wb_W0,Wf_W0 = MissionFractions(MTOW,WS,WP,PHIvec,R_req=1000,Rmax=1000)

        Wfuel=Wf_W0*MTOW
        Wbattery=Wb_W0*MTOW

        #Wbattery = MTOW * 0.11  # Battery weight
        P_total = MTOW/WP
        P_GT = MTOW/WP_GT
        P_EM1 = MTOW/WP_EM1
        

        
        gas_turb = (((P_GT / 2)**0.9306) * 10**(-0.1205)) * 2  # Total gas turbine engine weight
        EM1 = (P_EM1 / (5.22*1.34102209/2.20462262))  # Total electric motor weight, 5.22 kW/kg --> hp/lbf
        Wengine = 2.575 * (((gas_turb)/2)**0.922) * 2 + EM1 # TOTAL ENGINE WEIGHT
        
        

        Sw = MTOW/WS   # Wing area
        bw = np.sqrt(Sw*ARw) # Wing Span
        # print('span',Sw,ARw,bw)
        # bw = 115.76 # Wing span
        Wfw = Wfuel  # Weight of fuel in wing
        # ARw = bw**2/Sw  # Aspect ratio of wing
        Gammaw = 5 * (np.pi / 180)   # Wing sweep angle
        lambdaw = 0.4 # Wing taper ratio
        tcw = 0.16    # Thickness to chord ratio of wing root 
        Nz = 2.5 * 1.5    # Ultimate load factor; 1.5 x limit load factor
        Wdg = MTOW  # Design gross weight
        q = (0.0010651 * (V_cruise)** 2) / 2   # Dynamic pressure at cruise
        Scsw = 0.2 * Sw
        W_strut = 394 #approximate wing strut weight <---????

        Wwing = 0.0051 * ((Wdg * Nz)**0.557) * (Sw**0.649) * (ARw**0.5) * (tcw**-0.4) * ((1+lambdaw)**0.1) * ((np.cos(Gammaw))**-1) * (Scsw**0.1) * 0.9 + W_strut

        Sht = Sw/826.134*94.19  # Area of horizantle tail
        Gammaht = 16 * (np.pi / 180)  # Sweep angle of horizontal tail
        lambdah = 0.4  # Taper ratio of horizontal tail
        tch = 0.14      # Thickness to chord ratio of horizontal tail root
        bh = 20.36
        ARh = bh**2/Sht      # Aspect ratio of horizontal tail
        Fw = 4.5
        Lt = 40.5
        Ky = 0.3 * Lt
        Se = 0.1 * Sht
        Wht = 0.0379 * (1.143) * ((1+(Fw/bh))**-0.25) * (Wdg**0.639) * (Nz**0.1) * (Sht**0.75) * (Lt**-1) * (Ky**0.704) * ((np.cos(Gammaht))**-1) * (ARh**0.166) * ((1+(Se/Sht))**0.1) * 0.83

        Svt = Sw/826.134*146.09  # Area of vertical tail
        Gammavt = 30 * (np.pi / 180)  # Sweep angle of vertical tail
        lambdavt = 0.8 # Taper ratio of vertical tail
        tcv = 0.14  # Thickness to chord ratio of vertical tail root
        ARvt = 1.127 # Aspect ratio of vertical tail
        Wvt = 0.0026 * (2**0.225) * (Wdg**0.556) * (Nz**0.536) * (Lt**-0.5) * (Svt**0.5) * (Lt**0.875) * ((np.cos(Gammavt))**-1) * (ARvt**0.35) * (tcv**-0.5) * 0.83

        Lt = 40.5  # Tail length; wing quarter-MAC to tail quarter-MAC, ft
        L = 79   # Fuselage structural length, ft
        D = 0.5    # Fuselage structural depth, ft
        Sf = 1775.85   # Fuselage wetted area, ft^2
        Vpr = 3919.81   # Volume of pressurized area
        Wpress = 11.9 + (Vpr * 8)**0.271
        Kd = 1.06
        Klg = 1.12
        Kws = 0.75 * ((1+2*lambdaw)/(1+lambdaw))*(bw*np.tan(Gammaw/L))

        Wfuselage = 0.3280 * (Kd) * (Klg) * ((Wdg * Nz)**0.5) * (L**0.25) * (Sf**0.302) * ((1+Kws)**0.04) * ((L/D)**0.1) * 0.9

        Nl = 3.8 * 1.5  # ultimate landing load factor
        Wl = MTOW - (Wfuel)   # Landing design gross weight
        Lm = 60  # Length of main landing gear, in
        Ln = 54  # Lenght of nose landing gear, in
        Nmw = 8
        Nnw = 2
        Nmss = 4
        Vstall = 141

        Wmainlanding = 0.0106 * (Wl**0.888) * (Nl**0.25) * (Lm**0.4) * (Nmw**0.321) * (Nmss**-0.5) * (Vstall ** 0.1)
        Wnoselanding = 0.032 * (Wl**0.646) * (Nl**0.2) * (Ln**0.5) * (Nnw**0.45)


        Kng = 1 # 1.017 for pylon-mounted nacelle; = 1.0 otherwise
        NLt = 20.5 # nacelle length, ft
        Nw = 2.5 # nacelle width, ft
        Wec = Wengine + 0 # weight of engine and contents, lb (per nacelle)
        Nen = 2 # number of engines (total for aircraft)
        Sn = 553.299/2 # nacelle wetted area, ft2
        Wnacellegroup = 0.6724*Kng*NLt**.1*Nw**0.294*Nz**0.119*Wec**0.611*Nen**0.984*Sn**0.224

        Lec = 30 #routing distance from engine front to cockpit,ft
        Wenginecontrols = 5*Nen+0.80*Lec

        Wen = Wengine + 0 # engine weight, each, lb
        Wstarter = 49.19*(Nen*Wen/1000)**0.541

        Vt= 125.036*7.48051948 # total fuel volume, gal
        Vi= 125.036*7.48051948 # integral tanks volume, gal
        Vp= 0 # self-sealing tanks, gal
        Nt= 4 # number of fuel tanks
        Wfuelsystem = 2.405*Vt**.606*(1+Vi/Vt)**-1*(1+Vp/Vt)*Nt**0.5

        Nf=7 # number of separate functions performed by surface controls, including rudder, aileron, elevator, flaps, spoiler, and speed brakes
        Nm=2 # number of surface controls driven by mechanical actuation instead of hydraulics
        Scs=200 # total control surface area, ft2
        Iyaw=1 # yawing moment of inertia, lb*ft2
        Wflightcontrols = 145.9*Nf**0.554*(1+Nm/Nf)**-1*Scs**.2*(Iyaw*10**-16)**.07

        WAPUuninstalled= 115 # weight of APU, uninstalled
        WAPUinstalled = 2.2*WAPUuninstalled

        Kr= 1 # 1.133 if reciprocating engine; = 1.0 otherwise
        Ktp= 0.793 # 0.793 if turboprop; = 1 .0 otherwise
        Nc= 3 # number of crew 
        Lf= 79 # total fuselage length
        Bw= 115.76 # wingspan
        Winstruments = 4.509*Kr*Ktp*Nc**.541*Nen*(Lf+Bw)**0.5

        Whydraulics=0.2673*Nf*(Lf+Bw)**.937

        Rkva=50 # system electrical rating, typically 40-60 for transports, kV · A 
        La=80 # electrical routing distance, generators to avionics to cockpit, ft
        Ngen=2 # number of generators (typically = Nen)
        Welectrical=7.291*Rkva**0.782*La**.346*Ngen**.1

        Wuav=1000 # uninstalled avionics weight, lb (typically = 800-1400 lb)
        Wavionics=1.73*Wuav**.983

        Wc=Wbaggage+0 # maximum cargo weight, lb
        Wfurnishings=0.0577*Nc**.1*Wc**.393*Sf**.75

        Np=53 # number of personnel onboard (crew and passengers)
        Wairconditioning=62.36*Np**.25*(Vpr/1000)**.604*Wuav**.1

        Wantiice=.002*Wdg

        Whandlinggear=(3.0*10**-4)*Wdg


        # xCG values in feet measured from leading edge of wing(Calculated if leading edge of wing moved forward by 2.1ft)
        wingxCG = 5.41 * 0.25   # At quarter chord of wing
        fuelxCG = 5.41 * 0.35      # Fuel sits about a third of the way along the chord of the wing
        passengersxCG = 4.8 # Passenger weight slightly behind wing LE
        crewxCG = -4.77
        baggagexCG = 15.69
        batteryxCG = 5.41*0.55
        enginexCG = 0.0
        htxCG = 48.17
        vtxCG = 41.854
        noselandingxCG = -20.858
        mainlandingxCG = 12
        fuselagexCG = 6.007
        nacellexCG = 4.708    # Nacelle group cg sits almost level with the wing leading edge
        engcontxCG = 10.021
        starterxCG = 0.0
        fuelsysxCG = 5.41 * 0.25
        flightcontxCG = 10.021
        APUxCG = 46.717
        instrumentsxCG = -26.172
        hydraulicsxCG = 22.3
        electricalxCG = -0.805
        avionicsxCG = -26.172
        furnishingsxCG = 4.8
        airconxCG = 3.461
        antiicexCG = 0
        handlinggearxCG = 0
        
        
        W_wing = WeightComponent(Wwing,wingxCG)
        W_fuel = WeightComponent(Wfuel,fuelxCG)
        W_passengers = WeightComponent(Wpassengers,passengersxCG)
        W_crew = WeightComponent(Wcrew,crewxCG)
        W_baggage = WeightComponent(Wbaggage,baggagexCG)
        W_battery = WeightComponent(Wbattery,batteryxCG)
        W_engine = WeightComponent(Wengine,enginexCG)
        W_ht = WeightComponent(Wht,htxCG)
        W_vt = WeightComponent(Wvt,vtxCG)
        W_noselanding = WeightComponent(Wnoselanding,noselandingxCG)
        W_mainlanding = WeightComponent(Wmainlanding,mainlandingxCG)
        W_fuselage = WeightComponent(Wfuselage,fuselagexCG)
        W_nacellegroup = WeightComponent(Wnacellegroup,nacellexCG)
        W_enginecontrols = WeightComponent(Wenginecontrols,engcontxCG)
        W_starter = WeightComponent(Wstarter,starterxCG)
        W_fuelsystem = WeightComponent(Wfuelsystem,fuelsysxCG)
        W_flightcontrols = WeightComponent(Wflightcontrols,flightcontxCG)
        W_APUinstalled = WeightComponent(WAPUinstalled,APUxCG)
        W_instruments = WeightComponent(Winstruments,instrumentsxCG)
        W_hydraulics = WeightComponent(Whydraulics,hydraulicsxCG)
        W_electrical = WeightComponent(Welectrical,electricalxCG)
        W_avionics = WeightComponent(Wavionics,avionicsxCG)
        W_furnishings = WeightComponent(Wfurnishings,furnishingsxCG)
        W_airconditioning = WeightComponent(Wairconditioning,airconxCG)
        W_antiice = WeightComponent(Wantiice,antiicexCG)
        W_handlinggear = WeightComponent(Whandlinggear,handlinggearxCG)

        weightComponents = [] # component list
        weightComponents.append(W_wing           )
        weightComponents.append(W_fuel           )
        weightComponents.append(W_passengers     )
        weightComponents.append(W_crew           )
        weightComponents.append(W_baggage        )
        weightComponents.append(W_battery        )
        weightComponents.append(W_engine         )
        weightComponents.append(W_ht             )
        weightComponents.append(W_vt             )
        weightComponents.append(W_noselanding    )
        weightComponents.append(W_mainlanding    )
        weightComponents.append(W_fuselage       )
        weightComponents.append(W_nacellegroup   )
        weightComponents.append(W_enginecontrols )
        weightComponents.append(W_starter        )
        weightComponents.append(W_fuelsystem     )
        weightComponents.append(W_flightcontrols )
        weightComponents.append(W_APUinstalled   )
        weightComponents.append(W_instruments    )
        weightComponents.append(W_hydraulics     )
        weightComponents.append(W_electrical     )
        weightComponents.append(W_avionics       )
        weightComponents.append(W_furnishings    )
        weightComponents.append(W_airconditioning)
        weightComponents.append(W_antiice        )
        weightComponents.append(W_handlinggear   )
        
        # components = dict(zip(['Wwing ', ' Wfuel ', ' Wpass ', ' Wcrew ', ' Wbaggage ', ' Wbattery ', ' Wengine ', ' Wht ', ' Wvt ', ' Wfusel ', ' W_noselanding ', ' W_mainlanding ', 'W_nacellegroup ', ' W_enginecontrols ', ' W_starter ', ' W_fuelsystem ', ' W_flightcontrols ', ' W_APUinstalled ', ' W_instruments ', ' W_hydraulics ', ' W_electrical ', ' W_avionics ', ' W_furnishings ', ' W_airconditioning ', ' W_antiice ', ' W_handlinggear'],
        #                 [Wwing , Wfuel , Wpassengers , Wcrew , Wbaggage , Wbattery , Wengine , Wht , Wvt , Wfusel , W_noselanding , W_mainlanding ,W_nacellegroup , W_enginecontrols , W_starter , W_fuelsystem , W_flightcontrols , W_APUinstalled , W_instruments , W_hydraulics , W_electrical , W_avionics , W_furnishings , W_airconditioning , W_antiice , W_handlinggear]))
        # componentsxCG = dict(zip(['wingxCG','fuelxCG','passengersxCG','crewxCG','baggagexCG','batteryxCG','enginexCG','horizontalxCG','verticalxCG','noselandingxCG','mainlandingxCG','fuselagexCG','nacellexCG','engcontxCG','starterxCG','fuelsysxCG','flightcontxCG','APUxCG','instrumentsxCG','hydraulicsxCG','electricalxCG','avionicsxCG','furnishingsxCG','airconxCG','antiicexCG','handlinggearxCG'],
        #                         [wingxCG,fuelxCG,passengersxCG,crewxCG,baggagexCG,batteryxCG,enginexCG,horizontalxCG,verticalxCG,fuselagexCG,noselandingxCG,mainlandingxCG,nacellexCG,engcontxCG,starterxCG,fuelsysxCG,flightcontxCG,APUxCG,instrumentsxCG,hydraulicsxCG,electricalxCG,avionicsxCG,furnishingsxCG,airconxCG,antiicexCG,handlinggearxCG]))
        
        # print(components)
        MTOWn=0
        for comp in weightComponents:
            MTOWn += comp.weight

        xCG=0
        for comp in weightComponents:
            xCG += comp.weight*comp.xCG
        xCG = xCG/MTOWn

        err = abs(MTOWn - MTOW)
        MTOW = MTOWn
    print('MTOW: {:.3f}'.format(MTOW))
    print('GT: {:.3f} hp, {:.3f} kg\nEM: {:.3f} hp, {:.3f} kg\nW_engine: {:.3f} hp, {:.3f} kg'.format(P_GT,gas_turb,P_EM1,EM1,P_total,Wengine))
    print('Battery Weight: {:.3f}, Fuel Weight: {:.3f}'.format(Wbattery,Wfuel))
    print('Wing Area: {:.3f}'.format(Wbattery,Wfuel))
    print(xCG)
    if math.isnan(MTOW):
        return (1e7,1e7)
    else:
        return MTOW,Wfuel


    # # print('AAA')
    # name='STARTG01'
    # cd = os.getcwd() # Get current location of python script
    # print(cd)
    # with open('{}\\Planes\\{}\\{}.mass'.format(cd,name,name),'w') as file:
    #     file.write('Lunit = 1 ft\nMunit = 0.03108486167 slug\nTunit = 1.0 s\n\n')
    #     for comp in weightComponents:
    #         file.write('{} {} {} {} {} {} {} {} {}\n'.format(comp.weight,comp.xCG,comp.yCG,comp.zCG,comp.Ixx,comp.Iyy,comp.Izz,comp.Ixz,comp.Ixy,comp.Iyz))

    # file.writelines(ComponentHeader('MASS DEFINTION'))
    # file.write(SectionHeader('MASS DEFINTION'))
    
def WeightEstimation(WS,WP,WP_GT,WP_EM1,PHIvec,V_cruise=1.68780986*275,ARw=17.5):

    Wb_W0,Wf_W0 = MissionFractions(1,WS,WP,PHIvec,R_req=1000,Rmax=1000)

    # Number of pilots
    pilots = 2
    # Number of attendants
    attend = 1
    # Total crew
    crew = pilots + attend
    # Number of passengers
    passengers = 50 # lbm
    # Weight of each crew member in lbs
    wt_crew = 190 # lbm
    # Weight of each passenger in lbs
    wt_passengers = 200 # lbm
    # Weight of baggage for each crew member in lbs
    wt_crew_baggage = 30 # lbm
    # Weight of baggage for each passenger in lbs
    wt_pass_baggage = 40 # lbm
    # Total payload weight
    W_payload = (passengers * (wt_passengers + wt_pass_baggage)) 
    # print(W_payload)
    # Total crew weight
    W_crew = crew * (wt_crew + wt_crew_baggage)
    
    W0_list = []
    W0 = 50000
    A = 1.20212 # from regression model
    C = -0.100611
    error = 1
    delta  = (2 * error)

    while delta > error:
        W0_list.append(W0)
        # defined from direct ratios
        W_wing_W0 = 10/WS # wing loading
        # iterables
        We_W0 = A*W0**C # everything else


        P_total = W0/WP
        P_GT = W0/WP_GT
        P_EM1 = W0/WP_EM1
        
        gas_turb = (((P_GT / 2)**0.9306) * 10**(-0.1205)) * 2  # Total gas turbine engine weight
        EM1 = (P_EM1 / (5.22*1.34102209/2.20462262))  # Total electric motor weight, 5.22 kW/kg --> hp/lbf
        W_engine = gas_turb+EM1
        # Wengine = 2.575 * (((gas_turb)/2)**0.922) * 2 + EM1 # TOTAL ENGINE WEIGHT

        # W_engine = 2*((W0/WP_ICE/2)**0.9306*10**-0.1205 + (W0/WP_EM1/2)/(5.22*1.34102209/2.20462262)) # lbm, 5.2kW/kg electric engine from Martins
        # W_pg = 1.35*(W_engine+0.24*W0*(1/WP_ICE+1/WP_EM1))
        W0_New = (W_crew + W_payload + W_engine) / (1 - We_W0 - W_wing_W0 - Wf_W0 - Wb_W0 )
        delta = abs((W0_New - W0)/W0_New)
        W0 = W0_New
    W_empty_W0 = (1-Wf_W0)

    print('MTOW: {:.3f}'.format(W0))
    print('GT: {:.3f}, EM: {:.3f}, W_engine: {:.3f}'.format(P_GT,P_EM1,P_total))
    print('Battery Weight: {:.3f}, Fuel Weight: {:.3f}'.format(Wb_W0*W0,Wf_W0*W0))
    if math.isnan(W0):
        return (1e7,1e7)
    else:
        return W0,Wf_W0*W0

class BlockFuelOPT(om.ExplicitComponent):
    """
    Mission Analysis
    """

    def setup(self):
        # Global Design Variable
        self.add_input('PHIvec', val = np.array([[0, 0], # Taxi
            [0.4, 0.4],      # Takeoff
            [0.36, 0.36],        # Climb
            [0, 0],            # Cruise
            [0, 0],            # Descent
            [0, 0],            # Divert Climb
            [0, 0],            # Divert
            [0, 0],            # Divert First Descent
            [0, 0],            # Loiter
            [0, 0],            # Divert Final Descent
            [0, 0]],           # Landing
            float))
        self.add_output('Wf', val = 0)
        # self.add_input('z', val=np.zeros(2))


    def setup_partials(self):
        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
        """
        Evaluates block fuel
        """

        WS,WP,WP_GT,WP_EM1 = PrelimSize(inputs['PHIvec'])
        # MTOW,Wfuel = WeightBuildUp(WS,WP,WP_GT,WP_EM1,inputs['PHIvec'],V_cruise=1.68780986*275,ARw=17.51)
        MTOW,Wfuel = WeightBuildUp(WS,WP,WP_GT,WP_EM1,inputs['PHIvec'],V_cruise=1.68780986*275,ARw=17.51)
        print(inputs['PHIvec'])
        print('Wfuel {:.3f}'.format(Wfuel))
        # outputs['Wip1_Wi'] = Wip1_Wi
        outputs['Wf'] = Wfuel

if __name__ == "__main__":
    # # build the model
    # prob = om.Problem()
    # prob.model.add_subsystem('BFOPT', BlockFuelOPT(), promotes_inputs=['PHIvec'])

    # prob.model.set_input_defaults('PHIvec', np.array([[0, 0], # 0: Taxi
    #         [0.4, 0.4],      # Takeoff
    #         [0.36, 0.36],        # Climb
    #         [0, 0],            # 3: Cruise
    #         [0, 0],            # 4: Descent
    #         [0, 0],            # 5: Divert Climb
    #         [0, 0],            # 6: Divert
    #         [0, 0],            # 7: Divert First Descent
    #         [0, 0],            # 8: Loiter
    #         [0, 0],            # 9: Divert Final Descent
    #         [0, 0]],           # 10: Landing
    #         float))
    # # prob.model.set_input_defaults('PHIvec', np.array([[0.06369971, 0.31903651],
    # #         [0.96385417, 0.71884486],
    # #         [0.96173562, 0.00945743],
    # #         [0.21274627, 0.78550783],
    # #         [0.99974305, 0.00426302],
    # #         [0.00117523, 0.16083328],
    # #         [0.04747238, 0.07949061],
    # #         [0.127311  , 0.25506034],
    # #         [1.        , 0.08457946],
    # #         [0.3926251 , 0.07309257],
    # #         [0.38544507, 0.05145903]],           # 10: Landing
    # #         float))

    # # setup the optimization 
    # prob.driver = om.ScipyOptimizeDriver()
    # prob.driver.options['optimizer'] = 'SLSQP'
    # prob.driver.options['maxiter'] = 1e5
    # prob.driver.options['tol'] = 1e-16

    # prob.model.add_design_var('PHIvec', lower=0, upper=1)
    # prob.model.add_objective('BFOPT.Wf',scaler=1)
    

    # prob.setup()
    # prob.run_driver();
    
    # WS = 69.36423531558572
    # WP = 8.564498702867692
    PHIvec = np.array([[0, 0], # 0: Taxi
            [3.77133831e-01, 3.77133831e-01],      # 1: Takeoff
            [1.76550631e-05, 3.61126603e-01],        # 2: Climb
            [0, 0],            # 3: Cruise
            [0, 0],            # 4: Descent
            [0, 0],            # 5: Divert Climb
            [0, 0],            # 6: Divert
            [0, 0],            # 7: Divert First Descent
            [0, 0],            # 8: Loiter
            [0, 0],            # 9: Divert Final Descent
            [0, 0]],           # 10: Landing
            float)
    
    WS,WP,WP_GT,WP_EM1 = PrelimSize(PHIvec,verbose=False)
    WeightBuildUp(WS,WP,WP_GT,WP_EM1,PHIvec,V_cruise=1.68780986*275,ARw=17.5)
