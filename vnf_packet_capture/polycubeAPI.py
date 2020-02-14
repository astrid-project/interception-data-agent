"""
polycubeAPI

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging
import requests
import json

# debug logger instance
debugLevel = logging.DEBUG
logger = logging.getLogger( "mainLogger" )
logHandler = logging.StreamHandler()
logger.addHandler( logHandler )
logger.setLevel( debugLevel )

class PolycubeAPI() :
    def __init__( self, polycubeIPAddress = "127.0.0.1" , polycubeIPPort = 9000 ) :
        # save Polycube server IP parameters
        # Polycube server is the instance of Polycube to use to launch Polycube services (ex. PacketCapture)
        self.polycubeIPAddress = polycubeIPAddress
        self.polycubeIPPort = polycubeIPPort 
        self.polycubeVersion = "polycube/v1/"
        self.polycubeURL = "http://" + self.polycubeIPAddress + ":" + str( self.polycubeIPPort ) + \
            "/" + self.polycubeVersion + "/"
    
    def createPacketCapture( self, packetCaptureName ) :
        createPacketCaptureEndpoint = self.polycubeURL + "packetcapture/" + packetCaptureName + "/"
        payload = {}
        logger.debug( createPacketCaptureEndpoint )
        logger.debug( json.dumps( payload ) )
        response = requests.post( createPacketCaptureEndpoint, data = json.dumps( payload ) )
        if response.status_code == 201 :
            return True
        return False

    def attachPacketCapture( self, packetCaptureName, interfaceToAttach ) :
        attachPacketCaptureEndpoint = self.polycubeURL + "attach/" + "/"
        payload = {}
        payload[ "cube" ] = packetCaptureName
        payload[ "port" ] = interfaceToAttach
        logger.debug( attachPacketCaptureEndpoint )
        logger.debug( json.dumps( payload ) )
        response = requests.post( attachPacketCaptureEndpoint, data = json.dumps( payload ) )
        if response.status_code == 200 :
            return True
        return False

    def srcIPSetPacketCapture( self, packetCaptureName, ipaddress = "0.0.0.0", mask = "24" ) :
        srcIPSetPacketCaptureEndpoint = self.polycubeURL + packetCaptureName + "/filters/src"
        payload = ipaddress + "/" + mask
        logger.debug( srcIPSetPacketCaptureEndpoint )
        logger.debug( payload )
        response = requests.patch( srcIPSetPacketCaptureEndpoint, data = payload )
        if response.status_code == 200 :
            return True
        return False
    
    def dstIPSetPacketCapture( self, packetCaptureName, ipaddress = "0.0.0.0", mask = "24" ) :
        dstIPSetPacketCaptureEndpoint = self.polycubeURL + packetCaptureName + "/filters/dst"
        payload = ipaddress + "/" + mask
        logger.debug( dstIPSetPacketCaptureEndpoint )
        logger.debug( payload )
        response = requests.patch( dstIPSetPacketCaptureEndpoint, data = payload )
        if response.status_code == 200 :
            return True
        return False

    def srcPortSetPacketCapture( self, packetCaptureName, port = 0 ) :
        srcPortSetPacketCaptureEndpoint = self.polycubeURL + packetCaptureName + "/filters/sport"
        payload = port
        logger.debug( srcPortSetPacketCaptureEndpoint )
        logger.debug( payload )
        response = requests.patch( srcPortSetPacketCaptureEndpoint, data = payload )
        if response.status_code == 200 :
            return True
        return False

    def dstPortSetPacketCapture( self, packetCaptureName, port = 0 ) :
        dstPortSetPacketCaptureEndpoint = self.polycubeURL + packetCaptureName + "/filters/dport"
        payload = port
        logger.debug( dstPortSetPacketCaptureEndpoint )
        logger.debug( payload )
        response = requests.patch( dstPortSetPacketCaptureEndpoint, data = payload )
        if response.status_code == 200 :
            return True
        return False
    
    """
    parameters: "tcp" or "udp"
    """
    def l4ProtoSetPacketCapture( self, packetCaptureName, l4Proto = "" ) :
        l4ProtoSetPacketCaptureEndpoint = self.polycubeURL + packetCaptureName + "/filters/l4proto"
        payload = l4Proto
        logger.debug( l4ProtoSetPacketCaptureEndpoint )
        logger.debug( payload )
        response = requests.patch( l4ProtoSetPacketCaptureEndpoint, data = payload )
        if response.status_code == 200 :
            return True
        return False

    def delPacketCapture( self, packetCapturename ) :
        delPacketCaptureEndpoint = self.polycubeURL + packetCapturename
        logger.debug( delPacketCaptureEndpont )
        response = requests.delete( delPacketCaptureEndpoint )
        if response.status_code == 200 :
            return True
        return False




    