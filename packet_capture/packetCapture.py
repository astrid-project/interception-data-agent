"""
packetCapture

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging

from captureHandler import CaptureHandler
from configurationManager import ConfigurationManager
from interceptionManager import InterceptionManager
from restServer import RestServer 

# debug logger instance
debugLevel = logging.DEBUG
logger = logging.getLogger( "mainLogger" )
logHandler = logging.StreamHandler()
logger.addHandler( logHandler )
logger.setLevel( debugLevel )

def main() :
    confBox = ConfigurationManager()

    restBox = RestServer( confBox.getPacketInterceptionAddress(), \
        confBox.getPacketInterceptionPort())

    return True

if __name__ == "__main__" :
    logger.debug( " " + __file__ + " : starting ... " )
    main()
    logger.debug( " " + __file__ + " : ... end " )
