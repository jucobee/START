import numpy as np

'''
Legend for flight_stg:

1 = clean
2 = takeoff flaps, gear up
3 = takeoff flaps, gear down
4 = landing flaps, gear up
5 = landing flaps, gear down

'''

def flapDrag(flight_stg):
    # Sw =  # Wing reference area
    # Sf =  # Area of flapped portion
    # Cfc = # Percentage of chord that is the flap portion
    dfl = 35 # Landing flap deflection angle in RADIANS
    dft = 15 # Takeoff flap deflection angle in RADIANS
    if flight_stg == 1:
        CDflaps = 0
        return CDflaps
    elif flight_stg == 2:
        CDflaps = 0.0023*dft*.6
        return CDflaps
    elif flight_stg == 3:
        CDflaps = 0.0023*dft*.6
        return CDflaps
    elif flight_stg == 4:
        CDflaps = 0.0023*dfl*.6
        return CDflaps
    elif flight_stg == 5:
        CDflaps = 0.0023*dfl*.6
        return CDflaps