"""
interceptionMain

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from myLogger import MyLogger
from configurationManager import ConfigurationManager
from restServer import RestServer
from kafkaClient import KafkaClient

def main() :
    # main function

    if confBox.getRestServerAddress() != "" and confBox.getRestServerPort() != 0 :
        restServer = RestServer( confBox.getRestServerAddress(), confBox.getRestServerPort(),
            confBox.getPolycubeServerAddress(), confBox.getPolycubeServerPort(), 
            confBox.getInterceptionInterfaceName(), confBox.getLogVoIPServerPath(), 
            confBox.getLogVoIPServerFilename(), confBox.getVoIPLogReadingTimeOut(),
            confBox.getInterceptionTool(), confBox.getSavedInterceptionPath(),
            confBox.getLogstashServerAddress(), confBox.getLogstashServerMsgPort(),
            confBox.getLogstashServerVersion(), confBox.getKafkaServerAddress(),
            confBox.getKafkaServerPort(), "interception_data",
            confBox.getLogstashServerDataPort(),
            confBox.getTcpServerAddress(), confBox.getTcpServerPort() )
        restServer.run()
    elif confBox.getKafkaServerAddress() != "0.0.0.0" and confBox.getKafkaServerAddress() != "" and \
            confBox.getKafkaServerPort != 0 :
        kafkaClient = KafkaClient( confBox.getKafkaServerAddress(), confBox.getKafkaServerPort(), 
            confBox.getKafkaServerTopic(),
            confBox.getPolycubeServerAddress(), confBox.getPolycubeServerPort(), 
            confBox.getInterceptionInterfaceName(), confBox.getLogVoIPServerPath(), 
            confBox.getLogVoIPServerFilename(), confBox.getVoIPLogReadingTimeOut(),
            confBox.getInterceptionTool(), confBox.getSavedInterceptionPath(),
            confBox.getLogstashServerAddress(), confBox.getLogstashServerMsgPort(), 
            confBox.getLogstashServerVersion(), "interception_data",
            confBox.getLogstashServerDataPort(),
            confBox.getTcpServerAddress(), confBox.getTcpServerPort() )
        kafkaClient.run()


if __name__ == "__main__" :
    confBox = ConfigurationManager()
    myLogger = MyLogger()
    logger = myLogger.getLogger( logName = __name__ )

    logger.debug( "starting ... " )
    main()
    logger.debug( "... end " )
