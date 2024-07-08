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
#           curl -X GET http://192.168.1.149:27688/?set=1x50
#       this sets the broadcast Art-Net sending to 192.168.1.255, address 1 to 50%
#
#   or, http://localhost:27688/?set=1x50_2x60
#           curl -X GET  http://localhost:27688/?set=1x50_2x60
#       this sets both address 1 to 50% and address 2 to 60% with a single request
#       any number of addresses can be set with /?set=ADDRESSxPERCENT
#       with additional _ADDRESSxPERCENT pairs separated by underscores.
#
#   or, http://localhost:27688/?setl=1x11_22_33_44_55
#           curl -X GET  http://localhost:27688/?setl=1x11_22_33_44_55
#      set list of sequential addresses starting at address
#         followed by x then list of values separated by underscores
#         setl=AxV1_V2_V3..., sets (A)@V1, (A+1)@V2, (A+2)@V3, etc
#         result of example, 1@11, 2@22, 3@33, 4@44, 5@55

#
#   Edit web2dmx properties file to make the following changes:
#      Modify the Art-Net broadcast address (artip) to 10.255.255.255 for standard broadcast
#      Modify host name with specific ip address -or- 'localhost'
#         (localhost is only used for communicating  between apps on a single computer)
#
#################################################################

from http.server import HTTPServer
from myQueryHandler import myQueryHandler
from ArtNet import ArtNetInterface
from CTProperties import CTProperties
import time
import os

#######################   web2dmx class    ######################
#################################################################
#
#   web2DMX handles communication between HTTP server and Art-Net.
#
#########################################
class web2DMX:

#########################################
#
#   init properties dictionary of application options
#   from web2dmx.properties file.  Edit to change:
#      Art-Net broadcast address
#      hostname of network interface to use
#      port for web server to use
#
#########################################
    def __init__(self):
        #get properties from file named web2dmx.properties
        self.properties = CTProperties()
        cpath = os.path.realpath(__file__)
        self.appdirectory = os.path.dirname(cpath)
        self.properties.parseFile( self.appdirectory + "/web2dmx.properties")
        #read application options
        self.artip = self.properties.stringForKey("artnet_broadcast_address", "10.255.255.255")
        self.hostname = self.properties.stringForKey("hostname", "0.0.0.0")
        self.serverport = self.properties.intForKey("server_port", 27688)

#########################################
#
#   createArtNet makes Art-Net sender and starts it sending
#
#########################################
    def createArtNet(self):
        self.artnet_interface = ArtNetInterface(self.artip)
        self.artnet_interface.startSending()

#########################################
#
#   createWebServer makes web server object
#   uses myQueryHandler class to parse received query portion of urls
#   myQueryHandler calls back to its owner with do_set messages
#
#########################################
    def createWebServer(self):
        self.web_server = HTTPServer((self.hostname, self.serverport), myQueryHandler)
        myQueryHandler.setOwner(self)

#########################################
#
#   runWebServer
#      serve_forever BLOCKS until KeyboardInterrupt throws an exception
#
#########################################
    def runWebServer(self):
        print("Starting web server http://%s:%s" % (self.hostname, self.serverport))
        try:
            self.web_server.serve_forever()
        except KeyboardInterrupt:
            pass

#########################################
#
#   closeWebServer
#
#########################################
    def closeWebServer(self):
        self.web_server.server_close()
        print("Web server stopped.")

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
        self.artnet_interface.setDMXValue(int(a), d)

####################### end web2dmx class #######################
#################################################################

#################################################################
#######################   main program    #######################
#
#      creates web2dmx object for communicating between webserver and Art-Net.
#      creates Art-Net interface and starts it sending DMX.
#      creates HTTPServer with handler class, 'myQueryHandler'
#         (myQueryHandler calls back to web2dmx with do_set messages)
#      starts webServer running waiting for a connection/request
#
#########################################

if __name__ == "__main__":

    web2dmx = web2DMX()
    web2dmx.createArtNet()
    web2dmx.createWebServer()

    web2dmx.runWebServer()
    web2dmx.closeWebServer()