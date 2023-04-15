MTOW = 53438
Vstall = 237.981

glavity = 32.17

B = 28.25 #distance between landing gears
H = 9.87 #CG height from ground flat tires

Nf = 23.455 #foreward CG
Na =  23.565#Aft CG location from front wheel

Mf = 4.8 #fwd cg loc from rear wheel

Ma = 4.69 #aft cg loc from rear wheel

NOSEnum = 2

MAINnum = 4

#Main Wheel
StaticMax = MTOW*Na/B*(1.25)

print('SMM', StaticMax)
print('SMM per tire', StaticMax/MAINnum)

#Nose Wheels

StaticMaxNose = MTOW*Mf/B*(1.25)

print('SMN',StaticMaxNose)
print('SMN per tire',StaticMaxNose/NOSEnum)

StaticMinNose = MTOW*Ma/B*(1.25)/MAINnum

DynBrakeNose = 0.31*H*MTOW/B*(1.25)/MAINnum

#A and B values for diameter
adia = 1.63
bdia = 0.315

MWDia = adia*(StaticMax/MAINnum)**bdia

#A and B values for width
awid = 0.1043
bwid = 0.48

MWWid = awid*(StaticMax/MAINnum)**bwid


print('Main Wheel Diameter', MWDia)


print('Main Wheel Width', MWWid)

print('Ma/B', Ma/B)

print('Mf/B', Mf/B)

KEblake = (0.5)*MTOW*(Vstall**2)/32.17

print('Kinetic Energy Braking',KEblake)



