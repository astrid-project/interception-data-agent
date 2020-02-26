"""
parsingHandler

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from enum import Enum
from myLogger import MyLogger

class EventType( Enum ) :
    Undefined = 0
    InterceptedIPParameters = 1

class Event() :
    eventID = 0
    def __init__( self, eventName = EventType.Undefined ) :
        self.eventName = eventName
        self.data = {}
        self.__id = Event.eventID
        Event.eventID += 1

    def getName( self ) :
        return self.eventName

    def getData( self ) :
        return self.data

    def setName( self, eventName = EventType.Undefined ) :
        self.eventName = eventName

    def addData( self, parameter = "", data = "" ) :
        self.data[ parameter ] = data

class ParsingHandler() :
    def __init__( self, userID, providerID, serviceID,
    filePath = "./", fileName = "log.log" ):
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )
        self.filePath = filePath
        self.fileName = fileName
        self.events = {}
        self.fp = ""
        self.userID = userID
        self.providerID = providerID
        self.serviceID = serviceID
        
        try :
            self.fp = open( self.filePath + self.fileName , "r" )
        except Exception as e:
            self.logger.error( "error: impossible to open %s%s", self.filePath, self.fileName )
            self.logger.error( "error: %s", e )
        

    """
    readFileAndGetEvent
    ::
    Read a line from log file and decode the data in an event (packet capture data, missing call, etc).
    The event is inserted in a buffer
    ::
    return "True" if an event, "False" otherwise
    """
    def readFileAndGetEvent( self ) :
        if self.fp :
            line = self.fp.readline()
            if not line :
                self.logger.debug( "end of file" )
                return False
            self.logger.debug( "read line: %s", line )

            # TODO : parse line and create and Event
            return True
        
        return False

    """
    changeInterceptedIPParameters
    ::
    Return event if intercepted user IP parameters are changed
    data are :
    ::
    - userID / providerID / serviceID / srcAddress / srcPort / dstAddress / dstPort
    """
    def changeInterceptedIPParameters( self ) :
        for event in self.events :
            if event.eventName == EventType.InterceptedIPParameters :
                self.events.remove( event )
                return event.data
        return {}

