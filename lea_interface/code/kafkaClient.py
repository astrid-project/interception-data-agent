"""
kafkaClient

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import threading

from json import dumps
from kafka import KafkaConsumer
from myLogger import MyLogger
from fileFeed import FileFeed

class KafkaClient( threading.Thread ) :
    def __init__( self, kafkaAddress = "localhost", kafkaPort = "9092", kafkaTopic = "kafka" ) :
        threading.Thread.__init__( self )
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )

        self.fileWriter = dict()
        self.kafkaAddress = kafkaAddress
        self.kafkaPort = kafkaPort
        self.kafkaTopic = kafkaTopic

        # parameter for life cycle
        self.live = True 

        bootstrap_servers = [ str( self.kafkaAddress ) + ":" + str( self.kafkaPort ) ]
        self.logger.debug( "kafka bootstrap server : %s", str( bootstrap_servers ) )

        # parameter to use at python restart
        auto_offset_reset = "earliest"
        # commit the read of message to kafka broker
        enable_auto_commit = True
        auto_commit_interval_ms = 1000
        group_id = "interception"
        value_deserializer = lambda x: json.loads( x.decode( 'utf-8' ) )

        self.consumer = KafkaConsumer( self.kafkaTopic, bootstrap_servers = bootstrap_servers, auto_offset_reset = auto_offset_reset, enable_auto_commit = enable_auto_commit, group_id = group_id, value_deserializer = value_deserializer )

    def run( self ) :
        self.logger.debug( "kafka client receiver start" )
        while self.live :
            for data in self.consumer :
                message = data.value
                userID = message.get( "user_id", "" )
                data = message.get( "data", "" )
                writer = self.fileWriter.get( userID, "" )
                if writer == "" :
                    writer = FileFeed( fileName = str( userID ) + ".pcap" )
                    self.fileWriter[ userID ] = writer
                writer.writeStr( data )

    def stop( self ) :
        self.live = False
