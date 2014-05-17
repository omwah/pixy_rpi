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

import time
import logging

PIXY_MAXIMUM_ARRAYSIZE = 130
PIXY_START_WORD        = 0xaa55
PIXY_START_WORDX       = 0x55aa
PIXY_DEFAULT_ADDR      = 0x54  # I2C
BLOCK_LEN              = 5

def print_block(block):
    (signature, x, y, width, height) = block
    print("sig: %d x: %d y: %d width: %d height: %d" % (signature, x, y, width, height))

class Pixy:
    def __init__(self, link, addr=PIXY_DEFAULT_ADDR):
        self.link = link
        self.blocks = []
        self.skipStart = False # boolean
        #self.link.init(addr)

    def getBlocks(self, maxBlocks=1000):
        """ returns uint16_t """
        self.blocks = []

        if not self.skipStart:
            if not self._getStart():
                return 0
        else:
            self.skipStart = False

        while len(self.blocks) < maxBlocks and len(self.blocks) < PIXY_MAXIMUM_ARRAYSIZE:
            checksum = self.link.getWord()
            if checksum == PIXY_START_WORD: # start of next frame
                self.skipStart = True
                return len(self.blocks)
            elif checksum == 0:
                return len(self.blocks)

            block = []
            for ii in range(BLOCK_LEN):
                block.append(self.link.getWord())

            trialsum = sum(block)

            if (checksum == trialsum):
                self.blocks.append(block)
            else:
                logging.debug("cs error")

            w = self.link.getWord()

            if w != PIXY_START_WORD:
                return len(self.blocks)

    def _getStart(self):
        lastw = 0xffff
        while (True):
            w = self.link.getWord()
            if w == 0 and lastw == 0:
                self._delay_microsec(10)
                return False
            elif w == PIXY_START_WORD and lastw == PIXY_START_WORD:
                return True
            elif w == PIXY_START_WORDX:
                logging.debug("reorder")
                self.link.getByte() # resync

            lastw = w

    def _delay_microsec(self, durationMs):
        time.sleep(durationMs / 1000000.0)
