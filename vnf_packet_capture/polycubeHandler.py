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

    def interceptionStart( self, userID, providerID, serviceID, srcAddress, srcPort, dstAddress,
        dstPort, l4Proto = None, interfaceToAttachName = None ) :
        logger.debug( "interceptionStart" )
        packetCaptureName = str( serviceID ) + "." + str( providerID ) + "." + str( userID )
        logger.debug( "userID : %s, providerID : %s, serviceID : %s",
            str( userID ), str( providerID ), str( serviceID ) )
        logger.debug( "srcAddress : %s, srcPort : %s, dstAddress : %s",
            str( srcAddress ), str( srcPort ), str( dstAddress ) )
        logger.debug( "dstPort : %s, l4Proto : %s, interfaceToAttachName : %s", 
            str( dstPort ), str( l4Proto ), str( interfaceToAttachName ) )

        elem = self.packetCaptureList.get( packetCaptureName, False )
        if elem : 
            if elem == ( srcAddress, srcPort, dstAddress, dstPort, l4Proto ) :
                logger.debug( "packetcapture already running for this request")
                return True
            else :
                self.interceptionStop( userID, providerID, serviceID, srcAddress, srcPort,
                    dstAddress, dstPort, l4Proto )

        self.polycubeAPI.createPacketCapture( packetCaptureName )
        self.polycubeAPI.attachPacketCapture( packetCaptureName, interfaceToAttachName )
        if srcAddress :
            self.polycubeAPI.srcIPSetPacketCapture( packetCaptureName, srcAddress )

        self.packetCaptureList[ packetCaptureName ] = ( srcAddress, srcPort, dstAddress, dstPort, l4Proto )
        return True


    def interceptionStop( self, userID, providerID, serviceID ) :
        logger.debug( "interceptionStop" )
        packetCaptureName = str( serviceID ) + "." + str( providerID ) + "." + str( userID )
        if self.packetCaptureList.pop( packetCaptureName, False ) :
            self.polycubeAPI.delPacketCapture( packetCaptureName )
            return True

        return False
    


