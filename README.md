# lidar-tfmini

## 1. Install dependencies by running: 

*pip3 install -r dep.txt*


## 2. Test the sensor by running:

*python3 seti2c.py*


Enter the serial port addess and select option 1 to read data from the sensor.

## 3. Set device to i2c:

*python3 seti2c.py*


Enter the serial port address and select option 2 to set the sensor to i2c mode.


## 4. Using the sensor:
The *driver.py* file is the i2c driver for the lidar sensor. First import the file and then declare the *tfMiniS* object. The object has three parameters: *addr, bus, debug*. *debug* is by default false.


*import i2cdriver as driver*

*lidar = driver.tfMiniS(addr = 0x10, bus = 32)*


Then call the *getData()* function. The function returns 1 if the read was successful. Else, returns 0. The data and status can be read as following:


*if lidar1.getData(): # check if the data was read successfully*

    *print('Distance: ',lidar1.dist,'\t Flux: ', lidar1.flux, '\t LTemp: ',lidar1.temp) # print the values*
    
*else:*

    *print(lidar1.status) # if reading fails then print the status*
