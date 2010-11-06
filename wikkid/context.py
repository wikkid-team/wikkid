# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A means of storing execution context."""


class ExecutionContext(object):
    """Store run-time execution context data in the executionContext class,
    such as command-line options and settings.
    
    To use this class, create an instance of it, and either set key,value
    pairs just like you would a dictionary, or call add_context(dict), 
    passing in a dictionary of name,value pairs that you want to _append_
    to the execution context."""
    __options = {}
    
    def __getitem__(self, name):
        return self.__options[name]
    def __setitem__(self, name, value):
        self.__options[name] = value
    def __iter__(self):
        return iter(self.__options)
    def __contains__(self, name):
        return name in self.__options
        
    def add_context(self, contextDict):
        if type(contextDict) is not dict:
            raise TypeError, "Context must be a dictionary type."
        self.__options.update(contextDict)
        
    def get(self, name, default):
        return self.__options.get(name, default)