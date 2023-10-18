import lcm
from exlcm import ctd_t
import pandas as pd
import numpy as np
import math
import time

#file path
filename = r'/home/ednavbox/data/mesobot/ctd_lcm_spoof/mesobot074_short.csv'
df = pd.read_csv(filename)
temps = df.iloc[:, 0].to_numpy()
depths = df.iloc[:, 1].to_numpy()

lc = lcm.LCM()

for i in range(0, len(temps)):
	msg = ctd_t()
	msg.index =  i
	msg.depth = depths[i]
	msg.temp = temps[i]
	time.sleep()

	lc.publish("CTD", msg.encode())
