"""
interceptionTask

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import threading
import time

from parsingHandler import ParsingHandler
from polycubeHandler import PolycubeHandler
from myLogger import MyLogger

class InterceptionTask( threading.Thread ):
    def __init__( self, userID, providerID, serviceID,
    polycubeServerAddress, polycubeServerPort, interceptionInterfaceName, 
    logVoIPFilePath = "./", logVoIPFileName = "file.log", readVoIPLogTimeout = 0.5 ):
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )
        threading.Thread.__init__( self )
        self.is_active = True
        self.interceptionInterfaceName = interceptionInterfaceName
        self.logVoIPFilePath = logVoIPFilePath
        self.logVoIPFileName = logVoIPFileName
        self.userID = userID
        self.providerID = providerID
        self.serviceID = serviceID
        self.readVoIPLogTimeout = readVoIPLogTimeout
        self.parsingHandler = ParsingHandler( userID = self.userID, 
         providerID = self.providerID, serviceID = self.serviceID,
         filePath = self.logVoIPFilePath, fileName = self.logVoIPFileName )
        self.polycubeHandler = PolycubeHandler(polycubeServerAddress, polycubeServerPort)

    def run( self ):
        while self.is_active :
            # - read log from VoIP logfile
            if self.parsingHandler.readFileAndGetEvent() :
                # for every type of event, read all event and do something
                while True :
                    event = self.parsingHandler.changeInterceptedIPParameters()
                    if event != {} :
                        # parse event and get the data (srcAddress, etc)
                        print( "TODO" )
                        srcAddress = "0.0.0.0"
                        srcPort = 0
                        dstAddress = "0.0.0.0"
                        dstPort = 0
                        l4Proto = ""
                        
                        # - start/stop Polycube packetcapture, get from VoIP log parameters
                        self.logger.debug( "create packet capture" )
                        boolResult = False
                        """
                        boolResult = self.polycubeHandler.interceptionStart( 
                            self.userID, self.serviceProviderID, self.serviceID,
                            srcAddress, srcPort, dstAddress, dstPort, l4Proto, 
                            self.interceptionInterfaceName )
                        """
                        self.logger.debug( "result of Polycube Packetcapture start: %s", str( boolResult ) )
                    else :
                        break
                
                while True :
                    # event = self.GET_OTHER_EVENT()
                    print( "TODO" )
                    break

                    # - send log throught Logstash (missing call, retrieved call, etc)
           
            else :
                # if not event, wait for a time
                self.logger.debug( "sleep for: %s", str( self.readVoIPLogTimeout ) )
                time.sleep( self.readVoIPLogTimeout )

        # When main thread is stopped, the Polycube Packetcapture is removed
        boolResult = False
        """
        boolResult = self.polycubeHandler.interceptionStop( self.userID, self.providerID, self.serviceID )
        """
        self.logger.debug( "result of Polycube Packetcapture stop : %s", str( boolResult ) )

    def stop( self ):
        self.is_active = False




