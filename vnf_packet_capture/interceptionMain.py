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
#logger = logging.getLogger( __name__ )
logger = logging.getLogger( "mainLogger" )
logHandler = logging.StreamHandler()
logFormat = logging.Formatter( "%(name)s - %(levelname)s - %(message)s" )
logHandler.setFormatter( logFormat )
logger.addHandler( logHandler )
logger.setLevel( debugLevel )

def main() :
    # main function
    confBox = ConfigurationManager()
    restServer = RestServer( confBox.getRestServerAddress(), confBox.getRestServerPort() )
    restServer.run()


if __name__ == "__main__" :
    logger.debug( "starting ... " )
    main()
    logger.debug( "... end " )
