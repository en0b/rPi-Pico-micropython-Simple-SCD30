from machine import Pin, I2C
import struct

#init i2c
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000) 
i2c.scan()

#init rdy pin
rdy = Pin(7, Pin.IN)

#initialize sensor
SCD30_ADR = 97;
COMMAND_CONTINUOUS_MEASUREMENT = b'\x00\x10\x00\x00\x00';
COMMAND_SET_MEASUREMENT_INTERVAL =b'\x46\x00\x00\x02\x00';
COMMAND_AUTOMATIC_SELF_CALIBRATION = b'\x53\x06\x00\x01\x00';
COMMAND_READ_MEASUREMENT = b'\x03\x00'; 

i2c.writeto(SCD30_ADR, COMMAND_CONTINUOUS_MEASUREMENT)
i2c.writeto(SCD30_ADR, COMMAND_SET_MEASUREMENT_INTERVAL)
i2c.writeto(SCD30_ADR, COMMAND_AUTOMATIC_SELF_CALIBRATION)

while 1:
    
    #data ready?
    if 1 == rdy.value():
        i2c.writeto(SCD30_ADR, COMMAND_READ_MEASUREMENT)
        buf = i2c.readfrom(SCD30_ADR, 18)
        
        co2_b =  bytearray(4)
        co2_b[0] = buf[0]
        co2_b[1] = buf[1]
        co2_b[2] = buf[3]
        co2_b[3] = buf[4]
        co2 = struct.unpack('>f', co2_b)
        
        temp_b =  bytearray(4)
        temp_b[0] = buf[6]
        temp_b[1] = buf[7]
        temp_b[2] = buf[9]
        temp_b[3] = buf[10]
        temp = struct.unpack('>f', temp_b)
        
        humi_b =  bytearray(4)
        humi_b[0] = buf[12]
        humi_b[1] = buf[13]
        humi_b[2] = buf[15]
        humi_b[3] = buf[16]
        humi = struct.unpack('>f', humi_b)
        
        print("")
        print("SCD30 Reader:")
        print("----------------------------")
        print("CO2: " + '{:6.2f}'.format(co2[0]) + " ppm")
        print("T: " + '{:6.2f}'.format(temp[0]) + " °C")
        print("H: " + '{:6.2f}'.format(humi[0]) + " %RH")


