'''Handle a GRBL controller on a Raspberry Pi.
'''
from decimal import Decimal
from glob import glob
from time import sleep

from serial import Serial


class GrblSerial(Serial):
    '''Control a GRBL with G-code on a Raspberry Pi.
    '''
    def __init__(self, serial_port_glob='/dev/ttyUSB*', baud=115200, 
                 min_z=-20, max_z=0, feed_rate=10):
        def is_number(var, var_name):
            '''Raise an error if `var` if not an int/float/Decimal
            '''
            if not isinstance(var, (int, float, Decimal)):
                raise TypeError(f'{var_name} must be an int/float/Decimal, not {type(var)}')
        
        # check inputs
        is_number(min_z, 'min_z')
        is_number(max_z, 'max_z')
        if max_z <= min_z:
            raise ValueError('min_z must be less than max_z')
        is_number(feed_rate, 'feed_rate')
        if not 0 < feed_rate <= 100:
            raise ValueError(f'feed_rate must be between 0 and 100, not {feed_rate}')
        if not isinstance(baud, int):
            raise TypeError(f'baud must be an int (eg. 115200), not {type(baud)}')
        
        self.min_z = min_z
        self.max_z = max_z
        self.feed_rate = feed_rate
        self.current_z = 0
        self.busy = False
        
        # find serial port (first matching `serial_port_glob`)
        serial_ports = glob(serial_port_glob)
        serial_port = serial_ports[0]
        
        # run __init__ of Serial class
        print('Opening serial port...')
        super().__init__(serial_port, baud)
        
        self.wake_grbl()
        self.initialize()

    def wake_grbl(self):
        '''Open serial port for GRBL controller.
        '''
        # Wake up grbl
        self.write(b'\r\n\r\n')
        sleep(2)   # Wait for grbl to initialize
        self.reset_input_buffer()  # Flush startup text in serial input
    
    def initialize(self):
        '''Send G-codes to initialize GRBL controller.
        '''
        # set absolute coordinates
        self.write_gcode('G90')
        # set unit to mm
        self.write_gcode('G21')
        # set feed rate mm/min
        self.write_gcode(f'F{self.feed_rate}')
        # set current position to Z0
        self.write_gcode('G10 L2 P1 Z0')
        self.write_gcode('G54')
    
    def write_gcode(self, gcode):
        r'''Write G-code to GRBL controller
        
        Adds '\n' to end of `gcode` so that G-code is done by GRBL controller.
        
        Args:
            gcode (str): G-code to send
        Returns:
            str: response from GRBL controller
                eg. 'ok\r\n'
        '''
        # don't write G-code if already writing G-code
        if self.busy:
            return 'busy\r\n'
        
        self.busy = True
        print(f'Sending G-code: {gcode}')
        gcode += '\n'
        # convert G-code to bytes
        gcode_bytes = gcode.encode('utf-8')
        # send bytes to GRBL controller
        self.write(gcode_bytes)
        # Wait for grbl response with carriage return
        grbl_out = self.readline()
        # Convert to string
        grbl_out = grbl_out.decode('utf-8')
        print(f'GRBL response: {grbl_out}')
        self.busy = False
        return grbl_out
