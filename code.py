import board
import busio
import adafruit_framebuf

# uncomment next line if you are using Feather CharlieWing LED 15 x 7
# from adafruit_is31fl3731.charlie_wing import CharlieWing as Display
# uncomment next line if you are using Adafruit 16x9 Charlieplexed PWM LED Matrix
from adafruit_is31fl3731.matrix import Matrix as Display
# uncomment next line if you are using Adafruit 16x8 Charlieplexed Bonnet
#from adafruit_is31fl3731.charlie_bonnet import CharlieBonnet as Display

# uncomment next line if you are using Pimoroni Scroll Phat HD LED 17 x 7
# from adafruit_is31fl3731.scroll_phat_hd import ScrollPhatHD as Display
# uncomment next line if you are using Pimoroni 11x7 LED Matrix Breakout
# from adafruit_is31fl3731.matrix_11x7 import Matrix11x7 as Display

# uncomment this line if you use a Pico, here with SCL=GP21 and SDA=GP20.
I2C1 = busio.I2C(board.GP19, board.GP18)

#i2c = busio.I2C(board.GP19, board.GP18)

# Four matrices on each bus, for a total of eight...
DISPLAY = [
    Display(I2C1, address=0x74, frames=(0, 1)),  # Upper row
    Display(I2C1, address=0x75, frames=(0, 1)),
    Display(I2C1, address=0x76, frames=(0, 1)),
    Display(I2C1, address=0x77, frames=(0, 1)),
    #Display(I2C[1], address=0x74, frames=(0, 1)),  # Lower row
    #Display(I2C[1], address=0x75, frames=(0, 1)),
    #Display(I2C[1], address=0x76, frames=(0, 1)),
    #Display(I2C[1], address=0x77, frames=(0, 1)),
]

text = ["4", "2", "3", "4"]

# Create a framebuffer for our display
buf = bytearray(32)  # 2 bytes tall x 16 wide = 32 bytes (9 bits is 2 bytes)
fb = adafruit_framebuf.FrameBuffer(
    buf, DISPLAY[1].width, DISPLAY[1].height, adafruit_framebuf.MVLSB
)


frame = 0  # start with frame 0
while True:
    for disp in DISPLAY:
        fb.fill(0)
        if(disp == DISPLAY[0]):
            text_to_show = text[0]
        elif(disp == DISPLAY[1]):
            text_to_show = text[1]
        elif(disp == DISPLAY[2]):
            text_to_show = text[2]
        elif(disp == DISPLAY[3]):
            text_to_show = text[3]
        fb.text(text_to_show, 5, 0, color=1)

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
