#
# begin license header
#
# This file is part of Pixy CMUcam5 or "Pixy" for short
#
# All Pixy source code is provided under the terms of the
# GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
# Those wishing to use Pixy source code, software and/or
# technologies under different licensing terms should contact us at
# cmucam@cs.cmu.edu. Such licensing terms are available for
# all portions of the Pixy codebase presented here.
#
# end license header
#

#
#  Pixy.h - Library for interfacing with Pixy.
#  Created by Scott Robinson, October 22, 2013.
#  Released into the public domain.
#

import wiringpi2
import os
import struct
import numpy

SPI_CHANNEL          = 0
SPI_SPEED            = 250000

PIXY_SYNC_BYTE       = 0x5a
PIXY_SYNC_BYTE_DATA  = 0x5b
PIXY_OUTBUF_SIZE     = 6

class LinkSPI:
    def __init__(self):
        self.outBuf = []
        self.fd = wiringpi2.wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED)

    def getWord(self):
        """ returns uint16_t """
        # ordering is different because Pixy is sending 16 bits through SPI
        # instead of 2 bytes in a 16-bit word as with I2C
        out = 0

        if len(self.outBuf) > 0:
            w = numpy.uint16(self.getByte(PIXY_SYNC_BYTE_DATA))
            out = self.outBuf.pop(0)
        else:
            w = numpy.uint16(self.getByte(PIXY_SYNC_BYTE))

        w = w << 8
        c = numpy.uint8(self.getByte(out))
        w = w | c

        return w

    def getByte(self, out=0x00):
        """ return uint8_t """
        # Using file handles doesn't work too well
        #os.write(self.fd, struct.pack('B', out))
        #c = os.read(self.fd, 1)
        # Requires a fixed version of wiringpi2 SPI function
        _, c = wiringpi2.wiringPiSPIDataRW(0, struct.pack('B', out))
        ret = numpy.uint8(struct.unpack('B', c)[0])
        return ret

    def send(self, data):
        """ 
        data array of bytes
        return int8_t 
        """
        if len(data) > PIXY_OUTBUF_SIZE or len(self.outBuf) != 0:
            return -1

        self.outBuf = data
        return len(self.outBuf)
