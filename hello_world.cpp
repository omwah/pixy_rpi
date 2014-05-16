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

#include <Pixy.h>

Pixy pixy;

int main()
{ 
  int j;
  uint16_t blocks;
 
  while (1) { 
    blocks = pixy.getBlocks();
    
    if (blocks) {
      std::cout << "Detected " << blocks << std::endl; 
      for (j=0; j<blocks; j++) {
        std::cout << "  block " << j << " ";
        pixy.blocks[j].print();
      }
    }
  }

  return 0;
}

