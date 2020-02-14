"""
interceptionMain

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging

from configurationManager import ConfigurationManager
from restServer import RestServer

# debug logger instance
debugLevel = logging.DEBUG
logger = logging.getLogger( "mainLogger" )
logHandler = logging.StreamHandler()
logger.addHandler( logHandler )
logger.setLevel( debugLevel )

def main() :
    confBox = ConfigurationManager()
    #restServer = RestServer( confBox.getRestServerAddress(), confBox.getRestServerPort() )


if __name__ == "__main__" :
    logger.debug( " " + __file__ + " : starting ... " )
    main()
    logger.debug( " " + __file__ + " : ... end " )
