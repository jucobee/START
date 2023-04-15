MTOW = 55029.81867528567

Vstall = 1

glavity = 32.17

B = 32.25 #distance between landing gears
H = 9.87 #CG height from ground flat tires

Nf = 23.455 #foreward CG
Na =  23.565#Aft CG location from front wheel

Mf = 8.8 #fwd cg loc from rear wheel

Ma = 8.69 #aft cg loc from rear wheel

NOSEnum = 2

MAINnum = 4

#Main Wheel
StaticMax = MTOW*Na/B*(1.25)/NOSEnum

print('SMM', StaticMax)

#Nose Wheels

StaticMaxNose = MTOW*Mf/B*(1.25)/MAINnum

print('SMN',StaticMaxNose)

StaticMinNose = MTOW*Ma/B*(1.25)/MAINnum

DynBrakeNose = 0.31*H*MTOW/B*(1.25)/MAINnum

adia = 1.63
bdia = 0.315

MWDia = adia*(StaticMax)**bdia


awid = 0.1043
bwid = 0.48

MWWid = awid*(StaticMax)**bwid


print('Main Wheel Diameter', MWDia)


print('Main Wheel Width', MWWid)


KEblake = (0.5)*MTOW*(Vstall**2)/32.17