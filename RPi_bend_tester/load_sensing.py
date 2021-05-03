from time import sleep, time
import sys

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from hk711 import HK711

from graphs import formal_plot

REFERENCE_UNIT = 1
RUN_MINUTES = 5

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(REFERENCE_UNIT)
hx.reset()
sleep(1)
tare_value, tare_pause_values, tare_values = hx.tare()

print("Tare done! Add weight now...")

input('Press enter to continue once calibration weight added')

try:
    cal_value, cal_pause_values, cal_values = hx.read_pulse_average(times=15,
                                                                    duration=120,
                                                                    spacing=5,
                                                                    pause=60
                                                                    )
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()


formal_plot(tuple(range(len(tare_pause_values))),
            tare_pause_values,
            )

plt.plot((len(tare_pause_values)-0.,)*2,
         (0, max(tare_pause_values)),
         'r-'
)

(gradient, intercept), r_squared = formal_plot(tuple(range(len(tare_values))),
                                               tare_values,
                                               )

print('Gradient = ', gradient)
print('Intercept =', intercept)
print('r squared =', r_squared)
