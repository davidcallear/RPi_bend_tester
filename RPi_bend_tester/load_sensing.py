from time import sleep, time
import sys

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from hk711 import HK711

from graphs import formal_plot

REFERENCE_UNIT = 1
SPACING = 5

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
try:
    tare_value, tare_pause_values, tare_values = hx.tare()
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()

print("Tare done! Add weight now...")

input('Press enter once weight added')

try:
    cal_value, cal_pause_values, cal_values = hx.read_pulse_average(times=15,
                                                                    duration=120,
                                                                    spacing=SPACING,
                                                                    pause=60
                                                                    )
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()

# plot results for tare

formal_plot(tuple(range(0, len(tare_pause_values), SPACING)),
            tare_pause_values,
            )

plt.plot((len(tare_pause_values)-0.5,)*2,
         (0, max(tare_pause_values)),
         'r-'
)

(gradient, intercept), r_squared = formal_plot(tuple(range(0, len(tare_values), SPACING)),
                                               tare_values,
                                               title='',
                                               )

# Hopefully values are somewhat random, so r squared is close to zero
print('Gradient = ', gradient)
print('Intercept =', intercept)
print('r squared =', r_squared)

plt.show()

# plot results for measurement

formal_plot(tuple(range(0, len(cal_pause_values), SPACING)),
            cal_pause_values,
            )

plt.plot((len(cal_pause_values)-0.5,)*2,
         (0, max(cal_pause_values)),
         'r-'
)

(gradient, intercept), r_squared = formal_plot(tuple(range(0, len(cal_values), SPACING)),
                                               cal_values,
                                               )

# Hopefully values are somewhat random, so r squared is close to zero
print('Gradient = ', gradient)
print('Intercept =', intercept)
print('r squared =', r_squared)