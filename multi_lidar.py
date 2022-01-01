import i2cdriver as driver # import the driver
import time

NUM_OF_SENSORS = 4 # number of sensors
addr = [0x10, 0x10, 0x10, 0x10] # address of all the sensors
bus = [30,31,32,33] # all buses

lidars = [driver.tfMiniS(addr = addr[i], bus = bus[i]) for i in range(0,NUM_OF_SENSORS)] # create sensor instance

while True: # main loop
    print('===============================================')
    for i in range(0,NUM_OF_SENSORS):
        if lidars[i].getData():
            print('Sensor ',i, ': Distance: ',lidars[i].dist,'\t Flux: ', lidars[i].flux, '\t LTemp: ',lidars[i].temp)
        else:
            print('Sensor ',i,': ERROR: ',lidars[i].status)

    time.sleep(0.5)