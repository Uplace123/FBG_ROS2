import socket

from typing import List, Union
from dataclasses import dataclass, field
import numpy as np


@dataclass
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

@dataclass
class PeakContainer:
    CH1: List[ float ] = field( default_factory=list )
    CH2: List[ float ] = field( default_factory=list )
    CH3: List[ float ] = field( default_factory=list )
    CH4: List[ float ] = field( default_factory=list )

    @property
    def peaks( self ):
        return [ self.CH1, self.CH2, self.CH3, self.CH4 ]


@dataclass
class PeakMessage:
    header:StatusHeader = field( default_factory=StatusHeader)
    peak_container:PeakContainer = field(default_factory=PeakContainer)





class Interrogator():
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
        except socket.timeout:
            self.is_ready = False

    def getData(self):
        """ return PeakMessage object, None if not connected"""
        if not self.is_ready:
            print("Fail to connect with Interrogator!")
            return None
        data = self.sendCommand( "#GET_UNBUFFERED_DATA")
        peak_msg = PeakMessage()
        peak_msg.header = self.parseHeader(data)

        offset = peak_msg.header.HEADER_SIZE

        # sm130 has 4 channel
        for ch in range(4):
            if ch == 0:
                num_peaks = peak_msg.header.numCH1Sensors
            elif ch == 1:
                num_peaks = peak_msg.header.numCH2Sensors
            elif ch == 2:
                num_peaks = peak_msg.header.numCH3Sensors
            elif ch == 3:
                num_peaks = peak_msg.header.numCH4Sensors
            else:
                continue

            for _ in range(num_peaks):
                peak_val = int.from_bytes(data[offset:offset + 4],'little' ) / peak_msg.header.granularity
                offset += 4
                peak_msg.peak_container.peaks[ch].append(peak_val)

        return peak_msg

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
