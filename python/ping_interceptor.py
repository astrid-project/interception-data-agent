import threading, time, logging, socket, struct, select, sys
from Structures import icmpIpsAllowed
import ipaddress

ICMP_ECHO_REQUEST = 8 
ICMP_ECHOREPLY = 0

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time


class PingServer(threading.Thread):
    def __init__(self):

        threading.Thread.__init__(self)
        self.systemOperative = True

    def run(self):
        print('RUN thread PingServer')
        sockets = []
        
        if len( icmpIpsAllowed ) == 0 :
            print( "no ICMP IPs specified, exit" )
            return 

        for icmpIp in icmpIpsAllowed :
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
            s.bind( ( icmpIp, 1 ) )
            sockets.append( s )
        time_left = 1
               
        while self.systemOperative:
            ready = select.select(sockets, [], [], time_left)
            print( ready )
            for elem in ready[0] :
                rec_packet, addr = elem.recvfrom(2048)
                printable_ip = addr[0]
                printable_port = addr[1]
                print ("printable_ip: " + str(printable_ip) + " printable_port: " + str(printable_port))
                ipHeader = rec_packet[:20]
                # iphVersion (8), iphTypeOfSvc (8), iphLength (16), iphID (16), iphFlags (16), iphTTL (8), iphProtocol (8), iphChecksum (16), iphSrcIP (32), iphDestIP (32)
                iphVersion, iphTypeOfSvc, iphLength, iphID, iphFlags, iphTTL, iphProtocol, iphChecksum, iphSrcIP, iphDestIP = struct.unpack("!BBHHHBBHII", ipHeader)
                print ("ipHeader: iphVersion: ["+ str(iphVersion) + "] iphTypeOfSvc: [" + str(iphTypeOfSvc) + "] iphLength: [" + str(iphLength) + \
                "] iphID: [" + str(iphID) + "] iphFlags: [" + str(iphFlags) + "] iphTTL: [" + str(iphTTL) + "] iphProtocol: [" + str(iphProtocol) + \
                "] iphChecksum: [" + str(iphChecksum) + "] iphSrcIP: [" +  str(ipaddress.ip_address(iphSrcIP)) + "] iphDestIP: [" + str(ipaddress.ip_address(iphDestIP)) + "]")
                #"] iphSrcIP: [" + str(iphSrcIP) + "] iphDestIP: [" + str(iphDestIP) + "]")
                icmpHeader = rec_packet[20:28]
                # icmpType (8), icmpCode (8), icmpChecksum (16), icmpPacketID (16), icmpSeqNumber (16)
                icmpType, icmpCode, icmpChecksum, icmpPacketID, icmpSeqNumber = struct.unpack("!BBHHH", icmpHeader)
                print ("icmpHeader: icmpType: ["+ str(icmpType) + "] icmpCode: [" + str(icmpCode) + "] icmpChecksum: [" + str(icmpChecksum) + \
                "] icmpPacketID: [" + str(icmpPacketID) + "] icmpSeqNumber: [" + str(icmpSeqNumber) + "]")

                #print("len: rec_packet: " + str(len(rec_packet)) + " ipHeader: " + str(len(ipHeader)) + " icmpHeader: " + str(len(icmpHeader)))
                #rec_data = rec_packet[28:48]
                #if curRoute.route['icmpreplay']:
                #    time.sleep(curRoute.route['icmptimeoutA'])
                #    replayPing(s, addr, icmpPacketID, icmpSeqNumber)
                #else:
                #    pass
                time.sleep( 0.5 )
                replayPing( elem, addr, icmpPacketID, icmpSeqNumber )

def replayPing(mySocket, destIP, myID, mySeqNumber):
    """
    Send one ping to the given >destIP<.
    """
    packet_size = 64

    #destIP  =  socket.gethostbyname(destIP)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    # (packet_size - 8) - Remove header size from packet size
    myChecksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack("!BBHHH", ICMP_ECHOREPLY, 0, myChecksum, myID, mySeqNumber)

    padBytes = []
    startVal = 0x42
    # 'cose of the string/byte changes in python 2/3 we have
    # to build the data differnely for different version
    # or it will make packets with unexpected size.
    if sys.version[:1] == '2':
        bytes = struct.calcsize("d")
        data = ((packet_size - 8) - bytes) * "Q"
        data = struct.pack("d", default_timer()) + data
    else:
        for i in range(startVal, startVal + (packet_size-8)):
            padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        #data = bytes(padBytes)
        data = bytearray(padBytes)

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data) # Checksum is in network order

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack("!BBHHH", ICMP_ECHOREPLY, 0, myChecksum, myID, mySeqNumber)

    packet = header + data

    while packet:
        print( " SENDING ... " )
        print( mySocket )
        print( destIP[0] )
        sent = mySocket.sendto(packet, (destIP[0], 1))
        packet = packet[sent:]
    print("packet sent")

    #try:
    #    #mySocket.sendto(packet, (destIP, 1)) # Port number is irrelevant for ICMP
    #    sent = mySocket.sendto(packet, (destIP[0], 1))
    #    print("packet sent")
    #except socket.error as e:
    #    print("General failure (%s)" % (e.args[1]))
    #    return

def create_packet(icmpPacketID, icmpSeqNumber, rec_data):
    """Create a new echo request packet based on the given "id"."""
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    header = struct.pack('bbHHh', ICMP_ECHOREPLY, 0, 0, icmpPacketID, icmpSeqNumber)
    data = str(rec_data) #48 * 'Q'
    my_checksum = checksum(str(header) + data)
    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    #Type (8), Code (8), Checksum (16), Identifier (16), Sequence Number (16), Data
    header = struct.pack('bbHHh', ICMP_ECHOREPLY , 0, socket.htons(my_checksum), icmpPacketID, icmpSeqNumber)
    return header + bytes(data,'utf-8')

def checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    countTo = (int(len(source_string)/2))*2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if (sys.byteorder == "little"):
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        try:     # For Python3
            sum = sum + (hiByte * 256 + loByte)
        except:  # For Python2
            sum = sum + (ord(hiByte) * 256 + ord(loByte))
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string): # Check for odd length
        loByte = source_string[len(source_string)-1]
        try:      # For Python3
            sum += loByte
        except:   # For Python2
            sum += ord(loByte)

    sum &= 0xffffffff # Truncate sum to 32 bits (a variance from ping.c, which
                      # uses signed ints, but overflow is unlikely in ping)

    sum = (sum >> 16) + (sum & 0xffff)    # Add high 16 bits to low 16 bits
    sum += (sum >> 16)                    # Add carry from above (if any)
    answer = ~sum & 0xffff                # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer

if __name__ == "__main__" :
    print( " START ... " )
    pingServer = PingServer()
    pingServer.start()

    while pingServer.systemOperative == True :
        time.sleep( 1 )

    print( " ... END " )

