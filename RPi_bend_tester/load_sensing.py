from time import sleep, time
import sys

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from hx711 import HX711

from graphs import formal_plot

REFERENCE_UNIT = 1

# options for measurement timings
TIMES = 15
DURATION = 45
SPACING = 1
PAUSE = 15


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
    tare_value, tare_pause_values, tare_values = hx.tare((times=TIMES,
                                                          duration=DURATION,
                                                          spacing=SPACING,
                                                          pause=PAUSE
                                                          )
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()

print("Tare done! Add weight now...")

print('Value for tare:', tare_value)

# plot results for tare

# plot vertical red line to seperate pause and value reading sections of graph
separation_time = (len(tare_pause_values) - 0.5) * SPACING
plt.plot((separation_time, separation_time),
         (0, max(tare_pause_values)),
         'r-'
)
all_tare_values = tare_pause_values + tare_values
# plot values taken during averaging for given value
(gradient, intercept), r_squared = formal_plot(find_x_values(all_tare_values),
                                               all_tare_values,
                                               title='Values for tare: pause then actual',
                                               x_title='Time since start of tare',
                                               x_units='s',
                                               y_title='Value of reading'
                                               )

# Hopefully values are somewhat random, so r squared is close to zero
print('Gradient = ', gradient)
print('Intercept =', intercept)
# r squared value will be nan if readings were unchanging
# unchanging readings suggests hx711 isn't working/connected
print('r squared =', r_squared)

plt.show()



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

# plot results for measurement
# plot values taken during initial pause (not used for value)
formal_plot(find_x_values(cal_pause_values),
            cal_pause_values,
            show=False
            )
# plot vertical red line to seperate pause and value reading sections of graph
separation_time = (len(cal_pause_values) - 0.5) * SPACING
plt.plot((separation_time, separation_time),
         (0, max(cal_pause_values)),
         'r-'
)
# plot values taken during averaging for given value
(gradient, intercept), r_squared = formal_plot(find_x_values(cal_values),
                                               cal_values,
                                               title='Values for measurement: pause then actual',
                                               x_title='Time since start of measurement',
                                               x_units='s',
                                               y_title='Value of reading'
                                               )

# Hopefully values are somewhat random, so r squared is close to zero
print('Gradient = ', gradient)
print('Intercept =', intercept)
# r squared value will be nan if readings were unchanging
# unchanging readings suggests hx711 isn't working/connected
print('r squared =', r_squared)

print('Value for tare:', tare_value)
print('Value for measurement:', cal_value)
