"""
netParameterFetcher

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging

# debug logger instance
debugLevel = logging.DEBUG
logger = logging.getLogger( "mainLogger" )
logHandler = logging.StreamHandler()
logger.addHandler( logHandler )
logger.setLevel( debugLevel )

class NetParameterFetcher() :
    def __init__ () :
        logger.debug( "NetParamterFetcher object initialization" )
    
    def dataFetcher( userID, serviceProviderID, serviceID ) :
        """
        returns
        src IP address
        src PORT address
        dst IP address
        dst PORT address
        l4proto
        """
        srcIPAddress = "0.0.0.0/24"
        srcIPPort = 0
        dstIPAddress = "0.0.0.0/24"
        dstIPPort = 0
        l4Proto = 0
        
        # TODO

        return srcIPAddress, srcIPPort, dstIPAddress, dstIPPort, l4Proto