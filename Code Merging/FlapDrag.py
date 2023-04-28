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
    Sw =  # Wing reference area
    Sf =  # Area of flapped portion
    Cfc = # Percentage of chord that is the flap portion
    dfl = # Landing flap deflection angle in RADIANS
    dft = # Takeoff flap deflection angle in RADIANS
    if flight_stg == 1:
        CDflaps = 0
        return CDflaps
    elif flight_stg == 2:
        CDflaps = 0.9*(Cfc)**1.38 * (Sf/Sw) * (np.sin(dft))**2
        return CDflaps
    elif flight_stg == 3:
        CDflaps = 0.9*(Cfc)**1.38 * (Sf/Sw) * (np.sin(dft))**2
        return CDflaps
    elif flight_stg == 4:
        CDflaps = 0.9*(Cfc)**1.38 * (Sf/Sw) * (np.sin(dfl))**2
        return CDflaps
    elif flight_stg == 5:
        CDflaps = 0.9*(Cfc)**1.38 * (Sf/Sw) * (np.sin(dfl))**2
        return CDflaps