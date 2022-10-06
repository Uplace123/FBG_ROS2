import socket

from dataclasses import dataclass
import numpy as np


class StatusHeader:
    HEADER_SIZE = 88
    fullSpectrumRadix: int = None
    serialNumber: int = None
    granularity: float = None

    numCH1Sensors: int = None
    numCH2Sensors: int = None
    numCH3Sensors: int = None
    numCH4Sensors: int = None

    startWavelength: float = None
    endWavelength: float = None

    timeStamp: float = None  # ms

    bufferSize: int = None
    headerSize: int = None
    headerVersion: int = None

class PeakContainer:
    CH1: np.ndarray = None
    CH2: np.ndarray = None
    CH3: np.ndarray = None
    CH4: np.ndarray = None
    # end de

class PeakMessage:
    header = StatusHeader()
    peak_container = PeakContainer()

class Interrogator():
    peak_msg = PeakMessage()
    available_ch = {}

    def __init__(self, address, port, timeout: float = 1):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.socketTimeout = timeout
        self.is_ready = False
        self.connect(address,port)
        

    @property
    def socketTimeout(self):
        return self.sock.gettimeout()

    @socketTimeout.setter
    def socketTimeout(self, timeout: float):
        self.sock.settimeout(timeout)

    def connect(self,address,port):
        try:
            self.sock.connect((address,port))
            self.is_ready = True
            data = self.sendCommand("#GET_UNBUFFERED_DATA")
            self.peak_msg.header = self.parseHeader(data)
            self.check_ch_available()
            # get header
        except socket.timeout:
            self.is_ready = False
            return None

    def getData(self) -> np.ndarray:
        """ return PeakMessage object, None if not connected"""
        if not self.is_ready:
            print("Fail to connect with Interrogator!")
            return None
        data = self.sendCommand("#GET_UNBUFFERED_DATA")

        offset = self.peak_msg.header.HEADER_SIZE

        # sm130 has 4 channel
        for ch,num_peaks in self.available_ch.items():          
                
            temp_ch_val = np.zeros(num_peaks)


            # num_peaks should be the same for available channels
            for i in range(num_peaks):
                peak_val = int.from_bytes(data[offset:offset + 4],'little' ) / self.peak_msg.header.granularity
                offset += 4
                temp_ch_val[i] = peak_val
            # end for

            if ch == 'CH1':
                self.peak_msg.peak_container.CH1 = temp_ch_val
            elif ch == 'CH2':
                self.peak_msg.peak_container.CH2 = temp_ch_val
            elif ch == 'CH3':
                self.peak_msg.peak_container.CH3 = temp_ch_val
            elif ch == 'CH4':
                self.peak_msg.peak_container.CH4 = temp_ch_val
            else:
                pass
            # end if
        # end for
        return self.get_raw_data()
    # end getData

    def check_ch_available(self):
        # find the available channel
        if self.peak_msg.header.numCH1Sensors != 0:
            self.available_ch['CH1'] = self.peak_msg.header.numCH1Sensors
        else:
            pass
        if self.peak_msg.header.numCH2Sensors != 0:
            self.available_ch['CH2'] = self.peak_msg.header.numCH2Sensors
        else:
            pass
        if self.peak_msg.header.numCH3Sensors != 0:
            self.available_ch['CH3'] = self.peak_msg.header.numCH3Sensors
        else:
            pass
        if self.peak_msg.header.numCH4Sensors != 0:
            self.available_ch['CH4'] = self.peak_msg.header.numCH4Sensors
        else:
            pass
    # end check_ch_available

        


    def get_raw_data(self) -> np.ndarray:
        # return CH raw data
        raw_data = None
        for ch,num_peaks in self.available_ch.items():          
            if ch == 'CH1':
                if raw_data is None:
                    raw_data = self.peak_msg.peak_container.CH1
                else:
                    raw_data = np.vstack((raw_data,self.peak_msg.peak_container.CH1))
                # end if
            else:
                pass
            if ch == 'CH2':
                if raw_data is None:
                    raw_data = self.peak_msg.peak_container.CH2
                else:
                    raw_data = np.vstack((raw_data,self.peak_msg.peak_container.CH2))
                # end if
            else:
                pass

            if ch == 'CH3':
                if raw_data is None:
                    raw_data = self.peak_msg.peak_container.CH3
                else:
                    raw_data = np.vstack((raw_data,self.peak_msg.peak_container.CH3))
                # end if
            else:
                pass

            if ch == 'CH4':
                if raw_data is None:
                    raw_data = self.peak_msg.peak_container.CH4
                else:
                    raw_data = np.vstack((raw_data,self.peak_msg.peak_container.CH4))
                # end if
            else:
                pass
        return raw_data
    # end get_raw_data

    
    def getHeader(self):
        # return header info
        # todo
        print("getHeader is called!")
        print("function not finish yet")

    #end get_Header

    def sendCommand( self, command: str):
        """ return byte string of response"""
        if not self.is_ready:
            raise ConnectionError("Interrogator is not connected!")
        if not command.endswith("\n"):
            command += '\n'
        self.sock.send( command.encode('utf-8'))
        msg_size = int(self.sock.recv(10))
        msg = b""
        while len(msg) < msg_size:
            msg+=self.sock.recv(msg_size)
        return msg


    @staticmethod
    def parseHeader( data: bytes ):
        header = StatusHeader()
        header.fullSpectrimRadix = int.from_bytes( data[ 0:8 ], 'little' )
        header.serialNumber = int.from_bytes( data[ 7 * 4:7 * 4 + 4 ], 'little' )

        header.granularity = int.from_bytes( data[ 18 * 4:18 * 4 + 4 ], 'little' ) # float type

        header.numCH1Sensors = int.from_bytes( data[ 4 * 4:4 * 4 + 2 ], 'little' )
        header.numCH2Sensors = int.from_bytes( data[ 4 * 4 + 2:4 * 4 + 4 ], 'little' )
        header.numCH3Sensors = int.from_bytes( data[ 5 * 4:5 * 4 + 2 ], 'little' )
        header.numCH4Sensors = int.from_bytes( data[ 5 * 4 + 2:5 * 4 + 4 ], 'little' )

        header.startWavelength = int.from_bytes(
                data[ 20 * 4:20 * 4 + 4 ], 'little' ) / header.granularity #float type
        header.endWavelength = int.from_bytes(
                data[ 21 * 4:21 * 4 + 4 ], 'little' ) / header.granularity #float type

        header.timeStamp = int.from_bytes( data[ 9 * 4:9 * 4 + 4 ], 'little' ) + int.from_bytes(
                data[ 8 * 4:8 * 4 + 4 ], 'little' ) / 1e6 #float type

        header.bufferSize = data[ 12 * 4 ]
        header.headerSize = int.from_bytes( data[ 12 * 4 + 2:12 * 4 + 4 ], 'little' )
        header.headerVersion = data[ 12 * 4 + 1 ]
        return header
