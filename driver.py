# prepared by Al Arabi
import time
from smbus import SMBus

# error codes
class params:
    def __init__(self):
        self.TFMP_READY        =  0  # no error
        self.TFMP_HEADER       =  2  # no header found
        self.TFMP_CHECKSUM     =  3  # checksum doesn't match
        self.TFMP_TIMEOUT      =  4  # I2C timeout
        self.TFMP_PASS         =  5  # reply from some system commands
        self.TFMP_FAIL         =  6  #           "
        self.TFMP_I2CREAD      =  7
        self.TFMP_I2CWRITE     =  8  # I2C write failure
        self.TFMP_I2CLENGTH    =  9
        self.TFMP_WEAK         = 10  # Signal Strength <= 100
        self.TFMP_STRONG       = 11  # Signal Strength saturation
        self.TFMP_FLOOD        = 12  # Ambient Light saturation
        self.TFMP_MEASURE      = 13
        self.TFMP_FRAME_SIZE =  9   # Size of one data frame = 9 bytes
        self.CMD_CM = [0x05, 0x00, 0x01, 0x60]   #  command to return distance data in centimeters.

# from the tf mini s dataset
'''- - - - - -  TFMini Plus data formats  - - - - - - - - -
  Data Frame format:
  Byte0  Byte1  Byte2   Byte3   Byte4   Byte5   Byte6   Byte7   Byte8
  0x59   0x59   Dist_L  Dist_H  Flux_L  Flux_H  Temp_L  Temp_H  CheckSum_
  Data Frame Header character: Hex 0x59, Decimal 89, or "Y"
  Command format:
  Byte0  Byte1   Byte2   Byte3 to Len-2  Byte Len-1
  0x5A   Length  Cmd ID  Payload if any   Checksum
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''



class tfMiniS:
    def __init__(self, addr=0x10, bus=0, debug=False):
        self.params = params()
        self.addr = int(addr)
        self.bus = bus
        self.status = self.params.TFMP_READY
        self.dist = 0
        self.flux = 0
        self.temp = 0
        self.tempF = 0
        self.frame = [0,0,0,0,0,0,0,0,0]
        self.debug = debug
        if self.debug: print('Driver written by Al Arabi, www.abulalarabi.com')
    def begin(self):
        try:
            self.smb = SMBus( self.bus)
            self.smb.open( self.bus)
            self.smb.write_quick(self.addr)
            self.smb.close()
            return True
        except Exception:
            print(Exception)
            return False

    def getData(self):
        self.status = self.params.TFMP_READY;
        if self.debug: print('Opening i2c')
        self.smb = SMBus( self.bus)
        self.smb.write_i2c_block_data(self.addr, 0x5a, self.params.CMD_CM)
        if self.debug: print('Receiving data')
        #  get frame of data from device
        self.frame = self.smb.read_i2c_block_data( self.addr, 0, self.params.TFMP_FRAME_SIZE)
        if self.debug: print('Frame: ', [hex(self.frame[i]) for i in range(0,len(self.frame))])
        #  done communication
        self.smb.close()


        #  checksum test
        if self.debug: print('Checksum test')
        chkSum = 0
        for i in range( self.params.TFMP_FRAME_SIZE - 1): chkSum += self.frame[ i]
        if( chkSum & 0xff != self.frame[ self.params.TFMP_FRAME_SIZE - 1]):
            self.status = self.params.TFMP_CHECKSUM  # If not same, set error...
            return False            # and return "false."
        if self.debug: print('Parsing data')
        
        self.dist = (self.frame[3] << 8) + self.frame[2]
        self.flux = (self.frame[5] << 8) + self.frame[4]
        self.temp = (self.frame[7] << 8) + self.frame[6]

        self.temp = ( self.temp >> 3) - 256
        self.tempF = ( self.temp * 9 / 5) + 32
        
        if self.debug: print('Data validating')

        if( self.dist == -1):
            self.status = self.params.TFMP_WEAK
        elif( self.flux == -1):
            self.status = self.params.TFMP_STRONG #signal strength is 'saturated'
        elif( self.dist == -4):
            self.status = self.params.TFMP_FLOOD # Ambient Light saturation
        else:
            self.status = self.params.TFMP_READY

        if( self.status != self.params.TFMP_READY):
            if self.debug: print('Unsuccessful')
            return False;
        else:
            if self.debug: print('Reading success')
            return True;