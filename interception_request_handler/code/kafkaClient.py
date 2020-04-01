"""
kafkaClient

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from json import dumps
from kafka import KafkaProducer
from myLogger import MyLogger

class KafkaClient() :
    def __init__( self, address = "localhost", port = "9092", topic = "kafka" ) :
        self.address = address
        self.port = port
        self.topic = topic
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )

        bootstrap_servers = [ str( self.address ) + ":" + str( self.port ) ]
        self.logger.debug( "kafka bootstrap server: %s", str( bootstrap_servers ) )
        value_serializer = lambda x: dumps(x).encode( 'utf-8' )

        self.producer = KafkaProducer( bootstrap_servers = bootstrap_servers, value_serializer = value_serializer )

    """
    send
    ::
    it sends message to Kafka broker, it waits until message is sent
    ::
    "message" is a dictionary, function transforms it in a Json payload
    """
    def send( self, message ) :
        # asynchronous send
        self.producer.send( self.topic, message )
        self.logger.debug( "send a message to kafka broker" )

        # wait until all messages sent
        self.producer.flush()
        self.logger.debug( "message sent to kafka broker" )

