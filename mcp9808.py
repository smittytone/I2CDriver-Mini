"""
Temperature readout using the I2CDriver Mini (https://i2cdriver.com/mini.html)
and an MCP9808 digital temperature sensor (https://www.adafruit.com/product/1782)
"""

import time
import i2cdriver


class MCP9808:
    """
    Simple support for the MCP9808 sensor
    """

    MCP_CONFIG_REG = 0x01
    MCP_AMBIENT_TEMP_REG = 0x05
    MCP_MANUF_ID_REG = 0x06
    MCP_DEVICE_ID_REG = 0x07

    def __init__(self, i2c, address=0x18):
        """
        Instantiate the MCP9808 class
        Takes an I2CDriver instance and an (optional) I2C address
        (as the address can be manually adjusted on the MCP9808)
        """
        self.i2c = i2c
        self.addr = address
        self.alert = False

    def get_temperature(self):
        """
        Read and return the ambient temperature
        """
        temp = self.i2c.regrd(self.addr, self.MCP_AMBIENT_TEMP_REG, ">H")
        temp_msb =  (temp & 0xFF00) >> 8
        temp_lsb = temp & 0xFF

        temp_msb = temp_msb & 0x1F
        if temp_msb & 0x10 == 0x10:
            temp_msb = temp_msb & 0x0F
            temp = 256 - (temp_msb * 16 + temp_lsb / 16)
        else:
            temp = temp_msb * 16 + temp_lsb / 16

        return temp

    def get_ids(self):
        """
        Read and return the manufacturer and device IDs as a tuple
        """
        man_id = self.i2c.regrd(self.addr, self.MCP_MANUF_ID_REG, ">H")
        dev_id = self.i2c.regrd(self.addr, self.MCP_DEVICE_ID_REG, ">H")
        return (man_id, dev_id)


if __name__ == '__main__':
    i2c_bus = i2cdriver.I2CDriver("/dev/cu.usbserial-DO029IEZ")
    sensor = MCP9808(i2c_bus)

    # Check that we can read the manufacturer ID
    manufacturer, device = sensor.get_ids()
    assert manufacturer == 0x54

    # Loop and display temperature every 5 seconds
    while True:
        reading = sensor.get_temperature()
        print(f"Temperature: {reading:.2f}ºC")
        time.sleep(5.0)
