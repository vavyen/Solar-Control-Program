""" This module contains classes and functions to establish a communication with the
 Pylontech US2000B Plus Battery Management System.

**Description:**

    The communication is established over a USB to RS232 adapter, which is connected
    to the console port of the first battery. The console must be initialised with a
    defined string at a baud rate of; 1200,8,n,1. After a successful initialisation
    one can communicate via a text based terminal interface operating at a baud rate
    of; 115200,8,n,1.
    The functions in this module will allow to extract the required information necessary
    for the Solar-Control-Program. The main parameters extracted from the BMS are:
        1. SoC
        2. Voltage
        3. Current
        4. Temperature
The main class in this module (``US2000B``) allows the user to
communicate with the Pylontech US2000B Plus BMS.

"""

import serial,time,re
import numpy as np


# EMBEDDING CIRCUIT CLASS ----------------------------------------------------

class US2000B(object):
    """This class implements the serial connection functions """
    def __init__(self):
        ''' Constructor for this class. '''
        self.__port = 0


    def __del__(self):
        ''' Destructor for this class. '''
        if self.__port !=0:
            self.close()




    def initialise(self, port='/dev/ttyUSB0'):
        """Initialises the console communication fo the US2000B BMS
        Args:
            port: path to serial port. Default='/dev/ttyUSB0'
        Returns: Boolean value True or False"""
        temp_port = serial.Serial(port,1200, timeout=0.05)
        temp_port.write('~20014682C0048520FCC3\r')
        time.sleep(5)
        temp_port = serial.Serial(port,115200, timeout=0.05)
        temp_port.write('\r\n')
        temp_receive = repr(temp_port.read(1000))
        temp_port.close()
        return temp_receive == str("'\\n\\rpylon>\\n\\rpylon>'")

    def open(self, port='/dev/ttyUSB0', baud=115200):
        """Open serial port for communication

        Args:
            port: path to serial port. Default='/dev/ttyUSB0'
            baud: defines the baud rate. Default=115200

        Returns: Boolean value True or False

        """
        self.__port = serial.Serial(port,baud, timeout=0.05)
        return self.__port.is_open

    def close(self):
        """Close serial port

        Returns: Boolean value True or False

        """
        self.__port.close()
        return not self.__port.is_open

    def is_connected(self):
        """This function checks if the connection to the BMS is established
        and if the BMS responds to readout commands.

        Returns: Boolean value True or False

        """
        self.__port.write('\r\n')
        temp_receive = repr(self.__port.read(1000))
        return temp_receive == str("'\\n\\rpylon>\\n\\rpylon>'")


    def read_SOC(self,n_modules=1):
        """This function returns the State of Charge value of the
        Pylontech Batteries.
        Args:
            n_modules: number of modules to be read. Default=1

        Returns: list of length n_modules containing numpy arrays with the [SOC] dtype=float64.

        """
        try:
            SOC_array = np.zeros((n_modules, 1))
            self.__port.write('pwr\r')
            time.sleep(0.5)
            rec_str = self.__port.read(2200)
            rec_int = re.findall(r'\d+', rec_str)
            #Writes values into SOC_array and returns it.
            if n_modules == 1:
                SOC_array[0,0] = str(rec_int[8])
                return SOC_array
            if n_modules == 2:
                SOC_array[0,0] = str(rec_int[8])
                SOC_array[1,0] = str(rec_int[23])
                return SOC_array
            if n_modules == 3:
                SOC_array[0,0] = str(rec_int[8])
                SOC_array[1,0] = str(rec_int[23])
                SOC_array[2,0] = str(rec_int[38])
                return SOC_array
            if n_modules == 4:
                SOC_array[0,0] = str(rec_int[8])
                SOC_array[1,0] = str(rec_int[23])
                SOC_array[2,0] = str(rec_int[38])
                SOC_array[3,0] = str(rec_int[53])
                return SOC_array
            if n_modules == 5:
                SOC_array[0,0] = str(rec_int[8])
                SOC_array[1,0] = str(rec_int[23])
                SOC_array[2,0] = str(rec_int[38])
                SOC_array[3,0] = str(rec_int[53])
                SOC_array[4,0] = str(rec_int[68])
                return SOC_array
            if n_modules == 6:
                SOC_array[0,0] = str(rec_int[8])
                SOC_array[1,0] = str(rec_int[23])
                SOC_array[2,0] = str(rec_int[38])
                SOC_array[3,0] = str(rec_int[53])
                SOC_array[4,0] = str(rec_int[68])
                SOC_array[5,0] = str(rec_int[83])
                return SOC_array
            if n_modules == 7:
                SOC_array[0,0] = str(rec_int[8])
                SOC_array[1,0] = str(rec_int[23])
                SOC_array[2,0] = str(rec_int[38])
                SOC_array[3,0] = str(rec_int[53])
                SOC_array[4,0] = str(rec_int[68])
                SOC_array[5,0] = str(rec_int[83])
                SOC_array[6,0] = str(rec_int[98])
                return SOC_array
            if n_modules == 8:
                SOC_array[0,0] = str(rec_int[8])
                SOC_array[1,0] = str(rec_int[23])
                SOC_array[2,0] = str(rec_int[38])
                SOC_array[3,0] = str(rec_int[53])
                SOC_array[4,0] = str(rec_int[68])
                SOC_array[5,0] = str(rec_int[83])
                SOC_array[6,0] = str(rec_int[98])
                SOC_array[7,0] = str(rec_int[113])
                return SOC_array
            else:
                return SOC_array
        except:
            print"ERROR no communication possible, check if the connection has been opened with open()"

    def read_BMS(self,n_modules=1):
        """This function returns the values of the: SoC, Voltage, Current, and Temperature
        provided by the Pylontech BMS.
        Args:
            n_modules: number of modules to be read. Default=1

        Returns: list of length n_modules containing numpy arrays with the:
        [SoC, Voltage, Current, Temperature] dtype=float64.

        """
        try:
            BMS_array = np.zeros((n_modules, 4))
            self.__port.write('pwr\r')
            time.sleep(0.5)
            rec_str = self.__port.read(2200)
            rec_int = re.findall(r'\d+', rec_str)
            #Writes values into BMS_array and returns it.
            if n_modules == 1:
                BMS_array[0,0] = str(rec_int[8])#SOC
                BMS_array[0,1] = str(rec_int[1])#Voltage
                BMS_array[0,2] = str(rec_int[2])#Current
                BMS_array[0,3] = str(rec_int[3])#Temperature
                return BMS_array

            if n_modules == 2:
                BMS_array[0,0] = str(rec_int[8])#SOC
                BMS_array[0,1] = str(rec_int[1])#Voltage
                BMS_array[0,2] = str(rec_int[2])#Current
                BMS_array[0,3] = str(rec_int[3])#Temperature

                BMS_array[1,0] = str(rec_int[23])#SOC
                BMS_array[1,1] = str(rec_int[16])#Voltage
                BMS_array[1,2] = str(rec_int[17])#Current
                BMS_array[1,3] = str(rec_int[18])#Temperature
                return BMS_array

            if n_modules == 3:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature
                return BMS_array

            if n_modules == 4:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature
                return BMS_array

            if n_modules == 5:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature

                BMS_array[4, 0] = str(rec_int[68])  # SOC
                BMS_array[4, 1] = str(rec_int[61])  # Voltage
                BMS_array[4, 2] = str(rec_int[62])  # Current
                BMS_array[4, 3] = str(rec_int[63])  # Temperature
                return BMS_array

            if n_modules == 6:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature

                BMS_array[4, 0] = str(rec_int[68])  # SOC
                BMS_array[4, 1] = str(rec_int[61])  # Voltage
                BMS_array[4, 2] = str(rec_int[62])  # Current
                BMS_array[4, 3] = str(rec_int[63])  # Temperature

                BMS_array[5, 0] = str(rec_int[83])  # SOC
                BMS_array[5, 1] = str(rec_int[76])  # Voltage
                BMS_array[5, 2] = str(rec_int[77])  # Current
                BMS_array[5, 3] = str(rec_int[78])  # Temperature
                return BMS_array

            if n_modules == 7:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature

                BMS_array[4, 0] = str(rec_int[68])  # SOC
                BMS_array[4, 1] = str(rec_int[61])  # Voltage
                BMS_array[4, 2] = str(rec_int[62])  # Current
                BMS_array[4, 3] = str(rec_int[63])  # Temperature

                BMS_array[5, 0] = str(rec_int[83])  # SOC
                BMS_array[5, 1] = str(rec_int[76])  # Voltage
                BMS_array[5, 2] = str(rec_int[77])  # Current
                BMS_array[5, 3] = str(rec_int[78])  # Temperature

                BMS_array[6, 0] = str(rec_int[98])  # SOC
                BMS_array[6, 1] = str(rec_int[91])  # Voltage
                BMS_array[6, 2] = str(rec_int[92])  # Current
                BMS_array[6, 3] = str(rec_int[93])  # Temperature
                return BMS_array

            if n_modules == 8:
                BMS_array[0, 0] = str(rec_int[8])  # SOC
                BMS_array[0, 1] = str(rec_int[1])  # Voltage
                BMS_array[0, 2] = str(rec_int[2])  # Current
                BMS_array[0, 3] = str(rec_int[3])  # Temperature

                BMS_array[1, 0] = str(rec_int[23])  # SOC
                BMS_array[1, 1] = str(rec_int[16])  # Voltage
                BMS_array[1, 2] = str(rec_int[17])  # Current
                BMS_array[1, 3] = str(rec_int[18])  # Temperature

                BMS_array[2, 0] = str(rec_int[38])  # SOC
                BMS_array[2, 1] = str(rec_int[31])  # Voltage
                BMS_array[2, 2] = str(rec_int[32])  # Current
                BMS_array[2, 3] = str(rec_int[33])  # Temperature

                BMS_array[3, 0] = str(rec_int[53])  # SOC
                BMS_array[3, 1] = str(rec_int[46])  # Voltage
                BMS_array[3, 2] = str(rec_int[47])  # Current
                BMS_array[3, 3] = str(rec_int[48])  # Temperature

                BMS_array[4, 0] = str(rec_int[68])  # SOC
                BMS_array[4, 1] = str(rec_int[61])  # Voltage
                BMS_array[4, 2] = str(rec_int[62])  # Current
                BMS_array[4, 3] = str(rec_int[63])  # Temperature

                BMS_array[5, 0] = str(rec_int[83])  # SOC
                BMS_array[5, 1] = str(rec_int[76])  # Voltage
                BMS_array[5, 2] = str(rec_int[77])  # Current
                BMS_array[5, 3] = str(rec_int[78])  # Temperature

                BMS_array[6, 0] = str(rec_int[98])  # SOC
                BMS_array[6, 1] = str(rec_int[91])  # Voltage
                BMS_array[6, 2] = str(rec_int[92])  # Current
                BMS_array[6, 3] = str(rec_int[93])  # Temperature

                BMS_array[7, 0] = str(rec_int[113])  # SOC
                BMS_array[7, 1] = str(rec_int[106])  # Voltage
                BMS_array[7, 2] = str(rec_int[107])  # Current
                BMS_array[7, 3] = str(rec_int[108])  # Temperature
                return BMS_array

            else:
                return BMS_array
        except:
            print"ERROR no communication possible, check if the connection has been opened with open()"


