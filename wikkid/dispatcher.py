#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The dispatcher for wikkid views.

When this module is loaded, it will automagically load all the other views in
this directory.  The views inherit from the BaseView which has a metaclass
which registers the view with the dispatcher.
"""

import os

from breezy.urlutils import dirname, joinpath

from zope.interface import providedBy

from wikkid.context import ExecutionContext

# The view registry needs to map an Interface and a name to a class.
_VIEW_REGISTRY = {}


def get_view(obj, view_name, request, ec=ExecutionContext()):
    """Get the most relevant view for the object for the specified name.

    Iterate through the provided interfaces of the object and look in the view
    registry for a view.
    """
    interfaces = providedBy(obj)
    for interface in interfaces:
        try:
            klass = _VIEW_REGISTRY[(interface, view_name)]
            instance = klass(obj, request, ec)
            instance.initialize()
            return instance
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
    assert key not in _VIEW_REGISTRY, "key already registered: %r" % (key,)
    _VIEW_REGISTRY[key] = view_class
    if default_view:
        _VIEW_REGISTRY[(interface, None)] = view_class


def unregister_view(view_class):
    """Unregister the view."""
    interface = getattr(view_class, 'for_interface', None)
    view_name = getattr(view_class, 'name', None)
    default_view = getattr(view_class, 'is_default', False)

    if view_name is None or interface is None:
        # Don't register.
        return
    key = (interface, view_name)
    assert _VIEW_REGISTRY[key] is view_class, \
        "key registered with different class: %r: %r != %r" % (
            key, _VIEW_REGISTRY[key], view_class)
    del _VIEW_REGISTRY[key]
    if default_view:
        del _VIEW_REGISTRY[(interface, None)]


# We know that the controller (whatever that is going to end up being) will
# load this module to get the 'get_view' function.  None of the other view
# modules should be explicitly loaded anywhere else (possible exceptions may
# occur, so this isn't a hard rule).
#
# So... when this module is loaded, we want to load the other modules in the
# wikkid.view package so that when the classes are parsed, they register
# themselves with the view registry.

def load_view_modules():
    curr_dir = os.path.abspath(dirname(__file__))
    view_dir = joinpath(curr_dir, 'view')
    py_files = [
        filename for filename in os.listdir(view_dir)
        if filename.endswith('.py') and not filename.startswith('__')]
    for filename in py_files:
        __import__('wikkid.view.%s' % filename[:-3])


load_view_modules()
