"""
polycubeHandler

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging
import os

from polycubeAPI import PolycubeAPI

# debug logger instance
debugLevel = logging.DEBUG
logger = logging.getLogger( __name__ )
logHandler = logging.StreamHandler()
logger.addHandler( logHandler )
logger.setLevel( debugLevel )

class PolycubeHandler() :
    def __init__( self, polycubeServerAddress = "127.0.0.1", polycubeServerPort = 9000,
                    savedInterceptionPath = "./", savedInterceptionFileName = "capture_file" ) :
        self.packetCaptureList = {}
        self.polycubeAPI = PolycubeAPI()
        self.savedInterceptionPath = savedInterceptionPath
        self.savedInterceptionFileName = savedInterceptionFileName

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
        self.polycubeAPI.dumpPathSetPacketCapture( packetCaptureName, self.savedInterceptionPath, 
                self.savedInterceptionFileName )
        self.polycubeAPI.attachPacketCapture( packetCaptureName, interfaceToAttachName )
        polycubeFilter = ""
        if srcAddress :
            polycubeFilter = "( ip src " + str( srcAddress )
            # DON'T FILTER TRAFFIC FOR PORT
            #if srcPort :
            #    polycubeFilter += " && src port " + str( srcPort )
            polycubeFilter += " ) "
        if dstAddress :
            if polycubeFilter != "" :
                polycubeFilter += " || "
            polycubeFilter += "( ip dst " + str( dstAddress )
            # DON'T FILTER TRAFFIC FOR PORT
            #if dstPort :
            #    polycubeFilter += " && " + str( dstPort )
            polycubeFilter += " ) "
        if polycubeFilter != "" :
            self.polycubeAPI.filterSetPacketCapture( packetCaptureName, polycubeFilter )

        self.packetCaptureList[ packetCaptureName ] = ( srcAddress, srcPort, dstAddress, dstPort, l4Proto )
        return True


    def interceptionStop( self, userID, providerID, serviceID ) :
        logger.debug( "interceptionStop" )
        packetCaptureName = str( serviceID ) + "." + str( providerID ) + "." + str( userID )
        if self.packetCaptureList.pop( packetCaptureName, False ) :
            self.polycubeAPI.delPacketCapture( packetCaptureName )
            return True

        return False

    # TODO : set fileName in Polycube Packet Capture
    def interceptionSetFileName( self, fileName ) :
        if fileName != "" :
            # Remove ".pcap" extension
            self.savedInterceptionFileName = os.path.splitext( fileName )[0]
            return True
        return False
    
    def interceptionGetFileName( self ) :
        return self.savedInterceptionFileName

