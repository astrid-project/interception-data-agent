"""
captureHandler

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from threading import Thread
import logging
import time

logger = logging.getLogger( "mainLogger" )

class CaptureHandler( Thread ):
    def __init__( self, userID, srcIP, srcPort, dstIP, dstPort ) :
        self.runningStatus = False
        self.userID = userID
        self.srcIP = srcIP
        self.srcPort = srcPort
        self.dstIP = dstIP
        self.dstPort = dstPort
        return None

    def run( self ) :
        self.runningStatus = True
        while self.runningStatus == True :
            logger.debug( " one cycle ... " )
            time.sleep( 1 )

    def stop( self ) :
        self.runningStatus = False



