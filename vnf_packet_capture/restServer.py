"""
restServer

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

from flask import Flask, request
from flask_restful import Resource, Api
from flask_api import status
import json
import logging

from polycubeHandler import PolycubeHandler

logger = logging.getLogger( "mainLogger" )
polycubeHandler = PolycubeHandler()

class InterceptionStart( Resource ) :
    def __init__( self ) :
        return None

    def get( self ) :
        logger.debug( __file__ + " get " )
        result = {}
        return json.dumps( result ), status.HTTP_200_OK

    def post( self ) :
        logger.debug( __file__ + " post " )
        requestJson = request.get_json()

        userID = requestJson.get( "userID", "")
        serviceProviderID = requestJson.get( "serviceProviderID", "")
        serviceID = requestJson.get( "serviceID", "")

        logger.debug( json.dumps( requestJson ) )
        logger.debug( "userID={} , serviceProviderID={} , serviceID={} " \
        % ( userID, serviceProviderID, serviceID ) )

        if userID != "" and serviceProviderID != "" and serviceID != "" : 
            # RETRIVE INFORMATION (IP, PORT of USERID)
            # to be done...
            # START PACKET CAPTURE
            logger.debug( "create packet capture" )
            boolResult = polycubeHandler.interceptionStart( userID, serviceProviderID, serviceID, \
                "0.0.0.0", 0, "0.0.0.0", 0, "", "enp0s3" )
        
        result = {}
        if boolResult :
            return json.dumps( result ), status.HTTP_200_OK
        else :
            return json.dumps( result ), status.HTTP_500_INTERNAL_SERVER_ERROR

class InterceptionStop( Resource ) :
    def __init__( self ) :
        return None

    def get( self ) :
        logger.debug( __file__ + " get " )
        result = {}
        return json.dumps( result ), status.HTTP_200_OK

    def post( self ) :
        logger.debug( __file__ + " post " )
        requestJson = request.get_json()

        userID = requestJson.get( "userID", "")
        serviceProviderID = requestJson.get( "serviceProviderID", "")
        serviceID = requestJson.get( "serviceID", "")

        logger.debug( "userID={} , serviceProviderID={} , serviceID={} " \
        % ( userID, serviceProviderID, serviceID ) )

        if userID != "" and serviceProviderID != "" and serviceID != "" : 
            # STOP PACKET CAPTURE
            boolResult = polycubeHandler.interceptionStop( userID, serviceProviderID, serviceID, 
            "0.0.0.0", 0, "0.0.0.0", 0, "" )
            logger.debug( "remove packet capture" )

        result = {}
        if boolResult :
            return json.dumps( result ), status.HTTP_200_OK
        else :
            return json.dumps( result ), status.HTTP_500_INTERNAL_SERVER_ERROR

class RestServer():
    def __init__( self, address, port ):
        self.app = Flask( __name__ )
        self.api = Api( self.app )
        self.api.add_resource( InterceptionStart, "/interceptionstart" )
        self.api.add_resource( InterceptionStop, "/interceptionstop" )
        # "threaded = True" is used to multi-thread parallel requests managing
        #self.app.run( host=address, port=port, threaded = True )
        self.app.run( host=address, port=port )
        
        return None

