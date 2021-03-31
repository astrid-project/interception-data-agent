"""
parsingHandler

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import time
import calendar

from enum import Enum
from myLogger import MyLogger
from IPy import IP

class EventType( Enum ) :
    Undefined = 0
    InterceptedIPParameters = 1
    IncomingCallParameters = 2
    StartCallParameters = 3
    StopCallParameters = 4
    RejectedCallParameters = 5

class Event() :
    eventID = 0
    def __init__( self, eventName = EventType.Undefined ) :
        self.eventName = eventName
        self.data = dict()
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
        self.startEpochTime = time.time()

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
                    #self.logger.debug( "end of file" )
                    break
                #self.logger.debug( "read line: %s", line )

                # parse line and create and Event
                # First event creation doesn't need data check
                if self.__findOutChangeInterceptedIPParametersEvent( line ) :
                    returnValue = True

                # all these events creations need for data check
                if self.__outOfDataLineCheck( line ):
                    if self.__incomingCallEvent( line ) :
                        returnValue = True
                    if self.__startCallEvent( line ) :
                        returnValue = True
                    if self.__stopCallEvent( line ) :
                        returnValue = True
                    if self.__rejectedCallEvent( line ) :
                        returnValue = True
        
        return returnValue


    """
    __readEpochTimeFromString
    ::
    Read dateTime from a string like "ANYSTRING [04/Mar/2020:12:19:53 +0000] ANYSTRING"
    It is usefull only for VoIP logfile
    ::
    return the Epoch time, -1 if error
    """
    def __readEpochTimeFromString( self, dt ):
        epochTime = -1
        try:
            timeString = dt.split('[')[1].split(']')[0]
            utcTime = time.strptime( timeString, "%d/%b/%Y:%H:%M:%S %z" )
            epochTime = calendar.timegm( utcTime )
        except Exception as e:
            self.logger.error( "error: %s", e )

        return epochTime


    """
    __outOfDateLineCheck
    ::
    Check if the date inside the line has a date after or before the starting time of the software
    ::
    It returns True if the line date is next of starting time. Otherwise it returns False
    """
    def __outOfDataLineCheck( self, line = "" ) :
        if line != "" :
            # Check if data is out of date 
            epochTimeFromString = self.__readEpochTimeFromString( line )
            if epochTimeFromString - self.startEpochTime < 0 :
                self.logger.debug( "Out-of-date ( start: %d, value: %d ) data: %s", 
                        self.startEpochTime, epochTimeFromString, line )
                return False
            return True
        return False


    """
    findOutchangeInterceptedIPParametersEvent
    ::
    Update Parsinghandler object adding "InterceptedIPParameters" event and data to self.events array
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
    incomingCallEvent
    ::
    Update Parsinghandler object adding "IncomingCallParameters" event and data to self.events array
    ::
    it returns True if it find out some events, False if it doesn't
    ::
    example::
    INFO  [2020-01-30 14:54:29,199] incoming call from +306944125708 to +306941234567
    """
    def __incomingCallEvent( self, line = "" ) :
        if line != "" :
            elems = line.split()
            userFrom = ""
            userTo = ""

            # check if "incoming call" is the line
            if "incoming call" in line:
                # check userID of calling user
                for i in range( len( elems ) ) :
                    if elems[ i ] == "from" :
                        if i < len( elems ) :
                            userFrom = elems[ i + 1 ]
                        else :
                            userFrom = ""
                    if elems[ i ] == "to" :
                        if i < len( elems ) :
                            userTo = elems[ i + 1 ]
                        else :
                            userTo = ""
                self.logger.debug( "incoming call from user: %s to user: %s",
                    str( userFrom ), str( userTo ) ) 
                
                # check if userFrom or userTo is the intercepted user
                if userFrom == self.userID or userTo == self.userID :
                    # create and save a specific event
                    event = Event( EventType.IncomingCallParameters )
                    event.data[ "userFrom" ] = userFrom
                    event.data[ "userTo" ] = userTo
                    self.events.add( event )    
                    return True
                else :
                    return False
        return False

    """
    startCallEvent
    ::
    Update Parsinghandler object adding "StartCallParameters" event and data to self.events array
    ::
    it returns True if it find out some events, False if it doesn't
    ::
    example::
    INFO  [2020-01-30 14:54:29,199] start call from +306944125708 to +306941234567
    """
    def __startCallEvent( self, line = "" ) :
        if line != "" :
            elems = line.split()
            userFrom = ""
            userTo = ""
            # check if "start call" is the line
            if "start call" in line:
                # check userID of calling user
                for i in range( len( elems ) ) :
                    if elems[ i ] == "from" :
                        if i < len( elems ) :
                            userFrom = elems[ i + 1 ]
                        else :
                            userFrom = ""
                    if elems[ i ] == "to" :
                        if i < len( elems ) :
                            userTo = elems[ i + 1 ]
                        else :
                            userTo = ""
                self.logger.debug( "start call from user: %s to user: %s",
                    str( userFrom ), str( userTo ) ) 
                
                # check if userFrom or userTo is the intercepted User
                if userFrom == self.userID or userTo == self.userID :
                    # create and save a specific event
                    event = Event( EventType.StartCallParameters )
                    event.data[ "userFrom" ] = userFrom
                    event.data[ "userTo" ] = userTo
                    self.events.add( event )
                    return True
                else :
                    return False
        return False

    """
    stopCallEvent
    ::
    Update Parsinghandler object adding "StopCallParameters" event and data to self.events array
    ::
    it returns True if it find out some events, False if it doesn't
    ::
    example::
    INFO  [2020-01-30 14:54:29,199] stop call from +306944125708 to +306941234567
    """
    def __stopCallEvent( self, line = "" ) :
        if line != "" :
            elems = line.split()
            userFrom = ""
            userTo = ""
            # check if "stop call" is the line
            if "stop call" in line:
                # check userID of calling user
                for i in range( len( elems ) ) :
                    if elems[ i ] == "from" :
                        if i < len( elems ) :
                            userFrom = elems[ i + 1 ]
                        else :
                            userFrom = ""
                    if elems[ i ] == "to" :
                        if i < len( elems ) :
                            userTo = elems[ i + 1 ]
                        else :
                            userTo = ""
                self.logger.debug( "stop call from user: %s to user: %s",
                    str( userFrom ), str( userTo ) ) 
                
                # check if userFrom or userTo is the intercepted User
                if userFrom == self.userID or userTo == self.userID :
                    # create and save a specific event
                    event = Event( EventType.StopCallParameters )
                    event.data[ "userFrom" ] = userFrom
                    event.data[ "userTo" ] = userTo
                    self.events.add( event )
                    return True
                else : 
                    return False
        return False

    """
    rejectedCallEvent
    ::
    Update Parsinghandler object adding "RejectedCallParameters" event and data to self.events array
    ::
    it returns True if it find out some events, False if it doesn't
    ::
    example::
    INFO  [2020-01-30 14:54:29,199] rejected call from +306944125708 to +306941234567
    """
    def __rejectedCallEvent( self, line = "" ) :
        if line != "" :
            elems = line.split()
            userFrom = ""
            userTo = ""
            # check if "rejected call" is the line
            if "rejected call" in line:
                # check userID of calling user
                for i in range( len( elems ) ) :
                    if elems[ i ] == "from" :
                        if i < len( elems ) :
                            userFrom = elems[ i + 1 ]
                        else :
                            userFrom = ""
                    if elems[ i ] == "to" :
                        if i < len( elems ) :
                            userTo = elems[ i + 1 ]
                        else :
                            userTo = ""
                self.logger.debug( "rejected call from user: %s to user: %s",
                    str( userFrom ), str( userTo ) ) 
                
                # check if userFrom or userTo is the intercepted User
                if userFrom == self.userID or userTo == self.userID :
                    # create and save a specific event
                    event = Event( EventType.RejectedCallParameters )
                    event.data[ "userFrom" ] = userFrom
                    event.data[ "userTo" ] = userTo
                    self.events.add( event )     
                    return True
                else :
                    return False
        return False

    """
    changeInterceptedIPParameters
    ::
    Returns event if intercepted user IP parameters are changed
    Filled by findOutchangeInterceptedIPParametersEvent
    data are :
    ::
    - srcAddress
    """
    def changeInterceptedIPParameters( self ) :
        for event in self.events :
            if event.eventName == EventType.InterceptedIPParameters :
                self.events.remove( event )
                return event.getData()
        return {}

    """
    incomingCallParameters
    ::
    Returns event if a call is coming
    Filled by incomingCallEvent
    data are :
    ::
    - userFrom , userTo
    """
    def incomingCallParameters( self ) :
        for event in self.events :
            if event.eventName == EventType.IncomingCallParameters :
                self.events.remove( event )
                return event.getData()
        return {}

    """
    startCallParameters
    ::
    Returns event if a call is coming
    Filled by startCallEvent
    data are :
    ::
    - userFrom , userTo
    """
    def startCallParameters( self ) :
        for event in self.events :
            if event.eventName == EventType.StartCallParameters :
                self.events.remove( event )
                return event.getData()
        return {}

    """
    stopCallParameters
    ::
    Returns event if a call is coming
    Filled by stopCallEvent
    data are :
    ::
    - userFrom , userTo
    """
    def stopCallParameters( self ) :
        for event in self.events :
            if event.eventName == EventType.StopCallParameters :
                self.events.remove( event )
                return event.getData()
        return {}

    """
    rejectedCallParameters
    ::
    Returns event if a call is coming
    Filled by rejectedCallEvent
    data are :
    ::
    - userFrom , userTo
    """
    def rejectedCallParameters( self ) :
        for event in self.events :
            if event.eventName == EventType.RejectedCallParameters :
                self.events.remove( event )
                return event.getData()
        return {}
