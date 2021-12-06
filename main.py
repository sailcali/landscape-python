#!/usr/bin/env python3

import gpiozero
import time
 
relay = gpiozero.OutputDevice(17, active_high=True, initial_value=False)

relay.off()
time.sleep(15)
