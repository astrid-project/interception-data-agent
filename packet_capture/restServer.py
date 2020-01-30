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

logger = logging.getLogger( "mainLogger" )

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
        result = {}
        return json.dumps( result ), status.HTTP_200_OK

class InterceptionStop( Resource ) :
    def __init__( self ) :
        return None
    def get( self ) :
        logger.debug( __file__ + " get " )
        result = {}
        return json.dumps( result ), status.HTTP_200_OK
    def post( self ) :
        logger.debug( __file__ + " post " )
        result = {}
        return json.dumps( result ), status.HTTP_200_OK

class RestServer():
    def __init__( self, address, port ):
        self.app = Flask( __name__ )
        self.api = Api( self.app )
        self.api.add_resource( InterceptionStart, "/start" )
        self.api.add_resource( InterceptionStop, "/stop" )
        self.app.run( host=address, port=port )
        
        return None

