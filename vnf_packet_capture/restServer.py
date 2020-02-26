"""
restServer

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import json

from interceptionTask import InterceptionTask
from myLogger import MyLogger

"""
RestServerHandler
::
set "logger" variable
"""
class RestServerHandler( BaseHTTPRequestHandler ) :
    interceptionTasks = {}
    polycubeServerAddress = ""
    polycubeServerPort = 0
    interceptionInterfaceName = ""
    logVoIPFilePath = ""
    logVoIPFileName = ""
    readVoIPLogTimeout = 0
    logger = ""

    def _set_headers( self ) :
        self.send_response( 200 ) 
        self.send_header( "Content-type", "text/json" )
        self.end_headers()

    def do_GET( self ) :
        self._set_headers()
        return

    def do_HEAD( self ) :
        self._set_headers()
        return
    
    def do_POST( self ) :
        boolResult = False
        response = {} # response
        self._set_headers()
        requestMessageLength = int( self.headers.get( 'content-length' ) )
        requestMessage = ""
        requestJson = {}
        RestServerHandler.logger.debug( "request message length: %i", requestMessageLength )
        if requestMessageLength > 0 :
            requestMessage = self.rfile.read( requestMessageLength ).decode( "utf-8" )
            requestJson = json.loads( requestMessage ) if requestMessage else {}
            RestServerHandler.logger.debug( json.dumps( requestJson ) )
        
        # /interceptionstart
        if self.path == "/interceptionstart" :
            RestServerHandler.logger.debug( "POST request : interception start" )
            if "userID" in requestJson :
                userID = requestJson[ "userID" ]
            else :
                userID = ""
            if "providerID" in requestJson : 
                providerID = requestJson[ "providerID" ]
            else :
                providerID = ""
            if "serviceID" in requestJson :
                serviceID = requestJson[ "serviceID" ]
            else :
                serviceID = ""

            interceptionName = str( serviceID ) + str( providerID ) + str( userID )
            
            if RestServerHandler.interceptionTasks.get( interceptionName, False ) :
                RestServerHandler.logger.debug( "interception task yet exist !" )
            else :
                interceptionTask = InterceptionTask( userID, providerID, serviceID, 
                    RestServerHandler.polycubeServerAddress, RestServerHandler.polycubeServerPort, 
                    RestServerHandler.interceptionInterfaceName, RestServerHandler.logVoIPFilePath, 
                    RestServerHandler.logVoIPFileName, RestServerHandler.readVoIPLogTimeout )
                interceptionTask.start()
                RestServerHandler.interceptionTasks[ interceptionName ] = interceptionTask
                
        
        # /interceptionstop
        if self.path == "/interceptionstop" :
            RestServerHandler.logger.debug( "POST request : interception stop" )
            if "userID" in requestJson :
                userID = requestJson[ "userID" ]
            else :
                userID = ""
            if "providerID" in requestJson :
                providerID = requestJson[ "providerID" ]
            else :
                providerID = ""
            if "serviceID" in requestJson :
                serviceID = requestJson[ "serviceID" ]
            else :
                serviceID = ""

            interceptionName = str( serviceID ) + str( providerID ) + str( userID )
            interceptionTask = RestServerHandler.interceptionTasks.pop( interceptionName, False )
            if interceptionTask :
                interceptionTask.stop()

        self.wfile.write( bytes( json.dumps( response ), "utf-8" ) )


class RestServer():
    def __init__( self, restServerAddress, restServerPort,
        polycubeServerAddress, polycubeServerPort, interceptionInterfaceName,
        logVoIPFilePath, logVoIPFileName, readVoIPLogTimeout ):
        
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )
        self.restServerAddress = restServerAddress
        self.restServerPort = restServerPort
        self.handler = RestServerHandler
        RestServerHandler.polycubeServerAddress = polycubeServerAddress
        RestServerHandler.polycubeServerPort = polycubeServerPort
        RestServerHandler.interceptionInterfaceName = interceptionInterfaceName
        RestServerHandler.logVoIPFilePath = logVoIPFilePath
        RestServerHandler.logVoIPFileName = logVoIPFileName
        RestServerHandler.readVoIPLogTimeout = readVoIPLogTimeout
        RestServerHandler.logger = self.logger
        return None
    
    def run( self ) :
        with socketserver.TCPServer( ( self.restServerAddress, self.restServerPort ), self.handler ) as httpd:
            self.logger.debug( "web server started" )
            httpd.serve_forever()
        
        return None

