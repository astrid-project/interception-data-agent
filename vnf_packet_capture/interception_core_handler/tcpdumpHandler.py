"""
tcpdumpHandler

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import logging
import subprocess
from subprocess import DEVNULL
from pathlib import Path


# debug logger instance
debugLevel = logging.DEBUG
logger = logging.getLogger( __name__ )
logHandler = logging.StreamHandler()
logger.addHandler( logHandler )
logger.setLevel( debugLevel )

class TcpdumpHandler() :
    def __init__( self, savedInterceptionPath = "./", savedInterceptionFileName = "capture.pcap" ) :
        self.packetCaptureList = {}
        self.savedInterceptionPath = savedInterceptionPath
        self.savedInterceptionFileName = savedInterceptionFileName

    def __composeTcpdumpCommand( self, srcAddress = None, srcPort = None, dstAddress = None, dstPort = None, 
                                    interfaceToAttachName = None,
                                    pcapFilePath = "./", pcapFileName = "capture.pcap" ) :
        args = [ "tcpdump"]
        firstFilter = True
        if interfaceToAttachName :
            args.append( "-i" )
            args.append( interfaceToAttachName )

        # Traffic filters
        if srcAddress :
            if firstFilter == False :
                args.append( "and" )
            else :
                firstFilter = False
            args.append( "src" )
            args.append( srcAddress )
        if dstAddress :
            if firstFilter == False :
                args.append( "or" )
            else :
                firstFilter =  False
            args.append( "dst" )
            args.append( dstAddress )
        if srcPort :
            if firstFilter == False :
                args.append( "and" )
            else :
                firstFilter = False
            args.append( "src port")
            args.append( str( srcPort ) )
        if dstPort :
            if firstFilter == False :
                args.append( "or" )
            else :
                firstFilter = False
            args.append( "dst port" )
            args.append( str( dstPort ) )

        # Create path if different from local directory
        if pcapFilePath != "./" :
            Path( pcapFilePath ).mkdir( parents = True, exist_ok = True )

        completePath = pcapFilePath + pcapFileName
        args.append( "-w" )
        args.append( completePath )
        logger.debug( args )
        return args

    def interceptionStart( self, userID, providerID, serviceID, 
            srcAddress = None, srcPort = None, dstAddress = None, dstPort = None, 
            l4Proto = None, interfaceToAttachName = None ) :
        logger.debug( "interceptionStart" )
        packetCaptureName = str( serviceID ) + "." + str( providerID ) + "." + str( userID )

        elem = self.packetCaptureList.get( packetCaptureName, False )
        if elem : 
            if elem[0] == srcAddress and elem[1] == srcPort and \
                    elem[2] == dstAddress and elem[3] == dstPort :
                logger.debug( "packetcapture already running for this request")
                return True
            else :
                self.interceptionStop( userID, providerID, serviceID, srcAddress, srcPort,
                    dstAddress, dstPort, l4Proto )

        args = self.__composeTcpdumpCommand( srcAddress, srcPort, dstAddress, dstPort, interfaceToAttachName,
            self.savedInterceptionPath, self.savedInterceptionFileName )
        tcpdumpProcess = subprocess.Popen( args, stdout = DEVNULL, stderr = DEVNULL )

        self.packetCaptureList[ packetCaptureName ] = ( srcAddress, srcPort, dstAddress, 
                dstPort, l4Proto, tcpdumpProcess )
        return True


    def interceptionStop( self, userID, providerID, serviceID ) :
        logger.debug( "interceptionStop" )
        packetCaptureName = str( serviceID ) + "." + str( providerID ) + "." + str( userID )
        packetCaptureData = self.packetCaptureList.pop( packetCaptureName, False )
        if packetCaptureData :
            tcpdumpProcess = packetCaptureData[5]
            # check if "tcpdump" process is yet running
            if tcpdumpProcess.poll() == None :
                # terminate the "tcpdump" process
                tcpdumpProcess.terminate()
            return True

        return False
    


