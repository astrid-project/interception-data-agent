"""
restServer

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import json
import logging

from polycubeHandler import PolycubeHandler

#logger = logging.getLogger( __name__ )
logger = logging.getLogger( "mainLogger" )
polycubeHandler = PolycubeHandler()

class restServerHandler( BaseHTTPRequestHandler ) :
    #def __init__( self ) :
    #    return None

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
        response = {} # response
        self._set_headers()
        requestMessageLength = int( self.headers.get( 'content-length' ) )
        requestMessage = ""
        requestJson = {}
        logger.debug( "request message length: %i", requestMessageLength )
        if requestMessageLength > 0 :
            requestMessage = self.rfile.read( requestMessageLength ).decode( "utf-8" )
            requestJson = json.loads( requestMessage ) if requestMessage else {}
            logger.debug( json.dumps( requestJson ) )
        
        # /interceptionstart
        if self.path == "/interceptionstart" :
            logger.debug( "POST request : interception start" )
            None
        
        # /interceptionstop
        if self.path == "/interceptionstop" :
            logger.debug( "POST request : interception stop" )
            None

        self.wfile.write( bytes( json.dumps( response ), "utf-8" ) )

class InterceptionStart() :
    def __init__( self ) :
        return None

    def get( self ) :
        logger.debug( __file__ + " get " )
        result = {}
        return json.dumps( result ) #, status.HTTP_200_OK

    def post( self ) :
        logger.debug( __file__ + " post " )
        requestJson = None #request.get_json()

        userID = requestJson.get( "userID", "")
        serviceProviderID = requestJson.get( "serviceProviderID", "")
        serviceID = requestJson.get( "serviceID", "")

        logger.debug( json.dumps( requestJson ) )

        if userID != "" and serviceProviderID != "" and serviceID != "" : 
            # RETRIVE INFORMATION (IP, PORT of USERID)
            # to be done...
            # START PACKET CAPTURE
            logger.debug( "create packet capture" )
            boolResult = polycubeHandler.interceptionStart( userID, serviceProviderID, serviceID, \
                "0.0.0.0", 0, "0.0.0.0", 0, "", "enp0s3" )
        
        result = {}
        if boolResult :
            return json.dumps( result ) #, status.HTTP_200_OK
        else :
            return json.dumps( result ) #, status.HTTP_500_INTERNAL_SERVER_ERROR

class InterceptionStop() :
    def __init__( self ) :
        return None

    def get( self ) :
        logger.debug( __file__ + " get " )
        result = {}
        return json.dumps( result ) #, status.HTTP_200_OK

    def post( self ) :
        logger.debug( __file__ + " post " )
        requestJson = None #request.get_json()

        userID = requestJson.get( "userID", "")
        serviceProviderID = requestJson.get( "serviceProviderID", "")
        serviceID = requestJson.get( "serviceID", "")

        logger.debug( json.dumps( requestJson ) )

        if userID != "" and serviceProviderID != "" and serviceID != "" : 
            # STOP PACKET CAPTURE
            boolResult = polycubeHandler.interceptionStop( userID, serviceProviderID, serviceID, 
            "0.0.0.0", 0, "0.0.0.0", 0, "" )
            logger.debug( "remove packet capture" )

        result = {}
        if boolResult :
            return json.dumps( result ) #, status.HTTP_200_OK
        else :
            return json.dumps( result ) #, status.HTTP_500_INTERNAL_SERVER_ERROR

class RestServer():
    def __init__( self, address, port ):
        self.address = address
        self.port = port
        self.handler = restServerHandler
        return None
    
    def run( self ) :
        with socketserver.TCPServer( ( self.address, self.port ), self.handler ) as httpd:
            logger.debug( "web server started" )
            httpd.serve_forever()
        
        return None

