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
from kafkaClient import KafkaClient

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
    kafkaClient = ""
    
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
        requestFound = False
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
            requestFound = True
            RestServerHandler.logger.debug( "POST request : interception request start" )
            userID = requestJson.get( "userID", "" )
            providerID = requestJson.get( "serviceProviderID", "" )
            serviceID = requestJson.get( "serviceID", "" )

            interceptionName = str( serviceID ) + str( providerID ) + str( userID )
            
            if RestServerHandler.interceptionTasks.get( interceptionName, False ) :
                RestServerHandler.logger.debug( "interception request task yet exist !" )
                self._set_headers()
            else :
                error = None

                if RestServerHandler.contextBrokerAddress != "0.0.0.0" and \
                        RestServerHandler.contextBrokerAddress != "" :
                    # TODO : execute request to CB
                    url = "http://" + str( RestServerHandler.contextBrokerAddress ) + ":" + \
                        str( RestServerHandler.contextBrokerPort )
                    payload = "{}" # Json format
                    try :
                        cbResponse = requests.post( url , data = payload, timeout = 3 )
                        RestServerHandler.logger.debug( "start request sent to %s", str( url ) )
                        RestServerHandler.logger.debug( cbResponse.text() )
                        RestServerHandler.logger.debug( cbResponse.json() )
                        RestServerHandler.logger.debug( cbResponse.status_code )
                        self._set_headers( cbResponse.status_code )
                    except Exception as e :
                        error = e
                        RestServerHandler.logger.debug( e )
                        # 500 = internal server error
                        self._set_headers( 500 )

                if RestServerHandler.kafkaClient != "" and \
                        RestServerHandler.kafkaClient != None :
                    # send message to Kafka Broker
                    messageToSend = dict()
                    messageToSend[ "userID" ] = userID
                    messageToSend[ "providerID" ] = providerID
                    messageToSend[ "serviceID" ] = serviceID
                    messageToSend[ "action" ] = "start"
                    self._set_headers()
                    try :
                        RestServerHandler.kafkaClient.send( messageToSend )
                    except Exception as e :
                        error = e
                        RestServerHandler.logger.debug( e )
                        # 500 = internal server error
                        self._set_headers( 500 )
                
                # if NO error, add interceptionTask to the list
                if error == None :
                    RestServerHandler.interceptionTasks[ interceptionName ] = True
                else :
                    response = { "error" : str( error ) }

                
        
        # /interceptionstop
        if self.path == "/interceptionrequeststop" :
            requestFound = True
            RestServerHandler.logger.debug( "POST request : interception request stop" )
            userID = requestJson.get( "userID", "" )
            providerID = requestJson.get( "serviceProviderID", "" )
            serviceID = requestJson.get( "serviceID", "" )

            interceptionName = str( serviceID ) + str( providerID ) + str( userID )
            interceptionTask = RestServerHandler.interceptionTasks.pop( interceptionName, False )
            if interceptionTask :
                error = None
                if RestServerHandler.contextBrokerAddress != "0.0.0.0" and \
                        RestServerHandler.contextBrokerAddress != "" :
                    # TODO : execute request to CB
                    url = "http://" + str( RestServerHandler.contextBrokerAddress ) + ":" + \
                        str( RestServerHandler.contextBrokerPort )
                    payload = "{}" # Json format
                    try :
                        cbResponse = requests.post( url, data = payload, timeout = 3 )
                        RestServerHandler.logger.debug( "stop request sent to %s", str( url ) )
                        RestServerHandler.logger.debug( cbResponse.text() )
                        RestServerHandler.logger.debug( cbResponse.json() )
                        RestServerHandler.logger.debug( cbResponse.status_code )
                        self._set_headers( cbResponse.status_code )
                    except Exception as e :
                        error = e
                        RestServerHandler.logger.debug( e )
                        # 500 = internal server error
                        self._set_headers( 500 )

                if RestServerHandler.kafkaClient != "" and \
                        RestServerHandler.kafkaClient != None :
                    # send command to Kafka broker
                    messageToSend = dict()
                    messageToSend[ "userID" ] = userID
                    messageToSend[ "providerID" ] = providerID
                    messageToSend[ "serviceID" ] = serviceID
                    messageToSend[ "action" ] = "stop"
                    self._set_headers()

                    try :
                        RestServerHandler.kafkaClient.send( messageToSend )
                    except Exception as e:
                        error = e
                        RestServerHandler.logger.debug( e )
                        # 500 = internal server error
                        self._set_headers( 500 )

                # if ERROR, add task to the list
                if error != None :
                    response = { "error" : str( error ) }
                    RestServerHandler.interceptionTasks[ interceptionName ] = True
            else :
                # 500 = internal server error
                response = { "error" : "interception name not found" }
                self._set_headers( 500 )
        
        if requestFound == False :
            # request (endpoint) not found
            response = { "error" : "endpoint not found" }
            self.logger.debug( "request (endpoint) not found" )
            # 404 = page not found
            self._set_headers( 404 )


        self.wfile.write( bytes( json.dumps( response ), "utf-8" ) )


class RestServer():
    def __init__( self, restServerAddress, restServerPort,
        contextBrokerAddress, contextBrokerPort,
        kafkaAddress, kafkaPort, kafkaTopic ):
        
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ )
        self.restServerAddress = restServerAddress
        self.restServerPort = restServerPort
        self.handler = RestServerHandler
        RestServerHandler.contextBrokerAddress = contextBrokerAddress
        RestServerHandler.contextBrokerPort = contextBrokerPort
        RestServerHandler.logger = self.logger
        if kafkaAddress != "" and kafkaPort != 0 :
            RestServerHandler.kafkaClient = KafkaClient( kafkaAddress, kafkaPort, kafkaTopic )
        return None
    
    def run( self ) :
        with socketserver.TCPServer( ( self.restServerAddress, self.restServerPort ), self.handler ) as httpd:
            self.logger.debug( "web server started" )
            httpd.serve_forever()
        
        return None

