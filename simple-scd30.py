""" simple script to read out a Sensirion SCD30 with a Raspberry Pi Pico """

from machine import Pin, I2C
import struct

# function to extract the float numbers from the sensor response
def unpack_scd30_float(b0, b1, b2, b3):
    tmp = bytearray(4)
    tmp[0] = b0
    tmp[1] = b1
    tmp[2] = b2
    tmp[3] = b3
    return struct.unpack('>f', tmp)


# init i2c (default settings)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000) 
i2c.scan()

# init rdy pin
rdy = Pin(7, Pin.IN)

# sensor constants
# i2c sensor address (already shifted left by 1bit)
SCD30_ADR = 97;
# sensor automatically starts measurement. RDY pin signals measurement ready.
COMMAND_CONTINUOUS_MEASUREMENT = b'\x00\x10\x00\x00\x00';
# 2s measurement Interval
COMMAND_SET_MEASUREMENT_INTERVAL =b'\x46\x00\x00\x02\x00';
# automatic self calibration on
COMMAND_AUTOMATIC_SELF_CALIBRATION = b'\x53\x06\x00\x01\x00';
# command that needs to be sent before reading out the measurement result
COMMAND_READ_MEASUREMENT = b'\x03\x00'; 

# initialize sensor
i2c.writeto(SCD30_ADR, COMMAND_CONTINUOUS_MEASUREMENT)
i2c.writeto(SCD30_ADR, COMMAND_SET_MEASUREMENT_INTERVAL)
i2c.writeto(SCD30_ADR, COMMAND_AUTOMATIC_SELF_CALIBRATION)

# main loop
while 1:
    
    # data ready?
    if 1 == rdy.value():
        i2c.writeto(SCD30_ADR, COMMAND_READ_MEASUREMENT)
        buf = i2c.readfrom(SCD30_ADR, 18)
        
        co2 = unpack_scd30_float(buf[0], buf[1], buf[3], buf[4])
        temp = unpack_scd30_float(buf[6], buf[7], buf[9], buf[10])
        humi = unpack_scd30_float(buf[12], buf[13], buf[15], buf[16])
        
        print("")
        print("SCD30 Reader:")
        print("----------------------------")
        print("CO2: " + '{:6.2f}'.format(co2[0]) + " ppm")
        print("T: " + '{:6.2f}'.format(temp[0]) + " °C")
        print("H: " + '{:6.2f}'.format(humi[0]) + " %RH")
    

