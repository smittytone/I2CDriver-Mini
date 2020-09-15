"""
Countup and countdown readout using the I2CDriver Mini (https://i2cdriver.com/mini.html)
and an HT16K33-based 4-digit, 7-segment LED
(https://learn.adafruit.com/adafruit-7-segment-led-featherwings/overview)
"""

import time
import i2cdriver


class HT16K33:
    """
    A simple driver for the I2C-connected Holtek HT16K33 controller chip and a four-digit,
    seven-segment LED connected to it.
    For example: https://learn.adafruit.com/adafruit-7-segment-led-featherwings/overview
    Version:   2.0.0
    Author:    smittytone
    Copyright: 2020, Tony Smith
    Licence:   MIT
    """

    HT16K33_SEGMENT_SYSTEM_ON = 0x21
    HT16K33_SEGMENT_DISPLAY_ON = 0x81
    HT16K33_SEGMENT_CMD_BRIGHTNESS = 0xE0
    HT16K33_SEGMENT_MINUS_CHAR = 0x10
    HT16K33_SEGMENT_COLON_ROW = 0x04

    # The positions of the segments within the buffer
    pos = [0, 2, 6, 8]

    # Bytearray of the key alphanumeric characters we can show:
    # 0-9, A-F, minus, degree
    chars = b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x5F\x7C\x58\x5E\x7B\x71\x40\x63'

    def __init__(self, i2c, address=0x70):
        """
        Instantiate the LED object and power it up
        """
        self.i2c = i2c
        self.addr = address
        self.buffer = bytearray(16)

        # Initialize display: clock on, display on
        self.send_command(self.HT16K33_SEGMENT_SYSTEM_ON)
        self.send_command(self.HT16K33_SEGMENT_DISPLAY_ON)
        self.set_brightness(10)
        self.update()

    def set_brightness(self, brightness=15):
        """
        Set the LED's brightness (1-15)
        """
        if brightness < 1 or brightness > 15: brightness = 15
        brightness &= 0x0F
        self.send_command(self.HT16K33_SEGMENT_CMD_BRIGHTNESS | brightness)

    def set_flash(self, rate=0):
        rates = [0, 2, 1, 0.5]
        if rate not in rates: rate = 0
        value = rates.index(rate)
        self.send_command(0x81 | value)

    def set_colon(self, is_set=True):
        """
        Set or unset the display's central colon symbol.
        """
        self.buffer[self.HT16K33_SEGMENT_COLON_ROW] = 0x02 if is_set is True else 0x00

    def set_number(self, number, digit=0, has_dot=False):
        """
        Draw a number (0-9) on the LED at the specified digit: 0-4 (L-R)
        If 'has_dot' is true, the adjacent decimal point will be lit
        """
        self.set_char(str(number), digit, has_dot)

    def set_char(self, char, digit=0, has_dot=False):
        """
        Draw a character (0-0, A-F) on the LED at the specified digit: 0-4 (L-R)
        If 'has_dot' is true, the adjacent decimal point will be lit
        """
        if not 0 <= digit <= 3: return
        char = char.lower()
        if char in 'abcdef':
            char_val = ord(char) - 87
        elif char == '-':
            char_val = self.HT16K33_SEGMENT_MINUS_CHAR
        elif char in '0123456789':
            char_val = ord(char) - 48
        elif char == ' ':
            char_val = 0x00
        else:
            return

        self.buffer[self.pos[digit]] = self.chars[char_val]
        if has_dot is True: self.buffer[self.pos[digit]] |= 0b10000000

    def send_command(self, byte):
        """
        Send a command byte to the LED
        """
        self.i2c.start(self.addr, 0)
        self.i2c.write([byte])
        self.i2c.stop()

    def update(self):
        """
        Write the buffer to the LED
        """
        bfr = [0x00]
        for i in range(0, len(self.buffer)):
            bfr.append(self.buffer[i])
        self.i2c.start(self.addr, 0)
        self.i2c.write(bfr)
        self.i2c.stop()


if __name__ == '__main__':
    i2c_bus = i2cdriver.I2CDriver("/dev/cu.usbserial-DO029IEZ")
    led = HT16K33(i2c_bus)
    count = 0

    # Loop and count upwards
    while count < 10000:
        count_bcd = int(str(count), 16)
        led.set_number((count_bcd & 0xF000) >> 12, 0)
        led.set_number((count_bcd & 0x0F00) >> 8, 1)
        led.set_number((count_bcd & 0xF0) >> 4, 2)
        led.set_number((count_bcd & 0x0F), 3)
        led.update()
        count += 1
        time.sleep(0.01)

    led.set_colon()

    # Loop and count upwards
    while count > -1:
        count_bcd = int(str(count), 16)
        led.set_number((count_bcd & 0xF000) >> 12, 0)
        led.set_number((count_bcd & 0x0F00) >> 8, 1)
        led.set_number((count_bcd & 0xF0) >> 4, 2)
        led.set_number((count_bcd & 0x0F), 3)
        led.update()
        count -= 1
        time.sleep(0.01)
