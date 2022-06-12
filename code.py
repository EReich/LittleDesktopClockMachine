import board
import busio
import adafruit_framebuf
import pyRTOS
import rtc


# User defined message types start at 128
REQUEST_DATA = 128
SENT_DATA = 129

#init stuff for the displays
from adafruit_is31fl3731.matrix import Matrix as Display
#define the I2C buses
I2C1 = busio.I2C(board.GP19, board.GP18)
I2C2 = busio.I2C(board.GP17, board.GP16)

def DisplayTask(self):
    # Four matrices on each bus, for a total of eight...
    DISPLAY = [
        Display(I2C1, address=0x74, frames=(0, 1)),  # Upper row
        Display(I2C1, address=0x75, frames=(0, 1)),
        Display(I2C1, address=0x76, frames=(0, 1)),
        Display(I2C1, address=0x77, frames=(0, 1)),
        Display(I2C2, address=0x74, frames=(0, 1)),  # Lower row
        Display(I2C2, address=0x75, frames=(0, 1)),
        Display(I2C2, address=0x76, frames=(0, 1)),
        Display(I2C2, address=0x77, frames=(0, 1)),
    ]

    text = ["1", "2", "2","5","J","N", "1", "2"]

    # Create a framebuffer for our display
    buf = bytearray(32)  # 2 bytes tall x 16 wide = 32 bytes (9 bits is 2 bytes)
    fb = adafruit_framebuf.FrameBuffer(
        buf, DISPLAY[1].width, DISPLAY[1].height, adafruit_framebuf.MVLSB
    )

    fb.rotation = 3

    frame = 0  # start with frame 0
    
    yield  #initial yield
    
    while True:
        # Check messages
        msgs = self.recv()
        for msg in msgs:

            ### Handle messages by adding elifs to this
            if msg.type == pyRTOS.QUIT:  # This allows you to
                                         # terminate a thread.
                                         # This condition may be removed if
                                         # the thread should never terminate.

                ### Tear down code here
                print("Terminating task:", self.name)
                print("Terminated by:", msg.source)

                ### End of Tear down code
                return
            elif msg.type == REQUEST_DATA: # Example message, using user
                                           # message types
                self.send(pyRTOS.Message(SENT_DATA,
                                         self,
                                         msg.source,
                                         "This is data"))
        ### End Message Handler
        
        
        for disp in DISPLAY:
            fb.fill(0)
            if(disp == DISPLAY[0]):
                text_to_show = text[0]
                xpos = 2
            elif(disp == DISPLAY[1]):
                text_to_show = text[1]
                xpos = 2
            elif(disp == DISPLAY[2]):
                text_to_show = text[2]
                xpos = 2
            elif(disp == DISPLAY[3]):
                text_to_show = text[3]
                xpos = 2
            elif(disp == DISPLAY[4]):
                text_to_show = text[4]
                xpos = 2
            elif(disp == DISPLAY[5]):
                text_to_show = text[5]
                xpos = 2
            elif(disp == DISPLAY[6]):
                text_to_show = text[6]
                xpos = 2
            elif(disp == DISPLAY[7]):
                text_to_show = text[7]
                xpos = 2
            fb.text(text_to_show, xpos, 4, color=1)

            # to improve the display flicker we can use two frame
            # fill the next frame with scrolling text, then
            # show it.
            disp.frame(frame, show=False)
            # turn all LEDs off
            disp.fill(0)
            for x in range(disp.width):
                # using the FrameBuffer text result
                bite = buf[x]
                for y in range(disp.height):
                    bit = 1 << y & bite
                    # if bit > 0 then set the pixel brightness
                    if bit:
                        disp.pixel(x, y, 50)
        
        for disp in DISPLAY:
            # now that the frame is filled, show it.
            disp.frame(frame, show=True)
        frame = 0 if frame else 1
        
        yield [pyRTOS.timeout(0.1)]



pyRTOS.add_task(pyRTOS.Task(DisplayTask, name="display_task", mailbox=True))
#pyRTOS.add_service_routine(lambda: print("Service Routine Executing"))
pyRTOS.start()



