import time
from lcm import LCM
from mesobot_lcmtypes.raw import string_t
from mesobot_lcmtypes.raw import floats_t
from mesobot_lcmtypes.marine_sensor import ctd_t
import numpy as np #for algorithm
import pandas as pd #for algorithm

#initialize lists for depths and temps
temps = []
depths = []
index = 0 #counts number of message from CTD channel

#thermocline ID function
def thermocline_id(temps, depths):
    ##filtering for points at depths greater than 3 m
    #depth_cutoff = 2.0
    #temps = temps[depths > depth_cutoff]
    #depths = depths[depths > depth_cutoff]

    #fit polynomial
    coef = np.polyfit(temps,depths,5)    
    poly1d_fn = np.poly1d(coef) 

    #take derivatives
    deriv1 = poly1d_fn.deriv()
    deriv2 = deriv1.deriv()

    #find roots of second derivative and filter out erroneous imaginary solutions
    roots2 = np.roots(deriv2)
    realroots2 = np.unique(roots2.real[abs(roots2.imag)<1]) # where I chose 1 as a threshold and seelct only unique vals
    center_depth = 0

    #choose which root is thermocline center
    if np.size(realroots2) == 3:
        center_temp = realroots2[1]
        center_depth = poly1d_fn(center_temp)
    elif np.size(realroots2) == 2:
        middle_temp =(np.max(temps) + np.min(temps))/2 #midpoint of temperature range
        center_temp = realroots2[np.abs(realroots2 - middle_temp).argmin()]
        center_depth = poly1d_fn(center_temp)
    
    return(center_depth)


def my_handler(channel, data):
    msg = ctd_t.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print("   utime   = %s" % str(msg.utime))
    print("   temp    = %.6s" % str(msg.sea_water_temperature))
    print("   depth    = %.6s" % str(msg.depth))
    print("")

    #append info to depths and temps array
    temps.append(msg.sea_water_temperature)
    depths.append(msg.depth)

    center_depth = thermocline_id(temps, depths)
    print("thermocline center depth aproximation = %.6s" % str(center_depth))


lc  = LCM()
subscription = lc.subscribe("CTD", my_handler)

try:
    while True:
        lc.handle()

except KeyboardInterrupt:
    pass

lc.unsubscribe(subscription)
