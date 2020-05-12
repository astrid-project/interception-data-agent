"""
fileFeed

developed by @Infocom - 2020
info: guerino.lamanna@infocomgenova.it
"""

import base64

from myLogger import MyLogger

class FileFeed() :
    id = 0
    def __init__( self, filePath = "./", fileName = "interception.pcap" ) :
        self.filePath = filePath
        self.fileName = fileName
        myLogger = MyLogger()
        self.logger = myLogger.getLogger( __name__ + str( FileFeed.id ) )
        FileFeed.id += 1
        self.file = None
        completePath = self.filePath + self.fileName
        self.logger.debug( "open file %s ", completePath )
        try :
            self.file = open( completePath, "ba" )
        except Exception as e :
            self.logger.debug( "impossible to open file: %s in folder: %s \
                - error : %s", 
            str( self.fileName ), str( self.filePath ), str( e ) ) 

    """
    writeStr
    ::
    message is a string to decode in 64bit format
    ::
    return False if some problems raised
    """
    def writeStr( self, message : str ) :
        if self.file :
            data = base64.b64decode( message )
            self.file.write( data )
            return True
        return False


    def writeByte( self, message : bytes ) :
        if self.file : 
            self.file.write( message )
            return True
        return False

    def close( self ) :
        self.file.close()