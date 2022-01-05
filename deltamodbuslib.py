import serial
from time import sleep


class deltaDriver:
    #set parameters
    ser              = serial.Serial()
    slave            = '01'                 # slave number              -> 2 digits hexadecimal value
    port             = 'COM9'               # com port                  -> COM1=0, COM2=1, COM3=2 ...
    baudrate         = 9600                 # baudrate                  -> 4800, 9600, 19200, 38400, 57600, 115200
    bytesize         = 7                    # data bit                  -> 7 or 8
    parity           = 'E'                  # parity                    -> O (odd), E (even) or N (None)
    stopbits         = serial.STOPBITS_ONE  # stop bit                  -> 1 or 2
    timeout          = 1                    # timeout                   -> 0 for no timeout, (seconds)
    error            = ''                   # last error message
    package          = ''
    package_utf      = ''
    package_stx      = ':'                  # package starting char
    package_address  = ''                   # 4 digit hexadecimal number that reffers address
    package_command  = ''                   # 01=read coil status, 02=I/O read input status, 03=read holding register, 05=coil set/reset, 06=preset single register ...
    package_data     = 0                    # parameter value (decimal)
    package_data_hex = ''                   # parameter value (4 digit hexadecimal string)
    package_end      = '\r\n'               # package ending char
    package_lrc      = ''                   # check sum

    def __init__(self):
        self.ser.port       = self.port
        self.ser.boudrate   = self.baudrate
        self.ser.bytesize   = self.bytesize
        self.ser.parity     = self.parity
        self.ser.stopbits   = self.stopbits
        self.ser.timeout    = self.timeout

    def address(device, no):
        # takes input as 1 char as device, device number as integer
        if no >= 0:
            starting_hex = {'S': '0000', 'X': '0400', 'Y': '0500',
                            'T': '0600', 'M': '0800', 'C': '0E00', 'D': '1000'}
            if device not in ['S', 'X', 'Y', 'T', 'M', 'C', 'D']:
                return "Wrong Device Address"
            else:
                return format(int(starting_hex[device], 16) + no, '04X')
        else:
            return "Wrong Device Number"

    def readResponse(self):
        sleep(0.1)
        response = self.ser.read(self.ser.in_waiting) 
        return response.decode('utf-8'),


    def open(self):
        try:
            self.ser.open()
        except:
            pass
        return self.ser.isOpen()


    def close(self):
        #closes serial port, return serial status
        if self.ser.isOpen():
            try:
                self.ser.close()
            except:
                pass
        return self.ser.isOpen()


    def calcLRC(self):
        #LRC calculation, return 2 digits hexadecimal value
        self.package_lrc = ''

        if len(self.package_data_hex) % 2 == 0:
            #hexadecimal to decimal convertion
            lrc = int(self.slave, 16)
            lrc = int(self.package_command, 16) + lrc

            #takes the data in binary groups and sums it as decimal.
            for i in range(0, len(self.package_data_hex), 2):
                lrc += int (self.package_data_hex[i:i+2], 16)
            
            lrc = lrc % 256
            lrc = 256 - lrc
            
            #2 digit hexadecimal conversion for return
            self.package_lrc = format(lrc, '02X')


        return self.package_lrc
    

    def createPackage(self):
        #Creates the data package to be sent to the serial
        package =  self.package_stx
        package += self.slave
        package += self.package_command
        package += self.package_data_hex
        package += self.calcLRC()
        package += self.package_end

        self.package_utf = package
        self.package = package.encode('utf-8')
    

    def readRegister(self, address):
        #reads register from PLC 
        #takes input as 4 digit hexadecimal address
        response = None

        self.package_address = address
        self.package_command = '03'
        
        self.package_data_hex = self.package_address
        self.package_data_hex += '0001'

        if self.open():
            self.createPackage()
            self.ser.write(self.package)

            response = self.readResponse()
            self.close()

            if len(response) > 0:
                if response[3:5] == '03':
                    response = int(response[7:11], 16)
                else:
                    self.error = response[:-2]
                    raise RuntimeError
        
        return response


    def readCoil(self, address):
        #reads coil from PLC 
        #takes input as 4 digit hexadecimal address
        response = None

        self.package_address = address
        self.package_command = '01'
        
        self.package_data_hex = self.package_address
        self.package_data_hex += '0001'

        if self.open():
            self.createPackage()
            self.ser.write(self.package)

            response = self.readResponse()
            self.close()

            if len(response) > 0:
                if response[3:5] == '01':
                    response = int(response[7:9], 16)
                    response &= 1
                else:
                    self.error = response[:-2]
                    raise RuntimeError
        
        return response


    def readInput(self, address):
        #reads Input from PLC 
        #takes input as 4 digit hexadecimal address
        response = None

        self.package_address = address
        self.package_command = '02'
        
        self.package_data_hex = self.package_address
        self.package_data_hex += '0001'

        if self.open():
            self.createPackage()
            self.ser.write(self.package)

            response = self.readResponse()
            self.close()

            if len(response) > 0:
                if response[1:3] == '01':
                    print(response)
                    response = int(response[5:7], 16)
                    response &= 1
                else:
                    self.error = response[:-2]
                    raise RuntimeError
        
        return response


    def setRegister(self, address, data):
        #write data to register 
        #takes input as 4 digit hexadecimal address and data as decimal integer
        self.package_address = address
        self.package_data = data
        self.package_command = '06'
        
        self.package_data_hex = self.package_address
        self.package_data_hex += format(self.package_data, '04X')

        if self.open():
            self.createPackage()
            self.ser.write(self.package)

            response = self.readResponse()
            self.close()

            if response == self.package:
                return True
            else:
                self.error = response[:-2]
        
        return False


    def setCoil(self, address, data=65280):
        #set coil on or off 
        #takes input as 4 digit hexadecimal address and data as decimal integer
        # reset if data is 0, set if other than 0
        self.package_address = address
        
        if data == 0: self.package_data = 0
        else: self.package_data = 65280

        self.package_command = '05'

        self.package_data_hex = self.package_address
        self.package_data_hex += format(self.package_data, '04X')

        if self.open():
            self.createPackage()
            self.ser.write(self.package)

            response = self.readResponse()
            self.close()

            if response == self.package_utf:
                return True
            else:
                self.error = response[:-2]

        return False


    def resetCoil(self, address):
        #resets coil at input address
        self.package_address = address
        return self.setCoil(self.package_address, data = 0)
    
    # if __name__ == '__main__':
    #     x       = deltaDriver()
    #     x.port  = 0
    #     x.slave  = '01'
    #     x.baudrate  = 38400
    #     x.bytesize  = 7
    #     x.parity  = 'N'
    #     x.stopbits  = 2
    #     print(x.readRegister(address='0000'))

delta = deltaDriver()