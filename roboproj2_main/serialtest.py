import serial

# configure the serial connection
# replace 'COM3' with the serial port name of the device on the other end of the USB-USB cable
ser = serial.Serial('COM3', 9600)
ser.timeout = 1

# write data to the serial connection
ser.write(b'Hello, World!')

# read data from the serial connection
data = ser.readline()
print(data)

# close the serial connection
ser.close()
