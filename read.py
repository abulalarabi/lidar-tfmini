import i2cdriver as driver # import the driver
import time

lidar1 = driver.tfMiniS(addr = 0x10, bus = 32) # create a sensor instance

while True:
    if lidar1.getData(): # check if the data was read successfully
        print('Distance: ',lidar1.dist,'\t Flux: ', lidar1.flux, '\t LTemp: ',lidar1.temp) # print the values
    else:
        print(lidar1.status) # if reading fails then print the status
    
    time.sleep(0.5) # add latency before reading another one