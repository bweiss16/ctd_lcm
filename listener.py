import lcm

from exlcm import ctd_t

def my_handler(channel, data):
    msg = ctd_t.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print("   index   = %s" % str(msg.index))
    print("   depth    = %s" % str(msg.depth))
    print("   temp = %s" % str(msg.temp))
    print("")

lc = lcm.LCM()
subscription = lc.subscribe("CTD", my_handler)

try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass

lc.unsubscribe(subscription)
