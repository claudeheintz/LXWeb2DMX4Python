# LXWeb2DMX for Python

Simple web server and Art-Net broadcast application
Web server responds to get requests with a query string
which is interpreted to set levels of dmx addresses in
outgoing broadcast Art-Net

run web2dmx.py using python 3.x

example use:

Assume that the computer has an ip address of 10.110.115.49.

Use a browser or curl to send a GET request to `http://10.110.115.49:27688/?set=1x50`
  this sets address 1 to 50% in the packets being broadcast to Art-Net.
  
or, `http://10.110.115.49:27688/?set=1x50_2x60`
   this sets both address 1 to 50% and address 2 to 60% with a single request.
   Any number of addresses can be set with /?set=ADDRESSxPERCENT
   with additional _ADDRESSxPERCENT pairs separated by underscores.
   
or, `http://localhost:27688/?setl=1x11_22_33_44_55`
   sets list of sequential addresses starting at the provided address.
      An address followed by x then list of values separated by underscores
	  setl=AxV1_V2_V3..., sets (A)@V1, (A+1)@V2, (A+2)@V3, etc
	  result of example, 1@11%, 2@22%, 3@33%, 4@44%, 5@55%
	  
Addresses remain at established levels in dmx output until changed
by a later `set` or `setl` query

Options for the webserver and Art-Net broadcast can be set by the command line
or by editing the `web2dmx.properties` file.

The web server is set to listen for connections on any interface and port 27688.
Art-Net is broadcast to the network of the primary ip address found.

You can change and bind the web server to a particular interface of the computer
by providing the ip address of that interface as the first argument on the command
line, or by setting the `hostname` property in the `web2dmx.properties` file.
Likewise, the port can be specified by the second command line argument or
`server_port` in the properties file.  Finally, the address to send Art-Net to can be
set with a third command line argument or `artnet_broadcast_address`
in the properties file. 