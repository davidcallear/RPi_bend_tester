from time import sleep, time

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
hx.tare()

print("Tare done! Add weight now...")

values = []
start_time = time()

while time() - start_time < 60 * RUN_MINUTES:
    try:
        val = hx.get_weight(5)
        values.append(val)
        print(val)

        hx.power_down()
        hx.power_up()
        sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

start_index = len(values) * 3 // RUN_MINUTES
stable_values = values[start_index:]

formal_plot(tuple(range(len(stable_values))),
            stable_values,
            title='Runtime (/ ~0.1s) against Load cell reading'
            )
