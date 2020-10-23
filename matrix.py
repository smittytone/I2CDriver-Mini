"""
Demo for the I2CDriver Mini (https:#i2cdriver.com/mini.html)
"""

import time
import random
import i2cdriver


class HT16K33:
    """
    A simple driver for the I2C-connected Holtek HT16K33 controller chip and Adafruit's
    0.8-inch 8 x 16 LED Matrix FeatherWing (https://www.adafruit.com/product/3149)
    Version:   1.0.0
    Author:    smittytone
    Copyright: 2020, Tony Smith
    Licence:   MIT
    """

    HT16K33_MATRIX_SYSTEM_ON = 0x21
    HT16K33_MATRIX_DISPLAY_ON = 0x81
    HT16K33_MATRIX_CMD_BRIGHTNESS = 0xE0
    HT16K33_MATRIX_MINUS_CHAR = 0x10
    HT16K33_MATRIX_COLON_ROW = 0x04

    DISPLAY_WIDTH = 16
    DISPLAY_HEIGHT = 8

    CHARSET = [
        b"\x00\x00",              # space - Ascii 32
        b"\xfa",                  # !
        b"\xc0\x00\xc0",          # "
        b"\x24\x7e\x24\x7e\x24",  # #
        b"\x24\xd4\x56\x48",      # $
        b"\xc6\xc8\x10\x26\xc6",  # %
        b"\x6c\x92\x6a\x04\x0a",  # &
        b"\xc0",                  # '
        b"\x7c\x82",              # (
        b"\x82\x7c",              # )
        b"\x10\x7c\x38\x7c\x10",  # *
        b"\x10\x10\x7c\x10\x10",  # +
        b"\x06\x07",              # ,
        b"\x10\x10\x10\x10",  	 # -
        b"\x06\x06",              # .
        b"\x04\x08\x10\x20\x40",  # /
        b"\x7c\x8a\x92\xa2\x7c",  # 0 - Ascii 48
        b"\x42\xfe\x02",          # 1
        b"\x46\x8a\x92\x92\x62",  # 2
        b"\x44\x92\x92\x92\x6c",  # 3
        b"\x18\x28\x48\xfe\x08",  # 4
        b"\xf4\x92\x92\x92\x8c",  # 5
        b"\x3c\x52\x92\x92\x8c",  # 6
        b"\x80\x8e\x90\xa0\xc0",  # 7
        b"\x6c\x92\x92\x92\x6c",  # 8
        b"\x60\x92\x92\x94\x78",  # 9
        b"\x36\x36",              # : - Ascii 58
        b"\x36\x37",              # ;
        b"\x10\x28\x44\x82",      # <
        b"\x24\x24\x24\x24\x24",  # =
        b"\x82\x44\x28\x10",      # >
        b"\x60\x80\x9a\x90\x60",  # ?
        b"\x7c\x82\xba\xaa\x78",  # @
        b"\x7e\x90\x90\x90\x7e",  # A - Ascii 65
        b"\xfe\x92\x92\x92\x6c",  # B
        b"\x7c\x82\x82\x82\x44",  # C
        b"\xfe\x82\x82\x82\x7c",  # D
        b"\xfe\x92\x92\x92\x82",  # E
        b"\xfe\x90\x90\x90\x80",  # F
        b"\x7c\x82\x92\x92\x5c",  # G
        b"\xfe\x10\x10\x10\xfe",  # H
        b"\x82\xfe\x82",          # I
        b"\x0c\x02\x02\x02\xfc",  # J
        b"\xfe\x10\x28\x44\x82",  # K
        b"\xfe\x02\x02\x02\x02",  # L
        b"\xfe\x40\x20\x40\xfe",  # M
        b"\xfe\x40\x20\x10\xfe",  # N
        b"\x7c\x82\x82\x82\x7c",  # O
        b"\xfe\x90\x90\x90\x60",  # P
        b"\x7c\x82\x92\x8c\x7a",  # Q
        b"\xfe\x90\x90\x98\x66",  # R
        b"\x64\x92\x92\x92\x4c",  # S
        b"\x80\x80\xfe\x80\x80",  # T
        b"\xfc\x02\x02\x02\xfc",  # U
        b"\xf8\x04\x02\x04\xf8",  # V
        b"\xfc\x02\x3c\x02\xfc",  # W
        b"\xc6\x28\x10\x28\xc6",  # X
        b"\xe0\x10\x0e\x10\xe0",  # Y
        b"\x86\x8a\x92\xa2\xc2",  # Z - Ascii 90
        b"\xfe\x82\x82",          # [
        b"\x40\x20\x10\x08\x04",  # \
        b"\x82\x82\xfe",          # ]
        b"\x20\x40\x80\x40\x20",  # ^
        b"\x02\x02\x02\x02\x02",  # _
        b"\xc0\xe0",              # '
        b"\x04\x2a\x2a\x1e",      # a - Ascii 97
        b"\xfe\x22\x22\x1c",      # b
        b"\x1c\x22\x22\x22",      # c
        b"\x1c\x22\x22\xfc",      # d
        b"\x1c\x2a\x2a\x10",      # e
        b"\x10\x7e\x90\x80",      # f
        b"\x18\x25\x25\x3e",      # g
        b"\xfe\x20\x20\x1e",      # h
        b"\xbc\x02",              # i
        b"\x02\x01\x21\xbe",      # j
        b"\xfe\x08\x14\x22",      # k
        b"\xfc\x02",              # l
        b"\x3e\x20\x18\x20\x1e",  # m
        b"\x3e\x20\x20 \x1e",     # n
        b"\x1c\x22\x22\x1c",      # o
        b"\x3f\x22\x22\x1c",      # p
        b"\x1c\x22\x22\x3f",      # q
        b"\x22\x1e\x20\x10",      # r
        b"\x12\x2a\x2a\x04",      # s
        b"\x20\x7c\x22\x04",      # t
        b"\x3c\x02\x02\x3e",      # u
        b"\x38\x04\x02\x04\x38",  # v
        b"\x3c\x06\x0c\x06\x3c",  # w
        b"\x22\x14\x08\x14\x22",  # x
        b"\x39\x05\x06\x3c",      # y
        b"\x26\x2a\x2a\x32",      # z - Ascii 122
        b"\x10\x7c\x82\x82",      # {
        b"\xee",                  # |
        b"\x82\x82\x7c\x10",      # }
        b"\x40\x80\x40\x80",      # ~
        b"\x60\x90\x90\x60",      # Degrees sign - Ascii 127
    ]

    def __init__(self, i2c, address=0x70):
        """
        Instantiate the LED object and power it up
        """
        import time

        self.i2c = i2c
        self.addr = address
        self.buffer = bytearray(32)

        # Initialize display: clock on, display on
        self.send_command(self.HT16K33_MATRIX_SYSTEM_ON)
        self.send_command(self.HT16K33_MATRIX_DISPLAY_ON)
        self.set_brightness(10)
        self.update()

    def set_brightness(self, brightness=15):
        """
        Set the LED's brightness (1-15)
        """
        if brightness < 1 or brightness > 15: brightness = 15
        brightness &= 0x0F
        self.send_command(self.HT16K33_MATRIX_CMD_BRIGHTNESS | brightness)

    def set_flash(self, rate=0):
        rates = [0, 2, 1, 0.5]
        if rate not in rates: rate = 0
        value = rates.index(rate)
        self.send_command(0x81 | value)

    def clear(self):
        for i in range(0, 32):
            self.buffer[i] = 0x00
        return self

    def plot(self, x, y, colour=1):
        if (0 <= x < self.DISPLAY_WIDTH) and (0 <= y < self.DISPLAY_HEIGHT):
            x = self._get_row(x)
            v = self.buffer[x]
            if colour == 1:
                if v & (1 << y) == 0: v = v | (1 << y)
            else:
                if v & (1 << y) != 0: v = v & ~(1 << y)
            self.buffer[x] = v
            return self
        return None

    def set_char(self, the_char, row):
        if the_char is None or len(the_char) != 1: return None
        if 0 <= row < self.DISPLAY_WIDTH:
            glyph = self.CHARSET[ord(the_char[0]) - 32]
            for j in range(0, len(glyph)):
                col = glyph[j]
                for k in range(0, 8):
                    if row < self.DISPLAY_WIDTH:
                        r = self._get_row(row)
                        v = self.buffer[r]
                        if col & (1 << k) != 0: v = v | (1 << k)
                        self.buffer[r] = v
                row += 1
            return self
        return None

    def scroll_text(self, the_line, speed=0.1):
        if the_line is None or len(the_line) == 0: return None
        the_line += "        "
        length = 0
        for i in range(0, len(the_line)):
            glyph = self.CHARSET[ord(the_line[i]) - 32]
            length += len(glyph) + 1
        buf = bytearray(length * 8)

        row = 0
        for i in range(0, len(the_line)):
            glyph = self.CHARSET[ord(the_line[i]) - 32]
            for j in range(0, len(glyph)):
                buf[row] = glyph[j]
                row += 1
            row += 1

        row = 0
        cur = 0
        while row < length:
            for i in range(0, 16):
                self.buffer[self._get_row(i)] = buf[cur];
                cur += 1
            self.update()
            time.sleep(speed)
            row += 1
            cur -= 15

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

    def _get_row(self, x):
        if x < 8:
            x = 16 + (x << 1)
        else:
            x = 1 + (x << 1)
        return x



if __name__ == '__main__':
    i2c_bus = i2cdriver.I2CDriver("/dev/cu.usbserial-DO029IEZ")
    led = HT16K33(i2c_bus)
    led.update()

    led.set_char("*", 5).update()
    time.sleep(2)
    led.clear().update()

    x = 0
    y = 0
    dx = 1
    dy = 1

    led.scroll_text("This is a test of scrolling...")

    count = 0
    while True:
        # Get the CPU utilization and calculate
        # the Binary-Coded Decimal (BCD) form
        led.clear().plot(x, y).update()

        x += dx

        if x < 0:
            x = 0
            dx = 1
            y += dy
        if x == led.DISPLAY_WIDTH:
            x = led.DISPLAY_WIDTH - 1
            dx = -1
            y += dy

        if y >= led.DISPLAY_HEIGHT:
            y -= 1
            dy = -1
        if y < 0:
            y = 0
            dy = 1
            count += 1
            if count > 4: break

        # Pause for breath
        time.sleep(0.01)

    time.sleep(0.01)
    led.clear().update()
