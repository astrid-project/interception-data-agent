"""
interceptionTask

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import threading
import time

from datetime import datetime
from parsingHandler import ParsingHandler
from polycubeHandler import PolycubeHandler
from tcpdumpHandler import TcpdumpHandler
from myLogger import MyLogger
from configurationManager import InterceptionTool
from logstashClient import LogstashClient, LogstashEvent, LogstashEventAction
from interceptionSender import InterceptionSender, SenderTool

class InterceptionTask( threading.Thread ):
    def __init__( self, userID, providerID, serviceID,
    polycubeServerAddress, polycubeServerPort, interceptionInterfaceName, 
    logVoIPFilePath = "./", logVoIPFileName = "file.log", readVoIPLogTimeout = 0.5,
    interceptionTool = InterceptionTool.PolycubePacketCapture,
    savedInterceptionPath = "./", 
    logstashAddress = "127.0.0.1", logstashMsgPort = 5959, logstashVersion = 1,
    kafkaAddress = "127.0.0.1", kafkaPort = 5002, kafkaTopic = "interception_data",
    logstashDataPort = 5960,
    tcpServerAddress = "", tcpServerPort = 0 ):
        threading.Thread.__init__( self )
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )
        threading.Thread.__init__( self )
        self.is_active = True
        self.interceptionInterfaceName = interceptionInterfaceName
        self.logVoIPFilePath = logVoIPFilePath
        self.logVoIPFileName = logVoIPFileName
        self.userID = userID
        self.providerID = providerID
        self.serviceID = serviceID
        self.readVoIPLogTimeout = readVoIPLogTimeout
        self.parsingHandler = ParsingHandler( userID = self.userID, 
         providerID = self.providerID, serviceID = self.serviceID,
         filePath = self.logVoIPFilePath, fileName = self.logVoIPFileName )
        self.savedInterceptionPah = savedInterceptionPath
        if interceptionTool == InterceptionTool.PolycubePacketCapture :
            self.logger.debug( "Polycube PacketCapture activation" )
            self.interceptionHandler = PolycubeHandler( 
                polycubeServerAddress, polycubeServerPort, savedInterceptionPath )
        elif interceptionTool == InterceptionTool.Tcpdump :
            self.logger.debug( "Tcpdump activation" )
            self.interceptionHandler = TcpdumpHandler( savedInterceptionPath, "capture.pcap" )
        else :
            self.logger.error( "no interception tool chosen !!!" )
            self.interceptionHandler = None
        self.interceptedUserIP = ""
        self.logstashAddress = logstashAddress
        self.logstashMsgPort = logstashMsgPort
        self.logstashVersion = logstashVersion
        self.kafkaAddress = kafkaAddress
        self.kafkaPort = kafkaPort
        self.kafkaTopic = kafkaTopic
        self.logstashDataPort = logstashDataPort
        self.tcpServerAddress = tcpServerAddress
        self.tcpServerPort = tcpServerPort
        self.logger.debug( "tcpServerAddress: %s / tcpServerPort: %s",
            str( self.tcpServerAddress ), str( self.tcpServerPort ) )
        self.logstashClient = LogstashClient( 
                                self.logstashAddress, 
                                self.logstashMsgPort,
                                self.logstashVersion )

        # list of sender : read pcap file and send it to LEA
        self.interceptionSenders = dict()

    def run( self ):
        while self.is_active :
            # - read log from VoIP logfile
            if self.parsingHandler.readFileAndGetEvent() :
                # for every type of event, read all event and do something
                while True :
                    event = self.parsingHandler.changeInterceptedIPParameters()
                    if event != {} :
                        # parse event and get the data (srcAddress, etc)
                        self.logger.debug( "catched event \"changeInterceptedIPParameter\" : " )
                        self.logger.debug( "userID: %s / providerID : %s / serviceID : %s", 
                            str( self.userID ), str( self.providerID ), 
                            str( self.serviceID ) )
                        self.logger.debug( "srcAddress : %s ", str( event.get( "srcAddress", "" ) ) )
                        
                        # save src address
                        self.interceptedUserIP = event.get( "srcAddress", "" )
                        
                        # Send message to Logstash
                        logstashEvent = LogstashEvent( self.userID, 
                                                       self.providerID, 
                                                       self.serviceID,
                                                       LogstashEventAction.userRegistration
                                                        )
                        logstashEvent.set( "ip_address", self.interceptedUserIP )
                        self.logstashClient.sendMessage( logstashEvent )
                        self.logger.debug( " send message to Logstash : %s ", str( logstashEvent ) )
                    else :
                        break
                
                while True :
                    event = self.parsingHandler.incomingCallParameters()
                    if event != {} :
                        self.logger.debug( "incoming call from: %s to: %s", 
                            str( event.get( "userFrom" , "" ) ), str( event.get( "userTo", "" ) ) )
                        userFrom = event.get( "userFrom", "" )
                        userTo = event.get( "userTo", "" )

                        # Send message to LogStash
                        logstashEvent = LogstashEvent( self.userID, 
                                                       self.providerID, 
                                                       self.serviceID,
                                                       LogstashEventAction.incomingCall
                                                        )
                        logstashEvent.set( "from_user", userFrom )
                        logstashEvent.set( "to_user", userTo )
                        self.logstashClient.sendMessage( logstashEvent )
                        self.logger.debug( " send message to Logstash : %s ", str( logstashEvent ) )
                    else :
                        break
                
                while True :
                    event = self.parsingHandler.startCallParameters()
                    if event != {} :
                        userFrom = event.get( "userFrom", "" )
                        userTo = event.get( "userTo", "" )
                        
                        self.logger.debug( "start call from: %s to: %s", 
                            str( event.get( "userFrom" , "" ) ), str( event.get( "userTo", "" ) ) )

                        interceptedUser = ""
                        if userFrom == self.userID :
                            interceptedUser = userFrom
                        if userTo == self.userID :
                            interceptedUser = userTo
                        if interceptedUser == "" :
                            self.logger.debug( " this starting call is not to be intercepted " )
                            break
                        
                        srcAddress = self.interceptedUserIP
                        srcPort = "5060"

                        # copy src in dst so capture traffic in bidirectional mode (to and from intercepted IP)
                        dstAddress = srcAddress
                        dstPort = srcPort
                        l4Proto = ""

                        # - start/stop Polycube packetcapture/TCPDump, get from VoIP log parameters
                        self.logger.debug( "create packet capture" )
                        boolResult = False
                        
                        if self.interceptionHandler :
                            datetimestr = datetime.now().strftime("%d_%m_%Y_%H:%M:%S")
                            interceptionFileName = str( self.userID ) + "-" + \
                                str( self.providerID ) + "-" + str( self.serviceID ) + \
                                "_" + str( datetimestr ) + ".pcap"
                            self.interceptionHandler.interceptionSetFileName( interceptionFileName )

                            boolResult = self.interceptionHandler.interceptionStart( 
                                self.userID, self.providerID, self.serviceID,
                                srcAddress, srcPort, dstAddress, dstPort, l4Proto, 
                                self.interceptionInterfaceName )
                            
                            self.logger.debug( "result of interception tool start: %s", str( boolResult ) )

                            if boolResult :
                                # start task to read/send interception data file to LEA
                                taskName = str( self.serviceID ) + "." + \
                                    str( self.providerID ) + "." + str( self.userID )
                                taskFind = self.interceptionSenders.get( taskName, False )
                                if taskFind == False :
                                    # choose type of sender tool (logstash, kafka or tcpstream)
                                    senderTool = None

                                                                
                                    self.logger.debug( "tcpServerAddress: %s / tcpServerPort: %s",
                                        str( self.tcpServerAddress ), str( self.tcpServerPort ) )
                                    
                                    if self.tcpServerAddress != "" and self.tcpServerAddress != "0.0.0.0" and self.tcpServerPort != 0 :
                                        senderTool = SenderTool.tcpstream
                                    elif self.logstashAddress != "" and self.logstashAddress != "0.0.0.0" and self.logstashDataPort != 0 :
                                        senderTool = SenderTool.logstash
                                    elif self.kafkaAddress != "" and self.kafkaAddress != "0.0.0.0" and self.kafkaPort != 0 :
                                        senderTool = SenderTool.kafka
                                    else :
                                        self.logger.error( "ERROR: impossible to choose a sender tool between logstash, kafka or tcpstream: data missing" )
                                        break
                                    
                                    self.logger.debug( "sender tool : %s", str( senderTool ) )

                                    taskFind = InterceptionSender(
                                        self.userID, self.savedInterceptionPah, interceptionFileName, senderTool, self.kafkaAddress, self.kafkaPort, self.kafkaTopic,
                                        self.logstashAddress, self.logstashDataPort,
                                        tcpServerAddress = self.tcpServerAddress, tcpServerPort = self.tcpServerPort )
                                    taskFind.start()
                                    self.logger.debug( "save interception sender : %s", \
                                        str( taskName ) )
                                    self.interceptionSenders[ taskName ] = taskFind
                                else :
                                    self.logger( "Error: read/send interception file task yet exist" )

                            # Send message to LogStash
                            logstashEvent = LogstashEvent( self.userID, 
                                                       self.providerID, 
                                                       self.serviceID,
                                                       LogstashEventAction.startCall
                                                        )
                            logstashEvent.set( "from_user", userFrom )
                            logstashEvent.set( "to_user", userTo )
                            self.logstashClient.sendMessage( logstashEvent )
                            self.logger.debug( " send message to Logstash : %s ", str( logstashEvent ) )
                        else :
                            self.logger.error( "interception tool UNDEFINED or UNKNOWN (1)" )

                    else :
                        break
                    
                while True :
                    event = self.parsingHandler.stopCallParameters()
                    if event != {} :
                        self.logger.debug( "stop call from: %s to: %s", 
                            str( event.get( "userFrom" , "" ) ), str( event.get( "userTo", "" ) ) )
                        userFrom = event.get( "userFrom", "" )
                        userTo = event.get( "userTo", "" )

                        if self.interceptionHandler :
                            boolResult = self.interceptionHandler.interceptionStop( 
                                self.userID, self.providerID, self.serviceID)

                            # check if interception sender task is active and stop it
                            taskName = str( self.serviceID ) + "." + \
                                str( self.providerID ) + "." + str( self.userID )

                            senderTask = self.interceptionSenders.pop( taskName, False )
                            if senderTask :
                                senderTask.stop()
                            
                            self.logger.debug( "result of interception tool stop (1): %s", str( boolResult ) )
                        else :
                            self.logger.error( "interception tool UNDEFINED or UNKNOWN (2)" )


                        # Send message to LogStash
                        logstashEvent = LogstashEvent( self.userID, 
                                                       self.providerID, 
                                                       self.serviceID,
                                                       LogstashEventAction.stopCall
                                                        )
                        logstashEvent.set( "from_user", userFrom )
                        logstashEvent.set( "to_user", userTo )
                        self.logstashClient.sendMessage( logstashEvent )
                        self.logger.debug( " send message to Logstash : %s ", str( logstashEvent ) )
                    else :
                        break
                    
                while True :
                    event = self.parsingHandler.rejectedCallParameters()
                    if event != {} :
                        self.logger.debug( "reject call from: %s to: %s", 
                            str( event.get( "userFrom" , "" ) ), str( event.get( "userTo", "" ) ) )
                        userFrom = event.get( "userFrom", "" )
                        userTo = event.get( "userTo", "" )

                        # Send message to LogStash
                        logstashEvent = LogstashEvent( self.userID, 
                                                       self.providerID, 
                                                       self.serviceID,
                                                       LogstashEventAction.rejectedCall
                                                        )
                        logstashEvent.set( "from_user", userFrom )
                        logstashEvent.set( "to_user", userTo )
                        self.logstashClient.sendMessage( logstashEvent )
                        self.logger.debug( " send message to Logstash : %s ", str( logstashEvent ) )
                    else :
                        break
                

            else :
                # if not event, wait for a time
                # self.logger.warn( "sleep for: %s", str( self.readVoIPLogTimeout ) )
                time.sleep( self.readVoIPLogTimeout )

        # When main thread is stopped, the Polycube Packetcapture is removed
        boolResult = False
        
        if self.interceptionHandler :
            boolResult = self.interceptionHandler.interceptionStop( self.userID, self.providerID, self.serviceID )
        else :
            self.logger.error( "interception tool UNDEFINED or UNKNOWN (3)" )
        
        # stop all interception senders
        for k, v in self.interceptionSenders.items() :
            v.stop()

        self.logger.debug( "result of interception tool stop (2) : %s", str( boolResult ) )

    def stop( self ):
        self.is_active = False




