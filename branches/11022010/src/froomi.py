#!/usr/bin/env python
#
#
#
"""
Froomi web media search engine, and pseudo streaming provider
    Copyright (C) 2009  David Busby http://saiweb.co.uk
"""
import ConfigParser,sys,os
from time import time
class Froomi:
    
    def __init__(self):
        self.debug = False
        self.confd = ''
    
#===============================================================================
# This function sets up the module import paths, and attempts to import the mods
#===============================================================================
def loadmods():
    verbose('loadmods()')
    path = '%s/modules' % (sys.path[0])
    i = 0
    for mod in os.listdir(path):
        path = '%s/modules/%s' % (sys.path[0],mod)
        if mod != '.svn':
            if os.path.isdir(path):
                sys.path.append(path)
                try:
                    __import__(mod)
                except ImportError,e:
                    print 'Failed to import module',mod,'Error:',e
                    sys.exit(1)
                else:
                    i+=1
                    verbose('Loaded %s' % (mod))
    verbose('loadmods() complete %s module(s) loaded' % (i))
    
#===============================================================================
# verbose function
#===============================================================================
def verbose(str):
    if opts.verbose:
       print'%s: %s' % (time(),str)
#===============================================================================
# opts data subclass, used as a 'shared' store between threads
#===============================================================================
class opts:
    threads = []
    exit = False
    verbose = True
  
if __name__ == "__main__":
    loadmods()
    main()