# LXWeb2DMX for Python

Simple web server and Art-Net broadcast application
Web server responds to get requests with a query setting levels of dmx addresses
Sets those address/levels in outgoing broadcast Art-Net

run web2dmx.py using python 3.x

example use:

Use a  browser or curl to send a GET request to http://192.168.1.149:27688/?set=1x50
  this sets the sending broadcast Art-Net to 192.168.1.255, with address 1 to 50%
  
or, http://localhost:27688/?set=1x50_2x60
   this sets both address 1 to 50% and address 2 to 60% with a single request
   any number of addresses can be set with /?set=ADDRESSxPERCENT
   with additional _ADDRESSxPERCENT pairs separated by underscores.
   
or, http://localhost:27688/?setl1x11_22_33_44_55
   set list of sequential addresses starting at address
      followed by x then list of values separated by underscores
	  setl=AxV1_V2_V3..., sets (A)@V1, (A+1)@V2, (A+2)@V3, etc
	  result of example, 1@11, 2@22, 3@33, 4@44, 5@55
	  
addresses remain at established levels in dmx output until changed by a later set or setl query