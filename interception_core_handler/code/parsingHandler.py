"""
parsingHandler

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from enum import Enum
from myLogger import MyLogger
from IPy import IP

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
        self.events = set()
        self.fp = ""
        self.userID = userID
        self.providerID = providerID
        self.serviceID = serviceID

        # data used for parsing
        self.__readUserIP = ""
        
        try :
            self.fp = open( self.filePath + self.fileName , "r" )
        except Exception as e:
            self.logger.error( "error: impossible to open %s%s", self.filePath, self.fileName )
            self.logger.error( "error: %s", e )
        

    """
    readFileAndGetEvent
    ::
    Read all lines from a log file and decode the data in an event (packet capture data, missing call, etc).
    The event is inserted in a buffer
    ::
    return "True" if an event, "False" otherwise
    """
    def readFileAndGetEvent( self ) :
        returnValue = False
        while True :
            if self.fp :
                line = self.fp.readline()
                if not line :
                    self.logger.debug( "end of file" )
                    break
                #self.logger.debug( "read line: %s", line )

                # TODO : parse line and create and Event
                if self.__findOutChangeInterceptedIPParametersEvent( line ) :
                    returnValue = True
        
        return returnValue

    """
    findOutchangeInterceptedIPParametersEvent
    ::
    Update Parsinghandler object adding "changeInterceptedIP" event and data to self.events array
    ::
    it returns True if it find out some events, False if it doesn't
    ::
    example::
    62.74.14.183 - - [30/Jan/2020:14:54:29 +0000] "GET /v1/accounts/turn HTTP/1.1" 200 168 "-" "okhttp/3.8.1" 72
    INFO  [2020-01-30 14:54:29,199] org.whispersystems.textsecuregcm.auth.AccountAuthenticator: account for +306944125708 ispresent true
    """
    def __findOutChangeInterceptedIPParametersEvent( self, line = "" ) :
        if line != "" :
            elems = line.split()
            try :
                # check if first word is an IP address
                IP( elems[0] )
                self.__readUserIP = elems[0]
                self.logger.debug( " (1) Candidate user IP \"%s\" FOUND for User-ID \"%s\"", str( elems[0] ), str( self.userID ) )
                                    
                # Return False because algorithm is not complete
                # Now it search for "or.whispersystems...AccountAuthenticator" string
                return False
            except Exception as e :
                # this is the case when elems[0] is not an IP address
                if "org.whispersystems.textsecuregcm.auth.AccountAuthenticator:" in line :
                    if "ispresent true" in line :
                        isUserIdFound = 0
                        for elem in elems :
                            if isUserIdFound == 1 and elem == "for" :
                                isUserIdFound = 2
                                continue
                            if isUserIdFound == 2 :
                                if elem == self.userID :
                                    event = Event( EventType.InterceptedIPParameters )
                                    event.data[ "srcAddress" ] = self.__readUserIP
                                    self.events.add( event )
                                    self.__readUserIP = ""
                                    self.logger.debug( " (2) UserIP \"%s\" FOUND for userID \"%s\"", 
                                        str( event.data[ "srcAddress" ] ), str( self.userID ) )
                                    return True
                                return False
                            if elem == "account" :
                                isUserIdFound = 1
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

