"""
polycubeHandler

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging

from polycubeAPI import PolycubeAPI

# debug logger instance
debugLevel = logging.DEBUG
logger = logging.getLogger( __name__ )
logHandler = logging.StreamHandler()
logger.addHandler( logHandler )
logger.setLevel( debugLevel )

class PolycubeHandler() :
    def __init__( self, polycubeServerAddress = "127.0.0.1", polycubeServerPort = 9000 ) :
        self.packetCaptureList = {}
        self.polycubeAPI = PolycubeAPI()

    def interceptionStart( self, userID, providerID, serviceID, srcAddress, srcPort, dstAddress, dstPort, l4Proto, interfaceToAttachName ) :
        logger.debug( "interceptionStart" )
        packetCaptureName = str( serviceID ) + "." + str( providerID ) + "." + str( userID )
        self.polycubeAPI.createPacketCapture( packetCaptureName )
        self.polycubeAPI.attachPacketCapture( packetCaptureName, interfaceToAttachName )
        self.packetCaptureList[ packetCaptureName ] = True
        return True


    def interceptionStop( self, userID, providerID, serviceID, srcAddress, srcPort, dstAddress, dstPort, l4Proto ) :
        logger.debug( "interceptionStop" )
        packetCaptureName = str( serviceID ) + "." + str( providerID ) + "." + str( userID )
        if self.packetCaptureList.get( packetCaptureName, False ) :
            self.polycubeAPI.delPacketCapture( packetCaptureName )
            return True

        return False
    


