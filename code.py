import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_framebuf
import pyRTOS
import rtc
import time


c = rtc.RTC()
c.datetime = time.struct_time((2022, 1, 1, 0, 0, 0, 0, -1, -1))

# User defined message types start at 128
SENT_MODE = 128
SENT_TIME = 129
INPUT_HR = 130
INPUT_MIN = 131


#init stuff for the displays
from adafruit_is31fl3731.matrix import Matrix as Display
#define the I2C buses & GPIO pinouts
I2C1 = busio.I2C(board.GP19, board.GP18)
I2C2 = busio.I2C(board.GP17, board.GP16)

mode_button = DigitalInOut(board.GP1)
mode_button.switch_to_input(pull=Pull.DOWN)

hr_button = DigitalInOut(board.GP5)
hr_button.switch_to_input(pull=Pull.DOWN)

min_button = DigitalInOut(board.GP14)
min_button.switch_to_input(pull=Pull.DOWN)

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

    text = ["0", "0", "0","0","N","N", "0", "0"]

    # Create a framebuffer for our display
    buf = bytearray(32)  # 2 bytes tall x 16 wide = 32 bytes (9 bits is 2 bytes)
    fb = adafruit_framebuf.FrameBuffer(
        buf, DISPLAY[1].width, DISPLAY[1].height, adafruit_framebuf.MVLSB
    )

    fb.rotation = 3

    frame = 0  # start with frame 0
    
    yield  #initial yield
    
    if(mode == 2)
        IMAGE = FakePILImage()  # Instantiate fake PIL image object
        FRAME_INDEX = 0  # Double-buffering frame index

        while True:
        # Draw to each display's "back" frame buffer
            for disp in DISPLAY:
                for pixel in range(0, 16 * 9):  # Randomize each pixel
                    IMAGE.pixels[pixel] = BRIGHTNESS if random.randint(1, 100) <= PERCENT else 0
                # Here's the function that we're NOT supposed to call in
                # CircuitPython, but is still present. This writes the pixel
                # data to the display's back buffer. Pass along our "fake" PIL
                # image and it accepts it.
                disp.image(IMAGE, frame=FRAME_INDEX)

            # Then quickly flip all matrix display buffers to FRAME_INDEX
            for disp in DISPLAY:
                disp.frame(FRAME_INDEX, show=True)
            FRAME_INDEX ^= 1  # Swap buffers

    elif(mode == 1)
        while True:
            # Check messages
            msgs = self.recv()
            for msg in msgs:

                ### Handle messages by adding elifs to this
                if msg.type == SENT_TIME:
                    inTime = msg.message

                    text[0] = inTime[0]
                    text[1] = inTime[1]
                    text[2] = inTime[2]
                    text[3] = inTime[3]
                    text[4] = inTime[4]
                    text[5] = inTime[5]
                    text[6] = inTime[6]
                    text[7] = inTime[7]

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

            yield [pyRTOS.timeout(0.01)] #reduce Cycle load by reducing update rate to 30fps

def get_tens(num): #simple function used in the later TimeTask thread to get the 10's place of numbers for output
    pos_nums = []
    while num != 0:
        pos_nums.append(num % 10)
        num = num // 10
    return pos_nums

