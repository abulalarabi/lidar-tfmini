# tfmini lidar
This repo contains codes and instructions for working with TFMINI LIDAR in Jetson Xavier. This should also work with Jetson Nano.

## 1. Install dependencies by running: 

```
pip3 install -r dep.txt
```

## 2. Testing the sensor:

The seti2c.py file contails necessary code for testing and setting the device to i2c over serial communication. Run the following command to read using the serial port:

```
python3 seti2c.py
```

Enter the ***serial port*** addess and select ***option 1*** to read data from the sensor.

## 3. Set device to i2c:

The device can be set to i2c mode by running the command:

```
python3 seti2c.py
```

Then enter the ***serial port*** address and select ***option 2*** to set the sensor to i2c mode.


## 4. Using the sensor:
The ***driver.py*** file is the i2c driver for the lidar sensor. First import the file and then declare the ***tfMiniS*** object. The object has three parameters: ***addr, bus, debug***. ***debug*** is by default false.

```
import i2cdriver as driver
lidar = driver.tfMiniS(addr = 0x10, bus = 32)
```

Then call the ***getData()*** function. The function returns 1 if the read was successful. Else, returns 0. The data and status can be read as following:

```
if lidar.getData(): # check if the data was read successfully
    print('Distance: ',lidar1.dist,'\t Flux: ', lidar1.flux, '\t LTemp: ',lidar1.temp) # print the values
    
else:
    print(lidar1.status) # if reading fails then print the status
```

The example script can be found in the ***read.py*** file.


## 5. Multiple sensors:
The ***tfMiniS*** can be used to create an array of sensors and read from multiple sensors. Such as:

```
lidars = [driver.tfMiniS(addr = addr[i], bus = bus[i]) for i in range(0,NUM_OF_SENSORS)]
```

The multi-sensor script can be found in  ***multi_lidar.py*** file.
