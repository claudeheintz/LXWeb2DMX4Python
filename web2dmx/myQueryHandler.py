#   myQueryHandler.py
#
#	by Claude Heintz
#	copyright 2024 by Claude Heintz Design
#
#  see license included with this distribution or
#  https://www.claudeheintzdesign.com/lx/opensource.html
#

from http.server import BaseHTTPRequestHandler

#################################################################
#
#   myQueryHandler extends BaseHTTPRequestHandler to handle GET requests
#      specifically get request urls of the form 'http://address:port/?query'
#      when a recognized query is received, passes it to class's 'owner' object.
#   
#   URL address:port/?setAxV  (example 10.110.111.4:/?set10x35, 10@35%)
#      sets address A at percentage V
#      multiple AxV pairs can be added, separated by underscores
#      (example example 10.110.111.4:/?set10x35_20x45, 10@35% and 20@45%)
#
#########################################
class myQueryHandler(BaseHTTPRequestHandler):
#########################################
#   setOwner->owner object to process results of query
#      owner is class variable
#      owner must respond to do_set( f(stream), a(address), v(value) )
#########################################
    @classmethod
    def setOwner(cls, owner):
        cls.owner = owner
#########################################
#
#   query->returns query portion of path or empty string
#      returns portion of url after ? as long as path is '/' 
#
#########################################
    def query(self):
        p = self.path.split("?")
        if (len(p) == 2):
            if ( p[0] == "/"):
                return p[1]
        return ""
#########################################
#
#   do_set_query->splits query on the right of 'set='into address value pairs
#      sends owner a do_set message for each 
#
#########################################
    def do_set_query(self, sv ):
        spts = sv.split("_")
        for sp in spts:
            scv = sp.split("x")
            if ( len(scv) == 2 ):
                self.owner.do_set( self.wfile, scv[0], scv[1])
#########################################
#
#   do_setl_query->splits query on the right of 'setl='
#      into address and value sequence, AxV1_V2_V3...
#      sends owner a do_set message for each 
#
#########################################
    def do_setl_query(self, sv ):
        spts = sv.split("x")
        if ( len(spts) == 2 ):
            addr = int(spts[0])
            varr = spts[1].split("_")
            for v in varr:
                self.owner.do_set( self.wfile, addr, v)
                addr = addr + 1
#########################################
#
#   do_QUERY processes query portion of url from a get request
#      does nothing if query is not handled
#
#########################################
    def do_QUERY(self):
        query = self.query()
        if ( query != ""):
            qpts = query.split("&")
            if (len(qpts) > 0):
                for q in qpts:
                    qt = q.split("=")
                    if ( len(qt) == 2):
                        if ( qt[0].lower() == "set"):
                            self.do_set_query(qt[1])
                        elif ( qt[0].lower() == "setl"):
                            self.do_setl_query(qt[1])
#########################################
#
#   override of do_GET
#      handles get requests
#      responds on http connection with 
#         html page listing actions taken in response to query
#
#########################################
    def do_GET(self):
        print("do get")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>pylx</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.do_QUERY()
        self.wfile.write(bytes("</body></html>", "utf-8"))
