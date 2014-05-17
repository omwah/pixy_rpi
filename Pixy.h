//
// begin license header
//
// This file is part of Pixy CMUcam5 or "Pixy" for short
//
// All Pixy source code is provided under the terms of the
// GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
// Those wishing to use Pixy source code, software and/or
// technologies under different licensing terms should contact us at
// cmucam@cs.cmu.edu. Such licensing terms are available for
// all portions of the Pixy codebase presented here.
//
// end license header
//

/*
  Pixy.h - Library for interfacing with Pixy.
  Cobbled together by Omwah and Jasco May 2014
  Based on code originally created by Scott Robinson, October 22, 2013.
  Released into the public domain.
*/

#ifndef PIXY_H
#define PIXY_H

#include "TPixy.h"
#include <wiringPiSPI.h>

#define SPI_CHANNEL         0
#define SPI_SPEED           250000 // Arduino: SPI_CLOCK_DIV16

#define PIXY_SYNC_BYTE              0x5a
#define PIXY_SYNC_BYTE_DATA         0x5b
#define PIXY_OUTBUF_SIZE            6

class LinkSPI {
public:
    void init(uint8_t addr) {
        outLen = 0;
        wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) ;
    }

    uint16_t getWord() {
        // ordering is different because Pixy is sending 16 bits through SPI
        // instead of 2 bytes in a 16-bit word as with I2C
        uint16_t w;
        uint8_t c, out = 0;

        if (outLen) {
            w = getByte(PIXY_SYNC_BYTE_DATA);
            out = outBuf[outIndex++];

            if (outIndex == outLen) {
                outLen = 0;
            }
        } else {
            w = getByte(PIXY_SYNC_BYTE);
        }

        w <<= 8;
        c = getByte(out);
        w |= c;

        return w;
    }

    uint8_t getByte(uint8_t out=0x00) {
        uint8_t c = out;
        wiringPiSPIDataRW(SPI_CHANNEL, &c, 1);
        return c;
    }

    int8_t send(uint8_t *data, uint8_t len) {
        if (len > PIXY_OUTBUF_SIZE || outLen != 0) {
            return -1;
        }

        memcpy(outBuf, data, len);
        outLen = len;
        outIndex = 0;
        return len;
    }

private:
    uint8_t outBuf[PIXY_OUTBUF_SIZE];
    uint8_t outLen;
    uint8_t outIndex;
};


typedef TPixy<LinkSPI> Pixy;

#endif
