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

"""Tests for the view dispatcher."""

from zope.interface import Interface, implements

from wikkid.tests import TestCase
from wikkid.view.base import BaseView
from wikkid.view.dispatcher import get_view, register_view


class TestGetView(TestCase):
    """Tests for get_view."""

    def test_no_interfaces(self):
        """If the object supports no interfaces, there is no view."""
        class NoInterfaces(object):
            pass
        obj = NoInterfaces()
        self.assertIs(None, get_view(obj, None))

    def test_interface_not_registered(self):
        """If the object supports an interface, but that interface is not
        registered, we get no view."""
        class IHasInterface(Interface):
            pass
        class HasInterface(object):
            implements(IHasInterface)
        obj = HasInterface()
        self.assertIs(None, get_view(obj, None))

    def test_interface_view_registered(self):
        """If the object supports an interface, and the view is registered,
        make sure that the view is returned when asked for."""
        class IHasInterface(Interface):
            pass
        class HasInterface(object):
            implements(IHasInterface)
        class AView(object):
            for_interface = IHasInterface
            name = 'name'
        register_view(AView)
        obj = HasInterface()
        self.assertIs(AView, get_view(obj, 'name'))

    def test_interface_view_registered_default(self):
        """If the object supports an interface, and the view is registered as
        the default view, when a view is requested where no name is specified,
        the default view is returned."""
        class IHasInterface(Interface):
            pass
        class HasInterface(object):
            implements(IHasInterface)
        class AView(object):
            for_interface = IHasInterface
            name = 'name'
            is_default = True
        register_view(AView)
        obj = HasInterface()
        self.assertIs(AView, get_view(obj, None))


class TestViewRegistration(TestCase):
    """Test that views that inherit from BaseView are registered."""

    def test_registration(self):
        """Create a view class, and make sure it is registered."""
        class IHasInterface(Interface):
            pass
        class HasInterface(object):
            implements(IHasInterface)
        class AView(BaseView):
            for_interface = IHasInterface
            name = 'name'
        obj = HasInterface()
        self.assertIs(AView, get_view(obj, 'name'))
