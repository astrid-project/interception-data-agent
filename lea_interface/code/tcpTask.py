"""
tcpTask

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import threading
import socket
import time

from myLogger import MyLogger
from fileFeed import FileFeed

class TcpTask( threading.Thread ) :
    id = 0
    def __init__( self, connection, address, dataBuffer = 2048, path = "/tmp/" ) :
        threading.Thread.__init__( self )
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( logName = __name__ + str( TcpTask.id ) )
        TcpTask.id += 1
        self.is_active = True
        self.connection = connection
        self.address = address
        self.dataBuffer = dataBuffer
        self.path = path
    
    def run( self ) :
        fileName = ""
        completePath = ""
        feeder = None
        while self.is_active :
            try :
                data = self.connection.recv( self.dataBuffer )
                if not fileName :
                    # first received data is the name (string) of the file to write
                    fileName = str( data.decode() ).rstrip()
                    self.logger.debug( "name of file to write : %s", str( fileName ) )
                    feeder = FileFeed( self.path, fileName )
                else :
                    # rest of tcp stream is pcap file data
                    # write data of file
                    feeder.writeByte( data )

                if not data :
                    break
            except Exception as exception :
                self.logger.error( "ERROR: %s", str( exception ) )

        if feeder :
            feeder.close()
            self.logger.debug( "file %s close", completePath )
        self.connection.close()
        self.logger.debug( "connection close" )

    def stop( self ) :
        self.is_active = False
