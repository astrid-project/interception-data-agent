"""
interceptionTask

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import threading
import time

from enum import Enum
from parsingHandler import ParsingHandler
from polycubeHandler import PolycubeHandler
from tcpdumpHandler import TcpdumpHandler
from myLogger import MyLogger
from configurationManager import InterceptionTool

class InterceptionTask( threading.Thread ):
    def __init__( self, userID, providerID, serviceID,
    polycubeServerAddress, polycubeServerPort, interceptionInterfaceName, 
    logVoIPFilePath = "./", logVoIPFileName = "file.log", readVoIPLogTimeout = 0.5,
    interceptionTool = InterceptionTool.PolycubePacketCapture ):
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
        if interceptionTool == InterceptionTool.PolycubePacketCapture :
            self.interceptionHandler = PolycubeHandler(polycubeServerAddress, polycubeServerPort)
        elif interceptionTool == InterceptionTool.Tcpdump :
            self.interceptionHandler = TcpdumpHandler()
        else :
            self.interceptionHandler = None

    def run( self ):
        while self.is_active :
            # - read log from VoIP logfile
            if self.parsingHandler.readFileAndGetEvent() :
                # for every type of event, read all event and do something
                while True :
                    event = self.parsingHandler.changeInterceptedIPParameters()
                    if event != {} :
                        # parse event and get the data (srcAddress, etc)
                        self.logger.debug( "catched event \"changeInterceptedIPParameter\" : " )
                        self.logger.debug( "userID: %s / providerID : %s / serviceID : %s", 
                            str( event.get( "userID", "" ) ), str( event.get( "providerID", "" ) ), 
                            str( event.get( "serviceID", "") ) )
                        self.logger.debug( "srcAddress : %s / srcPort : %s ",
                            str( event.get( "srcAddress", "" ) ), str( event.get( "srcPort", "" ) ) )
                        self.logger.debug( "dstAddress : %s / dstPort : %s",
                            str( event.get( "dstAddress", "" ) ), str( event.get( "dstPort", "" ) ) )

                        srcAddress = event.get( "srcAddress", "0.0.0.0" )
                        srcPort = event.get( "srcPort", "0" )
                        dstAddress = event.get( "dstAddress", "0.0.0.0" )
                        dstPort = event.get( "dstPort", "0" )
                        l4Proto = ""
                        
                        # - start/stop Polycube packetcapture, get from VoIP log parameters
                        self.logger.debug( "create packet capture" )
                        boolResult = False
                        
                        if self.interceptionHandler :
                            boolResult = self.interceptionHandler.interceptionStart( 
                                self.userID, self.providerID, self.serviceID,
                                srcAddress, srcPort, dstAddress, dstPort, l4Proto, 
                                self.interceptionInterfaceName )
                        else :
                            self.logger.error( "interception tool UNDEFINED or UNKNOWN (1)" )

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
                self.logger.warn( "sleep for: %s", str( self.readVoIPLogTimeout ) )
                time.sleep( self.readVoIPLogTimeout )

        # When main thread is stopped, the Polycube Packetcapture is removed
        boolResult = False
        
        if self.interceptionHandler :
            boolResult = self.interceptionHandler.interceptionStop( self.userID, self.providerID, self.serviceID )
        else :
            self.logger.error( "interception tool UNDEFINED or UNKNOWN (2)" )
        
        self.logger.debug( "result of Polycube Packetcapture stop : %s", str( boolResult ) )

    def stop( self ):
        self.is_active = False




