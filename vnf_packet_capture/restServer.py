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
        boolResult = False
        response = {} # response
        self._set_headers()
        requestMessageLength = int( self.headers.get( 'content-length' ) )
        requestMessage = ""
        requestJson = {}
        logger.debug( "request message length: %i", requestMessageLength )
        if requestMessageLength > 0 :
            requestMessage = self.rfile.read( requestMessageLength ).decode( "utf-8" )
            requestJson = json.loads( requestMessage )
            logger.debug( json.dumps( requestJson ) )
        
        # /interceptionstart
        if self.path == "/interceptionstart" :
            logger.debug( "POST request : interception start" )

            userID = requestJson.get( "userID", "")
            serviceProviderID = requestJson.get( "serviceProviderID", "")
            serviceID = requestJson.get( "serviceID", "")

            if userID != "" and serviceProviderID != "" and serviceID != "" : 
                # RETRIVE INFORMATION (IP, PORT of USERID)
                # to be done...
                srcAddress = "0.0.0.0"
                srcPort = 0
                dstAddress = "0.0.0.0"
                dstPort = 0
                l4Proto = ""
                interfaceToAttachName = "enp0s3"
                # START PACKET CAPTURE
                logger.debug( "create packet capture" )
                boolResult = polycubeHandler.interceptionStart( userID, serviceProviderID, serviceID, \
                    srcAddress, srcPort, dstAddress, dstPort, l4Proto, interfaceToAttachName )
            
            if boolResult :
                self.send_response( 200 ) 
                self.wfile.write( bytes( json.dumps( response ), "utf-8" ) ) #, status.HTTP_200_OK
            else :
                self.send_response( 500 ) 
                self.wfile.write( bytes( json.dumps( response ), "utf-8" ) ) #, status.HTTP_500_INTERNAL_SERVER_ERROR

            return 
        
        # /interceptionstop
        if self.path == "/interceptionstop" :
            logger.debug( "POST request : interception stop" )

            userID = requestJson.get( "userID", "")
            serviceProviderID = requestJson.get( "serviceProviderID", "")
            serviceID = requestJson.get( "serviceID", "")

            if userID != "" and serviceProviderID != "" and serviceID != "" : 
                # STOP PACKET CAPTURE
                boolResult = polycubeHandler.interceptionStop( userID, serviceProviderID, serviceID, 
                "0.0.0.0", 0, "0.0.0.0", 0, "" )
                logger.debug( "remove packet capture" )

            if boolResult :
                self.send_response( 200 ) 
                self.wfile.write( bytes( json.dumps( response ), "utf-8" ) ) #, status.HTTP_200_OK
            else :
                self.send_response( 500 ) 
                self.wfile.write( bytes( json.dumps( response ), "utf-8" ) ) #, status.HTTP_500_OK

            return

        self.wfile.write( bytes( json.dumps( response ), "utf-8" ) )


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

