#!/usr/bin/env python
#
#
#
"""
Froomi web media search engine, and pseudo streaming provider
    Copyright (C) 2009  David Busby http://saiweb.co.uk

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import ConfigParser,sys,os
class Froomi:
    
    def __init__(self):
        self.debug = False
        self.confd = ''
    
    def _loadCfg(self):
        cwd = os.path.realpath(os.path.dirname(__file__))
        cfgPath = "%s%s" % (cwd,'/conf/froomi.conf')

        cfg = ConfigParser.RawConfigParser()
        cfg.read(cfgPath)
        
        try:
            self.debug = cfg.getboolean('froomi', 'debug')
            self.confd = "%s%s" % (cwd,cfg.get('froomi','conf.d'))
            self.modules = "%s%s" %(cwd, cfg.get('froomi','modules'))
            sys.path.append(self.modules)
            return True
        except (ConfigParser.NoOptionError and ConfigParser.NoSectionError), e:
            print e
            return False
            
    def _loadHTTPD(self):
        import httpd
        cfgHTTPD = ConfigParser.RawConfigParser()
        cfgHTTPDpath = "%s/%s" % (self.confd,'httpd.conf')
        cfgHTTPD.read(cfgHTTPDpath)
        
        try:
            self.httpd_port = cfgHTTPD.getint('httpd','http_port')
            self.httpd = httpd
            return True
        except (ConfigParser.NoOptionError and ConfigParser.NoSectionError), e:
            print e
            return False
    
def main():
    x = Froomi()
    res  = x._loadCfg()
    if not res:
        sys.exit(1)
    res = x._loadHTTPD()
    if not res:
        sys.exit(1)
    x.httpd.HTTPD(x.httpd_port)
if __name__ == "__main__":
    main()