from time import sleep, time
import sys

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from hx711 import HX711

from graphs import simple_plot

# adjust this to calibrate weight readings
REFERENCE_UNIT = 1

# options for measurement timings
# number of readings taken on each pulse of readings
TIMES = 15
# time between pulses of readings
SPACING = 5
# time to pause before taking average
PAUSE = 60
# time to take average for
DURATION = 120
# NB: total reading duration will be PAUSE + DURATION for each reading


# allow for clean exit (through keyboard interrupt) from long measurement readings
def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def find_x_values(y_values):
    '''Find x values for graph given y values
    
    Returns a tuple of the same length as `y_values`
        (0, SPACING, SPACING*2, SPACING*3, SPACING*4, SPACING*5, SPACING*6, ...)
    '''
    return tuple(i * SPACING for i in range(0, len(y_values)))

# initialize HK711:
# pin for dout (input pin) -> 5
# pin for pd_sck (output pin) -> 6
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(REFERENCE_UNIT)
hx.reset()
sleep(1)
# tare the balance
print('Now doing tare...')
# find average value, and readings during and after pause
try:
    tare_value, tare_pause_values, tare_values = hx.tare(times=TIMES,
                                                         duration=DURATION,
                                                         spacing=SPACING,
                                                         pause=PAUSE
                                                        )
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()

print("Tare done! Add weight now...")

print('Value for tare:', tare_value)

# plot results for tare
all_tare_values = tare_pause_values + tare_values
# plot values taken during averaging for given value
simple_plot(find_x_values(all_tare_values),
            all_tare_values,
            title='Values for tare: pause then actual',
            x_title=f'Time since start of tare (pause ends at {PAUSE})',
            x_units='s',
            y_title='Value of reading'
            )

plt.show(block=False)
# Hopefully values are somewhat random, so r squared is close to zero



# wait for user to have added weight before proceeding
input('Press enter once weight added')

print('Now taking measurement...')
try:
    # measure weight
    # find average value, and readings during and after pause
    cal_value, cal_pause_values, cal_values = hx.read_pulse_average(times=TIMES,
                                                                    duration=DURATION,
                                                                    spacing=SPACING,
                                                                    pause=PAUSE
                                                                    )
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()

print('Measurement done!')

print('Value for measurement:', cal_value)

print('Close current graph to see next graph')
plt.show()

# plot results for measurement
all_cal_values = cal_pause_values + cal_values
# plot values taken during averaging for given value
simple_plot(find_x_values(all_cal_values),
            all_cal_values,
            title='Values for measurement: pause then actual',
            x_title=f'Time since start of measurement (pause ends at {PAUSE})',
            x_units='s',
            y_title='Value of reading'
            )

plt.show(block=False)

print('Value for tare:', tare_value)
print('Value for measurement:', cal_value)
