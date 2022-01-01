import time
import sys
import tfmplus as tfmP
from tfmplus import *

print("Script version 1.0.0, written by Abul Al Arabi")
serialPort = input("Enter the serial port (example: /dev/ttyUSB0): ")
serialRate = 115200

print( "Opening Serial port: ", end= '')
if( tfmP.begin( serialPort, serialRate)):
    print( "ready.")

else:
    print( "not ready")
    sys.exit()   

print( "Performing System reset: ", end= '')

if( tfmP.sendCommand( SYSTEM_RESET, 0)):
    print( "passed.")

else:
    tfmP.printReply()

print("Please wait...")
time.sleep(1)  

print( "Checking Firmware version: ", end= '')

if( tfmP.sendCommand( OBTAIN_FIRMWARE_VERSION, 0)):
    print( str( tfmP.version[ 0]) + '.', end= '')
    print( str( tfmP.version[ 1]) + '.', end= '')
    print( str( tfmP.version[ 2]))

else:
    tfmP.printReply()

print( "Fetching Data-Frame rate: ", end= '')

if( tfmP.sendCommand( SET_FRAME_RATE, FRAME_20)):
    print( str(FRAME_20) + 'Hz')

else:
    tfmP.printReply()

print("Please wait...")
time.sleep(1)     

def setI2CMode():
    print("Setting device to i2c mode")
    tfmP.sendCommand( SET_I2C_MODE, 0)
    print("Please wait...")
    time.sleep(1)
    print('Set the device to i2c mode: DONE')
    print('Saving settings')
    tfmP.sendCommand( SAVE_SETTINGS, 0)
    print("Please wait...")
    time.sleep(1)
    print("Saving DONE")
    time.sleep(0.5)
    print('Rebooting into i2c mode, connection to serial will be lost...')
    
    if( tfmP.sendCommand( SYSTEM_RESET, 0)):
        print( "passed.")

    else:
        tfmP.printReply()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def readSensor():
    print("Reading from the sensor, press ctrl+c anytime to exit")
    try:
        while True:
            time.sleep(0.05)  
            if( tfmP.getData()):
                print( f" Dist: {tfmP.dist:{3}}cm ", end= '')   # display distance,
                print( " | ", end= '')
                print( f"Flux: {tfmP.flux:{4}d} ",   end= '')   # display signal strength/quality,
                print( " | ", end= '')
                print( f"Temp: {tfmP.temp:{2}}°C",  )   # display temperature,

            else:                  
              tfmP.printFrame()

    except KeyboardInterrupt:
        print( 'Keyboard Interrupt')

selection = input("1. Read data\n2. Set i2c mode\nEnter selection: ")
if selection == '1':
    readSensor()
elif selection == '2':
    setI2CMode()
    
exit()
