"""
interceptionSender

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import threading
import logging
import logstash
import base64
import socket

from time import sleep
from enum import Enum
from json import dumps
from kafka import KafkaProducer
from myLogger import MyLogger

class SenderTool( Enum ) :
    kafka = 0
    logstash = 1
    tcpstream = 2

"""
InterceptionSender()
::
Read interception data file (usually pcap) and sends it to LEA interface
through Kafka broker
::
from configuration file read:
- interception file path - interception file name - kafka server address
- kafka server port - kafka topic
"""
class InterceptionSender( threading.Thread ) :
    def __init__( self, userID, interceptionFilePath = "./", interceptionFileName = "interception.pcap" , senderTool : SenderTool = SenderTool.logstash, 
                  kafkaServerAddress = "localhost", kafkaServerPort = 9092, 
                  kafkaTopic = "interception_data", 
                  logstashAddress = "localhost", logstashPort = 5960, logstashMessageVersion = 1, 
                  sizeByteToRead = 100,
                  tcpServerAddress = "", tcpServerPort = 0 ) :
        threading.Thread.__init__( self )
        self.userID = userID
        self.interceptionFilePath = interceptionFilePath
        self.interceptionFileName = interceptionFileName
        self.senderTool = senderTool
        self.kafkaServerAddress = kafkaServerAddress
        self.kafkaServerPort = kafkaServerPort
        self.kafkaTopic = kafkaTopic
        self.logstashAddress = logstashAddress
        self.logstashPort = logstashPort
        self.logstashMessageVersion = logstashMessageVersion
        self.sizeByteToRead = sizeByteToRead
        self.tcpServerAddress = tcpServerAddress
        self.tcpServerPort = tcpServerPort
        self.tcpFirstMessage = None
        self.tcpSocket = None
        localLogger = MyLogger()
        self.logger = localLogger.getLogger( __name__ )
        self.logger.debug( "tcpServerAddress: %s / tcpServerPort: %s",
            str( self.tcpServerAddress ), str( self.tcpServerPort ) )
        self.is_active = True
        if self.senderTool == SenderTool.kafka :
            bootstrap_servers = [ str( self.kafkaServerAddress ) + ":" + str( self.kafkaServerPort ) ]
            self.logger.debug( "kafka bootstrap server: %s", str( bootstrap_servers ) )
            value_serializer = lambda x: dumps(x).encode( 'utf-8' )
            self.producer = KafkaProducer( bootstrap_servers = bootstrap_servers, value_serializer = value_serializer )
            self.__sender = self.__kafkaSender
        elif self.senderTool == SenderTool.logstash :
            self.logger.debug( "Logstash server : %s : %s",
                str( self.logstashAddress ), str( self.logstashPort ) )
            self.sendToLogstash = logging.getLogger( "interception" )
            self.sendToLogstash.setLevel( logging.INFO )
            self.sendToLogstash.addHandler(
                    logstash.TCPLogstashHandler(
                        host = self.logstashAddress,
                        port = self.logstashPort,
                        version = self.logstashMessageVersion
                    )
                )
            self.__sender = self.__logstashSender
        elif self.senderTool == SenderTool.tcpstream :
            self.logger.debug( "Tcp stream sender : tcp server : %s:%s", \
                str( self.tcpServerAddress ), str( self.tcpServerPort ) )
            self.tcpFirstMessage = True
            self.__sender = self.__tcpSender
            for res in socket.getaddrinfo( self.tcpServerAddress, 
                    self.tcpServerPort, socket.AF_UNSPEC, socket.SOCK_STREAM ) :
                af, socktype, proto, canonname, sa = res
                try :
                    self.tcpSocket = socket.socket( af, socktype, proto )
                except socket.error as exception :
                    self.logger.debug( "Error: create socket, retry : %s", str( exception ) )
                    self.tcpSocket = None
                    continue
                try :
                    self.tcpSocket.connect( sa )
                except socket.error as exception :
                    self.logger.debug( "Error: connect, retry : %s", str( exception ) )
                    self.tcpSocket.close()
                    self.tcpSocket = None
                    continue
                break
            if self.tcpSocket is None :
                self.logger.error( "ERROR: impossible to connect to %s:%s", \
                    str( self.tcpServerAddress ), str( self.tcpServerPort ) )

        else :
            self.__sender = self.__undefinedSender

    def sender( self, message, bytesToSend ) :
        self.__sender( message, bytesToSend )

    def __logstashSender( self, message, bytesToSend ) :
        self.sendToLogstash.info( message[ "data" ], extra = message )

    def __kafkaSender( self, message, bytesToSend ) :
        # message is a dictionary, lambda function transforms it in a Json payload
        self.producer.send( self.topic, message )
        # wait until all messages sent
        self.producer.flush()

    def __tcpSender( self, message, bytesToSend ) :
        if self.tcpSocket :
            if self.tcpFirstMessage :
                # send only name of file to write
                self.tcpFirstMessage = False
                self.tcpSocket.send( message[ "interceptionfilename" ].encode() )
                sleep( 1 )
            # send bytestream
            self.tcpSocket.send( bytesToSend )
        else :
            self.logger.error( "ERROR: socket is empty" )

    def __undefinedSender( self, message, bytesToSend ) :
        self.logger( "ERROR : sender tool not defined ")
    
    def run( self ) :
        self.logger.debug( "thread start")
        message = dict()
        message[ "userid" ] = self.userID
        message[ "data" ] = b'' # field for interception data
        message[ "interceptionfilename" ] = self.interceptionFileName
        interceptionCompletePath = str( self.interceptionFilePath ) \
            + "/" + str( self.interceptionFileName )

        # TODO : try to read the file 150 times before rise an error
        # 150 times for 2 seconds of sleep => 5 minutes of attempts
        isFileOpened = False
        openFileOperationCycle = 0
        while isFileOpened == False :
            try :
                file = open( interceptionCompletePath, "rb" )
                isFileOpened = True
                self.logger.debug( "File %s opened", str( interceptionCompletePath ) )
            except Exception as e :
                if openFileOperationCycle == 150 :
                    self.logger.error( "Impossible to open %s", str( interceptionCompletePath ) )
                    return
                openFileOperationCycle += 1
                if openFileOperationCycle % 10 :
                    self.logger.debug( "Impossible to open %s, retry in 1 sec", str( interceptionCompletePath ) )
                sleep( 2 )

        while self.is_active :
            # Continuously read interception file and send it to kafka broker or logstash
            bytes = file.read( self.sizeByteToRead )

            # if file is empty, wait until it will be filled up
            if bytes == b'' :
                sleep( 2 )
            else :
                message[ "data" ] = str( base64.b64encode( bytes ), 'utf-8' )
                self.sender( message, bytes )

    def stop( self ) :
        self.logger.debug( "stop task")
        self.is_active = False
        if self.tcpSocket :
            self.logger.debug( "close socket : %s", str( self.tcpSocket ) )
            self.tcpSocket.close()
            

