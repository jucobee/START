import numpy as np

'''
Legend for flight_stg:

1 = clean
2 = takeoff flaps, gear up
3 = takeoff flaps, gear down
4 = landing flaps, gear up
5 = landing flaps, gear down

'''

# This function takes a mach number and an integer that correspond to a flight stage that we want to plot and returns the miscellaneous drag value
def miscDrag(M, flight_stg):
    Sref = 826.13454 # Reference area
    u = 0.08238  # radians  # Upsweep angle in radians of aft section of fuselage
    Amax = 86.1771 # Maximum cross sectional area of fuselage
    Abase = 0 # Total area of all places where the aft fuselage angle to the freestream exceeds 20 degrees. See Raymer pg. 288 for clarification
    if flight_stg == 1:
        D_gear = 0
        D_fusel = (0.139 + 0.419*((M - 0.161)**2))
        D_bluff = 0
        D_props = 0
        CDmisc = (1 / Sref) * (D_gear + D_fusel + D_bluff + D_props)

    elif flight_stg == 2:
        D_gear = 0
        D_fusel = (0.139 + 0.419*((M - 0.161)**2))
        D_bluff = 0
        D_props = 0
        CDmisc = (1 / Sref) * (D_gear + D_fusel + D_bluff + D_props)

    elif flight_stg == 3:
        D_gear = 0.9    #Raymer Table 12.5
        D_fusel = (0.139 + 0.419*((M - 0.161)**2))
        D_bluff = 0
        D_props = 0
        CDmisc = (1 / Sref) * (D_gear + D_fusel + D_bluff + D_props)

    elif flight_stg == 4:
        D_gear = 0
        D_fusel = (0.139 + 0.419*((M - 0.161)**2))
        D_bluff = 3.83 * (u**2.5) * Amax
        D_props = 0
        CDmisc = (1 / Sref) * (D_gear + D_fusel + D_bluff + D_props)

    elif flight_stg == 5:
        D_gear = 0.9
        D_fusel = (0.139 + 0.419*((M - 0.161)**2))
        D_bluff = 3.83 * (u**2.5) * Amax
        D_props = 0
        CDmisc = (1 / Sref) * (D_gear + D_fusel + D_bluff + D_props)
    
    else:
        raise ValueError("Flight stage outside the range of acceptable values") 
    
    return CDmisc