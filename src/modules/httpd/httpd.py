#!/usr/bin/env python
#
#
#
"""
Froomi web media search engine, and pseudo streaming provider
    Copyright (C) 2009  David Busby http://saiweb.co.uk
"""

"""
Froomi HTTP Server component
Also support pseudo streaming of media

"""
import cStringIO
import string, cgi, time, gzip, urlparse, urllib, decimal
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class HTTPDHandler(BaseHTTPRequestHandler):
    
    HTTP_OK = 200
    HTTP_NOTFOUND = 404
    HTTP_INTERNALERROR = 500
    HTTP_FORBIDDEN = 403
    
    PSEUDO_FILE = 'file'
    PSEUDO_POS = 'position'
    PSEUDO_KEY = 'key'
    PSEUDO_BW = 'bw'
    
    gzip = False
    
    # ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
    #--------------------------------- params='', query='', fragment='')

        
    def _setup(self):
        self.url = urlparse.urlparse(self.path)
        self.URI = self.url[2]
        self.get_params = dict([part.split('=') for part in self.url[4].split('&')])
        #cleanup the data
        for key in self.get_params:
            self.get_params[key] = urllib.unquote_plus(self.get_params[key])
    
    def do_GET(self):
        self._setup()
        #------------------------------------------------------------- client ip
        #------------------------------------------------ self.client_address[0]
        #----------------------------------------------------------- client port
        #------------------------------------------------ self.client_address[1]
        
        if self.URI.endswith('.html'):
            self.send_response(self.HTTP_OK)
            self.send_header('Content-type','text/html')
            self._checkEncoding()
            str = """
            This is my froomi, there are not many like it and this one is ALL MINE <br />
            The quick brown fox, jumped over the lazy dog <br />
            Now is the time for all good men, to come to the aid of the party <br />
            """
            for key in self.get_params:
                str = '%s%s: %s<br />\n' % (str,key,self.get_params[key])
            self._Send(str)
            
        elif self.URI.endswith('.froomi'):
            self.send_response(self.HTTP_OK)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write('FROOMI Content here')
        elif self.URI.endswith('.mp4') or self.path.endswith('.flv'):
            self.send_response(self.HTTP_OK)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write('MEDIA Content here')
        return
       
    def do_POST(self):
        print self
    
    def _checkEncoding(self):
        if self.headers.has_key('accept-encoding'):
            encodings = self.headers['accept-encoding']
            if(string.find(encodings,'gzip') != -1):
                self.gzip = True
    
    def _compressBuff(self,buff):
        zbuf = cStringIO.StringIO()
        zfile = gzip.GzipFile(mode = 'wb', fileobj = zbuf, compresslevel = 6)
        zfile.write(buff)
        zfile.close()
        return zbuf.getvalue()
         
    def _Send(self,content):
        if self.gzip == True:
            self.send_header('Content-Encoding', 'gzip')
            uncom = len(content)
            content = self._compressBuff(content)
            com = len(content)
            self.send_header('Content-Length', com)
            
            decimal.getcontext().prec = 2
            compression_per = 100-(decimal.Decimal(com)/decimal.Decimal(uncom))*decimal.Decimal(100)
            
            print 'Compression %s/%s [%d%%]' %(com,uncom,compression_per)
            
            
        self.end_headers()
        self.wfile.write(content)
            

class HTTPD:
    def __init__(self,port):
        try:
            BaseHTTPRequestHandler.server_version = 'Froomi/0.1'
            self.server = HTTPServer(('',port), HTTPDHandler)
            print "HTTPD Started..."
            self.server.serve_forever()
        except KeyboardInterrupt:
            print "^C Recevied shutting down"
            self.server.socket.close()
    
            