def TimeTask(self):
    
    
    mode = 0
    
    yield
    
    while True:
        currTime = c.datetime
        msgs = self.recv()
        for msg in msgs:
            if msg.type == SENT_MODE:
                mode = msg.message
                print("new mode accepted:")
                print(mode)
                
            elif (msg.type == INPUT_HR and mode == 0):
                if(c.datetime.tm_hour < 23):
                    newHour = currTime.tm_hour + 1
                    c.datetime = time.struct_time((currTime.tm_year, currTime.tm_mon, currTime.tm_mday, newHour, currTime.tm_min, currTime.tm_sec, 0, -1, -1))
                else:
                    c.datetime = time.struct_time((currTime.tm_year, currTime.tm_mon, currTime.tm_mday, 0, currTime.tm_min, currTime.tm_sec, 0, -1, -1))
                    
            elif (msg.type == INPUT_HR and mode == 1):
                if(c.datetime.tm_hour < 11):
                    newMonth = currTime.tm_mon + 1
                    c.datetime = time.struct_time((currTime.tm_year, newMonth, currTime.tm_mday, currTime.tm_hour, currTime.tm_min, currTime.tm_sec, 0, -1, -1))
                else:
                    c.datetime = time.struct_time((currTime.tm_year, 1, currTime.tm_mday, 0, currTime.tm_min, currTime.tm_sec, 0, -1, -1))
                    
            elif (msg.type == INPUT_MIN and mode == 0):
                if(c.datetime.tm_min < 59):
                    newMin = currTime.tm_min + 1
                    c.datetime = time.struct_time((currTime.tm_year, currTime.tm_mon, currTime.tm_mday, currTime.tm_hour, newMin, currTime.tm_sec, 0, -1, -1))
                else:
                    c.datetime = time.struct_time((currTime.tm_year, currTime.tm_mon, currTime.tm_mday, currTime.tm_hour, 0, currTime.tm_sec, 0, -1, -1))
                    
            elif (msg.type == INPUT_MIN and mode == 1):
                if(c.datetime.tm_mday < 30 ):
                    newDay = currTime.tm_mday + 1
                    c.datetime = time.struct_time((currTime.tm_year, currTime.tm_mon, newDay, currTime.tm_hour, currTime.tm_min, currTime.tm_sec, 0, -1, -1))
                else:
                    c.datetime = time.struct_time((currTime.tm_year, currTime.tm_mon, 1, currTime.tm_hour, currTime.tm_min, currTime.tm_sec, 0, -1, -1))  
        
        month = currTime.tm_mon
        day = currTime.tm_mday
        hour = currTime.tm_hour
        minute = currTime.tm_min
        sec = currTime.tm_sec
        
        if(hour >= 10):
            hourtens = get_tens(hour)[1]
            hourones = get_tens(hour)[0]
        else:
            hourtens = 0
            hourones = hour
        if(minute >= 10):
            mintens = get_tens(minute)[1]
            minones = get_tens(minute)[0]
        else:
            mintens = 0
            minones = minute
        if(day >= 10):
            daytens = get_tens(day)[1]
            dayones = get_tens(day)[0]
        else:
            daytens = 0
            dayones = day
        if(month == 1):
            montens = "J"
            monones = "A"
        elif(month == 2):
            montens = "F"
            monones = "E"    
        elif(month == 3):
            montens = "M"
            monones = "R"
        elif(month == 4):
            montens = "A"
            monones = "P"
        elif(month == 5):
            montens = "M"
            monones = "Y"
        elif(month == 6):
            montens = "J"
            monones = "N"
        elif(month == 7):
            montens = "J"
            monones = "L"
        elif(month == 8):
            montens = "A"
            monones = "U"
        elif(month == 9):
            montens = "S"
            monones = "E"
        elif(month == 10):
            montens = "O"
            monones = "C"
        elif(month == 11):
            montens = "N"
            monones = "O"
        elif(month == 12):
            montens = "D"
            monones = "E"
        
        finalTime = [str(hourtens), str(hourones), str(mintens), str(minones), montens, monones, str(daytens), str(dayones)]  #save time strings in single list to reduce message overhead
        
        #send current time to diplay via message
        
        self.send(pyRTOS.Message(SENT_TIME, self, "display_task", finalTime))
        
        yield [pyRTOS.timeout(0.01)]

def ButtonTask(self):
    
    mode = 0
    prev_mode = 0
    hr_in = 0
    prev_hr_in = 0
    min_in = 0
    prev_min_in = 0
    
    yield
    
    while True:
        
        
        if(mode_button.value and prev_mode == 0 and mode == 0):
            mode = 1
            print(mode)
            self.send(pyRTOS.Message(SENT_MODE, self, "time_task", mode))
        elif(mode_button.value and prev_mode == 0 and mode == 1):
            mode = 2
            print(mode)
            self.send(pyRTOS.Message(SENT_MODE, self, "time_task", mode))
        elif(mode_button.value and prev_mode == 0 and mode == 2):
            mode = 0
            print(mode)
            self.send(pyRTOS.Message(SENT_MODE, self, "time_task", mode))
        prev_mode = mode_button.value
        
        if(hr_button.value and prev_hr_in == 0):
            print("hour button caught, sending message")
            self.send(pyRTOS.Message(INPUT_HR, self, "time_task", hr_in))
        prev_hr_in = hr_button.value
        
        if(min_button.value and prev_min_in == 0):
            print("minute button caught, sending message")
            self.send(pyRTOS.Message(INPUT_MIN, self, "time_task", min_in))
        prev_min_in = hr_button.value
        
        
        
            
        
        
        
        yield [pyRTOS.timeout(0.01)]

pyRTOS.add_task(pyRTOS.Task(DisplayTask, name="display_task", mailbox=True))
pyRTOS.add_task(pyRTOS.Task(TimeTask, name="time_task", mailbox=True))
pyRTOS.add_task(pyRTOS.Task(ButtonTask, name="button_task", mailbox=True))
#pyRTOS.add_service_routine(lambda: print("Service Routine Executing"))
pyRTOS.start()



