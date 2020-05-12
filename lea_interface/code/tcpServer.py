"""
tcpServer

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import threading
import socket
import time

from myLogger import MyLogger
from tcpTask import TcpTask


class TcpServer( threading.Thread ) :
    def __init__( self, serverAddress, serverPort ) :
        threading.Thread.__init__( self )
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( logName = __name__ )
        self.is_active = True
        self.address = serverAddress
        self.port = serverPort
        self.socket = None
        self.tcpConnections = []

        for resource in socket.getaddrinfo( self.address, self.port,
                socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE) :
            af, sockettype, proto, canonname, sa = resource
            try :
                self.logger.debug( "create socket" )
                self.socket = socket.socket( af, sockettype, proto )
            except socket.error as err :
                self.logger.error( "ERROR: create socket : %s", str( err ))
                self.socket = None
                continue
            
            try :
                self.logger.debug( "socket bind" )
                self.socket.bind( sa )
            except socket.error as err :
                self.logger.error( "ERROR: socket bind : %s", str( err ) )
                self.socket.close()
                self.socket = None
                continue
            
            break

        if self.socket == None :
            self.logger.error( "ERROR: socket is NONE" )
            raise Exception( "ERROR: impossible to create socket listen to %s:%s", \
                self.address, self.port )


    def run( self ) :
        if self.socket == None :
            self.logger.error( "ERROR: socket is NONE (2)" )
            raise Exception( "ERROR: impossible to create socket listen to %s:%s (2)", \
                self.address, self.port )
        try :
            self.logger.debug( "socket listen" )
            self.socket.listen( 5 ) # five elem in queue (backlog)
        except Exception as exception :
            self.logger.error( "ERROR: error in listen : %s", str( exception ) )
        
        while self.is_active :
            try :
                conn, addr = self.socket.accept()
                self.logger.debug( "connection received - %s, %s", \
                    str( conn ), str( addr ) )
            except socket.error as err :
                self.logger.error( "Error: socket listen/accept : %s", str( err ) )
                time.sleep( 1 )

            self.logger.debug( "create ONE \"TcpTask\"" )
            tcpThread = TcpTask( conn, addr )
            self.tcpConnections.append( tcpThread )
            tcpThread.start()

    def stop( self ) :
        self.is_alive = False
        for elem in self.tcpConnections :
            elem.stop()



