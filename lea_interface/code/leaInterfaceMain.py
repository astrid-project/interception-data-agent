"""
leaInterfaceMain

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from myLogger import MyLogger
from configurationManager import ConfigurationManager
from kafkaClient import KafkaClient
from tcpServer import TcpServer

def main() :
    # main function
    kafkaClient = None
    tcpServer = None

    try :
        if confBox.getKafkaServerAddress() != "" and confBox.getKafkaServerPort() != 0 :
            kafkaClient = KafkaClient( confBox.getKafkaServerAddress(),
                confBox.getKafkaServerPort(), confBox.getKafkaServerTopic() )
            kafkaClient.start()
        if confBox.getTcpServerAddress() != "" and confBox.getTcpServerPort() != 0 :
            tcpServer = TcpServer( confBox.getTcpServerAddress(), \
                confBox.getTcpServerPort() )
            tcpServer.start()
    except Exception as e :
        logger.error( e )
        if kafkaClient != None :
            kafkaClient.stop()
        if tcpServer != None :
            tcpServer.stop()

    if kafkaClient != None :
        kafkaClient.join()
    if tcpServer != None :
        tcpServer.join()



if __name__ == "__main__" :
    confBox = ConfigurationManager()
    myLogger = MyLogger()
    logger = myLogger.getLogger( logName = __name__ )

    logger.debug( "starting ... " )
    main()
    logger.debug( "... end " )
