# I&sup2;C Driver Mini #

**In Development**

A series of examples demonstrating use of the [I&sup2;C Driver Mini](https://i2cdriver.com/mini.html) USB breakout from Excamera Labs.

This is a tiny, USB-connected board that provides an I&sup2;C controller bus with Python and command line control. The board is controlled over a serial line so it can also be accessed through Swift.

## Examples ##

- [`mcp9808.py`](mcp9808.py)
    — Display the ambient temperature as read by an MCP9808 sensor.
    - Uses the I&sup2;C Driver Mini Python library.
    - Uses the [Adafruit MCP9808 High Accuracy I2C Temperature Sensor Breakout Board](https://www.adafruit.com/product/1782).
- [`mcp9808.swift`](main.swift)
    — Display the ambient temperature as read by an MCP9808 sensor.
    - Uses the I&sup2;C Driver Mini CLI tool call from Swift.
    - Uses the [Adafruit MCP9808 High Accuracy I2C Temperature Sensor Breakout Board](https://www.adafruit.com/product/1782).
- [`counter.py`](counter.py)
    — Display a count up and then count down on an HT16K33-based 7-segment LED display.
    - Uses the I&sup2;C Driver Mini Python library.
    - Uses the [Adafruit 0.56" 4-Digit 7-Segment Display w/I2C Backpack](https://www.adafruit.com/product/879).

## Licence ##

The code in this repo is licensed under the terms of the MIT Licence.<br />
The code in this repo &copy; 2020, Tony Smith.