"""
Ambient light level readout using the I2CDriver Mini (https://i2cdriver.com/mini.html)
and a TSL2561 digital temperature sensor
"""

import time
import i2cdriver


class TSL2561:
    """
    Simple support for the TSL2561 sensor
    """

    TSL_CMD_FLAG = 0x80
    TSL_CTRL_REG = 0x00
    TSL_TIMING_REG = 0x01
    TSL_ID_REG = 0x0A
    TSL_ADC_0 = 0x0C
    TSL_ADC_1 = 0x0E

    def __init__(self, i2c, address=0x39):
        """
        Instantiate the TSL2561 class
        Takes an I2CDriver instance and an (optional) I2C address
        (as the address can be manually adjusted on the TSL2561)
        """
        self.i2c = i2c
        self.addr = address
        self.alert = False

        # Power up device
        cmd = self.make_command(self.TSL_CTRL_REG)
        self.i2c.regwr(self.addr, self.TSL_CTRL_REG, [0x03])

        # Set timing
        cmd = self.make_command(self.TSL_TIMING_REG)
        self.i2c.regwr(self.addr, cmd, [0x11])

    def get_light_level(self):
        """
        Read and return the ambient temperature
        """
        cmd = self.make_command(self.TSL_ADC_0)
        adc_0 = self.i2c.regrd(self.addr, cmd, ">H")
        adc_0_msb =  (adc_0 & 0xFF00) >> 8
        adc_0_lsb = adc_0 & 0xFF

        cmd = self.make_command(self.TSL_ADC_1)
        adc_1 = self.i2c.regrd(self.addr, cmd, ">H")
        adc_1_msb =  (adc_1 & 0xFF00) >> 8
        adc_1_lsb = adc_1 & 0xFF

        return (adc_0, adc_1)

    def get_id(self):
        """
        Read and return the manufacturer and device IDs as a tuple
        """
        cmd = self.make_command(self.TSL_CTRL_REG)
        print(cmd)
        pwr_val = self.i2c.regrd(self.addr, cmd, ">B")
        print(pwr_val)

        cmd = self.make_command(self.TSL_ID_REG)
        print(cmd)
        dev_id = self.i2c.regrd(self.addr, cmd, ">B")
        print(dev_id)
        return (dev_id, pwr_val)

    def make_command(self, register):
        return self.TSL_CMD_FLAG | 0x20 | register


if __name__ == '__main__':
    i2c_bus = i2cdriver.I2CDriver("/dev/cu.usbserial-DO029IEZ")
    sensor = TSL2561(i2c_bus)
    i2c_bus.scan()

    # Check that we can read the manufacturer ID
    part_num, power_val = sensor.get_id()
    part_num = (part_num & 0xF0) >> 4
    #assert part_num == 0x00

    # Loop and display temperature every 5 seconds
    while True:
        reading = sensor.get_light_level()
        print(f"Lux: {reading[0]:.4f}")
        time.sleep(5.0)
