Pixy for Raspberry Pi
=====================

Included here are some C++ and Python code that can be used to read data from the `Pixy <http://www.cmucam.org/projects/cmucam5>`_ camera over SPI.

The C++ code requires `Wiring Pi <http://wiringpi.com/>`_. Compile it using the Makefile after installing Wiring Pi. Test using the `echo` program.

The Python code requires a modified version of the Python wrappers to Wiring Pi known as `WiringPi2-Python <https://github.com/WiringPi/WiringPi2-Python>`_. I had to fix the SPI read/write function in it so I could get data from the bus. After installing the Python wrappers you should be able to run `echo.py` to read what the Pixy is sending.

You can use the Arduino cable included with your Pixy and some jumpers to connect to the Raspberry Pi. Connect MISO, MOSI, SCK and Ground. The table below is what I used.

==== ===== ============
Name Cable Raspberry Pi
==== ===== ============
MISO  1     21
SCK   3     23
MOSI  4     19
Gnd   6     Various
==== ===== ============

For more information check the `eLinux.org GPIO page <http://elinux.org/RPi_Low-level_peripherals#General_Purpose_Input.2FOutput_.28GPIO.29>`_ and the `Arduino SPI page <http://arduino.cc/en/Reference/SPI>`_. The Arduino SPI page will help you figure out what the pins are on the Pixy included Arduino cable.

You can also get the `PixyMon <https://github.com/charmedlabs/pixy>`_ software compiled on the Raspberry Pi by following the instructions in the `host/linux/README.linux` file. You may need to remove `-mno-ms-bitfields` from the flags in the Makefile that is generated before succesfully compiling.
