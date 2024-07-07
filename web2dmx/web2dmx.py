#!/usr/bin/python

#   web2dmx.py
#
#	by Claude Heintz
#	copyright 2024 by Claude Heintz Design
#
#  see license included with this distribution or
#  https://www.claudeheintzdesign.com/lx/opensource.html


#################################################################
#
#   This file contains the main interface for a simple web query to Art-Net application
#   
#   When you run this python file it creats an Art-Net sender and a HTTP server
#   
#   example use:
#   Use a  browser or curl to send a GET request to http://192.168.1.149:27688/?set=1x50
#       this sets the broadcast Art-Net sending to 192.168.1.255, address 1 to 50%
#   or, http://localhost:27688/?set=1x50_2x60
#       this sets both address 1 to 50% and address 2 to 60% with a single request
#       any number of addresses can be set with /?set=ADDRESSxPERCENT
#       with additional _ADDRESSxPERCENT pairs separated by underscores.
#   or, http://localhost:27688/?setl1x11_22_33_44_55
#      set list of sequential addresses starting at address
#         followed by x then list of values separated by underscores
#         setl=AxV1_V2_V3..., sets (A)@V1, (A+1)@V2, (A+2)@V3, etc
#         result of example, 1@11, 2@22, 3@33, 4@44, 5@55
#
#   Modify the Art-Net broadcast address (artip) to 10.255.255.255 for standard broadcast
#   Modify host name with specific ip address -or- 'localhost'
#   (localhost is only used for communicating  between apps on a single computer)
#
#################################################################

from http.server import HTTPServer
import time
from myQueryHandler import myQueryHandler
from ArtNet import ArtNetInterface

#########################################
#   hostname->local network interface address.
#   '0.0.0.0' listens on all available addresses.
#########################################
hostName = "0.0.0.0"
#########################################
#   port->port to use for web.
#      browser or curl url is IP_OF_COMPUTER:port/?...
#......generally ports <1000 are reserved and shouldn't be used
#########################################
serverPort = 27688
#########################################
#   artip->broadcast address for Art-Net.
#      depends on class of address
#......if ip network is is 10.n.n.n, broadcast is 10.255.255.255
#      if ip network is 192.168.1.n, broadcast is 192.168.1.255
#########################################
artip = "192.168.1.255"
#########################################

#################################################################
#
#   web2DMX handles communication between HTTP server and Art-Net.
#
#########################################
class web2DMX:
#########################################
#
#   setArtNet sets local variable for Art-Net interface object.
#
#########################################
    def setArtNet(self, iface):
        self.artnet = iface
#########################################
#
#   do_set sets address at value.
#      f ->HTTP output stream for writing
#      a-> dmx address (1 to 512)
#      v-> level  (0 to 100 percent)
#
#########################################
    def do_set(self, f, a, v):
        f.write(bytes("<p>Address %s at %s </p>" % (a, v), "utf-8"))
        d = int((float(v)/100.0) * 255.0)
        self.artnet.setDMXValue(int(a), d)



#################################################################
#
#   main program
#      creates Art-Net interface and starts it sending DMX.
#      creates web2dmx object for communicating between query handler and Art-Net.
#      creates HTTPServer with handler class, 'myQueryHandler'
#      starts webServer running waiting for a connection/request
#
#########################################

if __name__ == "__main__":

    iface = ArtNetInterface(artip)
    iface.startSending()
    
    web2dmx = web2DMX()
    web2dmx.setArtNet(iface)


    webServer = HTTPServer((hostName, serverPort), myQueryHandler)
    myQueryHandler.setOwner(web2dmx)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")