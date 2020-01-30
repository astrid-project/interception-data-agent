"""
interceptionManager

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging

from captureHandler import CaptureHandler 

logger = logging.getLogger( "mainLogger" )

class InterceptionManager() :
    def __init__():
        self.packetCaptureList = {}
        return None

    def createPacketCapture( userID, serviceProviderID, serviceID,
    srcIP, srcPort, dstIP, dstPort ) :

        packetCaptureThread = CaptureHandler( srcIP, srcPort, dstIP, dstPort )

        return True

    def removePacketCapture() :
        return True