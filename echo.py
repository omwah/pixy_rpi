import pixy
import pixy_spi

p = pixy.Pixy(pixy_spi.LinkSPI())
while(True):
    num_blocks = p.getBlocks()
    if num_blocks > 0:
        print "Detected: %d" % num_blocks
        for ii, block in enumerate(p.blocks):
            print "  block %d" % ii,
            pixy.print_block(block)
