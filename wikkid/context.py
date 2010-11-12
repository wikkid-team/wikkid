# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A means of storing execution context."""


class ExecutionContext(dict):
    """Store run-time execution context data.
     
    To use this class, create an instance of it, and either set key,value
    pairs just like you would a dictionary, or call add_context(dict), 
    passing in a dictionary of name,value pairs that you want to _append_
    to the execution context.
    
    To retrieve values, you can either use the classic dictionary methods, 
    or access options as attribute. So, this:
    
    ec['someOption']
    
    is equivilent to this:
    
    ec.someOption
    """
        
    def add_context(self, contextDict):
        if type(contextDict) is not dict:
            raise TypeError, "Context must be a dictionary type."
        self.update(contextDict)
        
    def __getattr__(self, name):
        if self.has_key(name):
            return self[name]
        else:
            raise AttributeError, "ExecutionContext instance has no attribute '%s'" % (name)
        
    def __setattr__(self, name, value):
        self[name] = value
        
        
