import time
from zk import *

time.sleep(0)  # sometimes a delay is useful to se
# constant machine port
zk = ZK('192.168.1.201', port=4370)
zk.connect()
n = 5
while n > 0:
    events = zk.read_events()
    for e in events:
        res = '{}"code":[{}"event_type":"{}","door":"{}","card":"{}","pin":"{}","time":"{}","entry_exit":"{}","verify_mode":"{}"{}]{}'.format(
            "{", "{", e.event_type, e.door, e.card, e.pin, "", e.entry_exit, e.verify_mode, "}", "}")

    print('res', res)

    n -= 1
    time.sleep(1)
zk.disconnect()
