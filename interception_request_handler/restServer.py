"""
restServer

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import requests
import socketserver
import json


from http.server import HTTPServer, BaseHTTPRequestHandler
from myLogger import MyLogger

"""
RestServerHandler
::
set "logger" variable
"""
class RestServerHandler( BaseHTTPRequestHandler ) :
    interceptionTasks = {}
    contextBrokerAddress = ""
    contextBrokerPort = 0
    logger = ""
    
    def _set_headers( self, code = 200 ) :
        self.send_response( code ) 
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
        response = { 'ok' : 'ok' }  # response
        # self._set_headers()
        requestMessageLength = int( self.headers.get( 'content-length' ) )
        requestMessage = ""
        requestJson = {}
        RestServerHandler.logger.debug( "request message length: %i", requestMessageLength )
        if requestMessageLength > 0 :
            requestMessage = self.rfile.read( requestMessageLength ).decode( "utf-8" )
            requestJson = json.loads( requestMessage ) if requestMessage else {}
            RestServerHandler.logger.debug( json.dumps( requestJson ) )
        
        # /interceptionstart
        if self.path == "/interceptionrequeststart" :
            RestServerHandler.logger.debug( "POST request : interception request start" )
            userID = requestJson.get( "userID", "" )
            providerID = requestJson.get( "serviceProviderID", "" )
            serviceID = requestJson.get( "serviceID", "" )

            interceptionName = str( serviceID ) + str( providerID ) + str( userID )
            
            if RestServerHandler.interceptionTasks.get( interceptionName, False ) :
                RestServerHandler.logger.debug( "interception request task yet exist !" )
            else :
                RestServerHandler.interceptionTasks[ interceptionName ] = True
                
                # TODO : execute request to CB
                url = "http://" + str( RestServerHandler.contextBrokerAddress ) + ":" + \
                    str( RestServerHandler.contextBrokerPort )
                payload = "{}" # Json format
                try :
                    cbResponse = requests.post( url , data = payload )
                    RestServerHandler.logger.debug( "start request sent to %s", str( url ) )
                    RestServerHandler.logger.debug( cbResponse.text() )
                    RestServerHandler.logger.debug( cbResponse.json() )
                    RestServerHandler.logger.debug( cbResponse.status_code )
                    self._set_headers( cbResponse.status_code )
                except Exception as e :
                    RestServerHandler.logger.debug( e )
                    self._set_headers( requests.codes["internal_server_error"] )
                
        
        # /interceptionstop
        if self.path == "/interceptionrequeststop" :
            RestServerHandler.logger.debug( "POST request : interception request stop" )
            userID = requestJson.get( "userID", "" )
            providerID = requestJson.get( "serviceProviderID", "" )
            serviceID = requestJson.get( "serviceID", "" )

            interceptionName = str( serviceID ) + str( providerID ) + str( userID )
            interceptionTask = RestServerHandler.interceptionTasks.pop( interceptionName, False )
            if interceptionTask :
                # TODO : execute request to CB
                url = "http://" + str( RestServerHandler.contextBrokerAddress ) + ":" + \
                    str( RestServerHandler.contextBrokerPort )
                payload = "{}" # Json format
                try :
                    cbResponse = requests.post( url, data = payload )
                    RestServerHandler.logger.debug( "stop request sent to %s", str( url ) )
                    RestServerHandler.logger.debug( cbResponse.text() )
                    RestServerHandler.logger.debug( cbResponse.json() )
                    RestServerHandler.logger.debug( cbResponse.status_code )
                    self._set_headers( cbResponse.status_code )
                except Exception as e :
                    RestServerHandler.logger.debug( e )
                    self._set_headers( requests.code["internal_server_error"] )

        self.wfile.write( bytes( json.dumps( response ), "utf-8" ) )


class RestServer():
    def __init__( self, restServerAddress, restServerPort,
        contextBrokerAddress, contextBrokerPort ):
        
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )
        self.restServerAddress = restServerAddress
        self.restServerPort = restServerPort
        self.handler = RestServerHandler
        RestServerHandler.contextBrokerAddress = contextBrokerAddress
        RestServerHandler.contextBrokerPort = contextBrokerPort
        RestServerHandler.logger = self.logger
        return None
    
    def run( self ) :
        with socketserver.TCPServer( ( self.restServerAddress, self.restServerPort ), self.handler ) as httpd:
            self.logger.debug( "web server started" )
            httpd.serve_forever()
        
        return None

