# This is a program for all ADC Module. It will be imported when we should read analog values.
# convert analog signal to digital signal.
import RPi.GPIO as GPIO
import time

ADC_CS = 11
ADC_CLK = 12
ADC_DIO = 13
# using default pins for backwards compatibility
def setup(cs=11,clk=12,dio=13):
    global ADC_CS, ADC_CLK, ADC_DIO
    ADC_CS=cs
    ADC_CLK=clk
    ADC_DIO=dio
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # Number GPIOs by its physical location
    GPIO.setup(ADC_CS, GPIO.OUT) # Set pins' mode is output
    GPIO.setup(ADC_CLK, GPIO.OUT) # Set pins' mode is output
def destroy():
    GPIO.cleanup()

# using channel = 0 as default for backwards compatibility
def getResult(channel=0): # Get ADC result, input channal
    GPIO.setup(ADC_DIO, GPIO.OUT)
    GPIO.output(ADC_CS, 0)
    
    GPIO.output(ADC_CLK, 0)
    GPIO.output(ADC_DIO, 1); time.sleep(0.000002)
    GPIO.output(ADC_CLK, 1); time.sleep(0.000002)
    GPIO.output(ADC_CLK, 0)
    
    GPIO.output(ADC_DIO, 1); time.sleep(0.000002)
    GPIO.output(ADC_CLK, 1); time.sleep(0.000002)
    GPIO.output(ADC_CLK, 0)
    
    GPIO.output(ADC_DIO, channel); time.sleep(0.000002)
    
    GPIO.output(ADC_CLK, 1)
    GPIO.output(ADC_DIO, 1); time.sleep(0.000002)
    GPIO.output(ADC_CLK, 0)
    GPIO.output(ADC_DIO, 1); time.sleep(0.000002)
    
    dat1 = 0
    for i in range(0, 8):
        GPIO.output(ADC_CLK, 1); time.sleep(0.000002)
        GPIO.output(ADC_CLK, 0); time.sleep(0.000002)
        GPIO.setup(ADC_DIO, GPIO.IN)
        dat1 = dat1 << 1 | GPIO.input(ADC_DIO)

    dat2 = 0
    for i in range(0, 8):
        dat2 = dat2 | GPIO.input(ADC_DIO) << i
        GPIO.output(ADC_CLK, 1); time.sleep(0.000002)
        GPIO.output(ADC_CLK, 0); time.sleep(0.000002)

    GPIO.output(ADC_CS, 1)
    GPIO.setup(ADC_DIO, GPIO.OUT)

    if dat1 == dat2:
        return dat1
    else:
        return 0

def getResult1():
    return getResult(1)

def loop():
    while True:
        res0 = getResult(0)
        res1 = getResult(1)
        time.sleep(0.4)

if __name__ == '__main__': # Program start from here
    setup()
try:
    loop()
except KeyboardInterrupt:
    destroy()