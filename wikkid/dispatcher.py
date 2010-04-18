#
# Copyright (C) 2010 Wikkid Developers
#
# This file is part of Wikkid.
#
# Wikkid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wikkid.  If not, see <http://www.gnu.org/licenses/>

"""The dispatcher for wikkid views.

When this module is loaded, it will automagically load all the other views in
this directory.  The views inherit from the BaseView which has a metaclass
which registers the view with the dispatcher.
"""

import os

from bzrlib.urlutils import dirname, joinpath

from zope.interface import providedBy


# The view registry needs to map an Interface and a name to a class.
_VIEW_REGISTRY = {}


def get_view(obj, view_name):
    """Get the most relevant view for the object for the specified name.

    Iterate through the provided interfaces of the object and look in the view
    registry for a view.
    """
    interfaces = providedBy(obj)
    for interface in interfaces:
        try:
            return _VIEW_REGISTRY[(interface, view_name)]
        except KeyError:
            pass
    # For example, if someone asked for 'raw' view on a directory or binary
    # object.
    return None


def register_view(view_class):
    """Register the view."""
    interface = getattr(view_class, 'for_interface', None)
    view_name = getattr(view_class, 'name', None)
    default_view = getattr(view_class, 'is_default', False)

    if view_name is None or interface is None:
        # Don't register.
        return
    key = (interface, view_name)
    assert key not in _VIEW_REGISTRY, "key already registered: %r" % key
    _VIEW_REGISTRY[key] = view_class
    if default_view:
        _VIEW_REGISTRY[(interface, None)] = view_class


# We know that the controller (whatever that is going to end up being) will
# load this module to get the 'get_view' function.  None of the other view
# modules should be explicitly loaded anywhere else (possible exceptions may
# occur, so this isn't a hard rule).
#
# So... when this module is loaded, we want to load the other modules in the
# wikkid.view package so that when the classes are parsed, they register
# themselves with the view registry.

def _load_view_modules():
    curr_dir = os.path.abspath(dirname(__file__))
    view_dir = joinpath(curr_dir, 'view')
    py_files = [
        filename for filename in os.listdir(view_dir)
        if filename.endswith('.py') and not filename.startswith('__')]
    for filename in py_files:
        __import__('wikkid.view.%s' % filename[:-3])

_load_view_modules()
