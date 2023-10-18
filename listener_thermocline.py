import lcm
from exlcm import ctd_t
import numpy as np
import pandas as pd

#initialize lists for depths and temps
temps = []
depths = []

#FOR DEBUG: log result to file
file1 = open(r"/home/ednavbox/data/mesobot/ctd_lcm_spoof/log.txt", "a")

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
    
    print(center_depth, file=file1)


    return(center_depth)

def my_handler(channel, data):
    msg = ctd_t.decode(data)
    
    #print readings from this heartbeat
    print("Received message on channel \"%s\"" % channel)
    print("   current index   = %s" % str(msg.index))
    print("   current depth    = %s" % str(msg.depth))
    print("   current temp = %s" % str(msg.temp))
    print("")

    #append info to depths and temps array
    temps.append(msg.temp)
    depths.append(msg.depth)

    center_depth = thermocline_id(temps, depths)
    print("thermocline center depth aproximation = %s" % str(center_depth))

lc = lcm.LCM()
subscription = lc.subscribe("CTD", my_handler)

try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass

lc.unsubscribe(subscription)
