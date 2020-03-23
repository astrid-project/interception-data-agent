"""
interceptionMain

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from myLogger import MyLogger
from configurationManager import ConfigurationManager
from restServer import RestServer

def main() :
    # main function

    try :
        restServer = RestServer( confBox.getRestServerAddress(), confBox.getRestServerPort(),
            confBox.getPolycubeServerAddress(), confBox.getPolycubeServerPort(), 
            confBox.getInterceptionInterfaceName(), confBox.getLogVoIPServerPath(), 
            confBox.getLogVoIPServerFilename(), confBox.getVoIPLogReadingTimeOut(),
            confBox.getInterceptionTool(), confBox.getSavedInterceptionPath() )
        restServer.run()
    except Exception as e :
        logger.error( e )


if __name__ == "__main__" :
    confBox = ConfigurationManager()
    myLogger = MyLogger()
    logger = myLogger.getLogger( logName = __name__ )

    logger.debug( "starting ... " )
    main()
    logger.debug( "... end " )
