"""
logstashClient

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import json
import logstash
import logging

from enum import Enum
from myLogger import MyLogger


class LogstashEventAction( Enum ) :
    userRegistration = "user_registration"
    incomingCall = "incoming_call"
    startCall = "start_call"
    stopCall = "stop_call"
    rejectedCall = "rejected_call"
    undefined = "undefined"

"""
LogstashEvent
::
This class is to be used for Logstash events creation. Send objects using LogstashClient.
::
Every event is composed by:
- a message (string)
- extra data (dictionary) in the following structure :
        extra = {
            'test_string': 'python version: ' + repr(sys.version_info),
            'test_boolean': True,
            'test_dict': {'a': 1, 'b': 'c'},
            'test_float': 1.23,
            'test_integer': 123,
            'test_list': [1, 2, '3'],
        }
::
Every LogstashEvent object has mandatory extra fields:
- userid
- providerid
- serviceid
- event ("user registration", "coming call", "start call", "stop call", "rejected call", "undefined")
"""
class LogstashEvent() :
    def __init__( self, userID, providerID, serviceID, \
                  action : LogstashEventAction = LogstashEventAction.undefined ) :
        self.message = ""
        self.extraData = dict()
        self.extraData[ "userid" ] = userID
        self.extraData[ "providerid" ] = providerID
        self.extraData[ "serviceid" ] = serviceID
        self.extraData[ "event" ] = action
    
    def set( self, key, value = "" ) :
        self.extraData[ "key" ] = value

    def get( self, key ) :
        return self.extraData.get( key, "" )

    def getMessage( self ) :
        return self.message

    def getExtraData( self ) :
        return self.extraData


class LogstashClient() :
    def __init__( self, logstashAddress, logstashPort, logstashVersion = 1 ) :
        mylogger = MyLogger()
        self.logger = mylogger.getLogger( __name__ )
        self.address = logstashAddress
        self.port = logstashPort
        self.version = logstashVersion
        self.sender = logging.getLogger( "interception logger" )
        if len( self.sender.handlers ) == 0 :
           self.sender.setLevel( logging.INFO )
           self.sender.addHandler( logstash.TCPLogstashHandler( host = self.address, 
                                                             port = self.port, 
                                                             version = self.version ) )

    """
    sendMessage
    ::
    it sends message to Logstash
    ::
    logstashEvent = LogstashEvent()
    ::
    it returns TRUE if message sent, otherwise FALSE
    """
    def sendMessage( self, logstashEvent ) :
        self.logger.debug( " sending message to Logstash " )
        # change "action" field with an equal string, 
        # so for example: LogstashEventAction.incomingCall becomes "incoming_call"
        logstashEvent.extraData[ "event" ] = logstashEvent.extraData[ "event" ].value
        self.sender.info( logstashEvent.getMessage(), extra = logstashEvent.getExtraData() )
        return True
