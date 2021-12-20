#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the view dispatcher."""

from zope.interface import Interface, implementer

from wikkid.dispatcher import get_view, register_view, unregister_view
from wikkid.tests import TestCase
from wikkid.view.base import BaseView


class TestGetView(TestCase):
    """Tests for get_view."""

    def test_no_interfaces(self):
        """If the object supports no interfaces, there is no view."""
        class NoInterfaces(object):
            pass
        obj = NoInterfaces()
        self.assertIs(None, get_view(obj, None, None))

    def test_interface_not_registered(self):
        """If the object supports an interface, but that interface is not
        registered, we get no view."""
        class IHasInterface(Interface):
            pass

        @implementer(IHasInterface)
        class HasInterface(object):
            pass
        obj = HasInterface()
        self.assertIs(None, get_view(obj, None, None))

    def test_interface_view_registered(self):
        """If the object supports an interface, and the view is registered,
        make sure that the view is returned when asked for."""
        class IHasInterface(Interface):
            pass

        @implementer(IHasInterface)
        class HasInterface(object):
            pass

        class AView(object):
            for_interface = IHasInterface
            name = 'name'

            def __init__(self, *args):
                pass

            def initialize(self):
                self.initialized = True
        register_view(AView)
        self.addCleanup(unregister_view, AView)
        obj = HasInterface()
        view = get_view(obj, 'name', None)
        self.assertIsInstance(view, AView)
        self.assertTrue(view.initialized)

    def test_interface_view_registered_default(self):
        """If the object supports an interface, and the view is registered as
        the default view, when a view is requested where no name is specified,
        the default view is returned."""
        class IHasInterface(Interface):
            pass

        @implementer(IHasInterface)
        class HasInterface(object):
            pass

        class AView(object):
            for_interface = IHasInterface
            name = 'name'
            is_default = True

            def __init__(self, *args):
                pass

            def initialize(self):
                self.initialized = True
        register_view(AView)
        self.addCleanup(unregister_view, AView)
        obj = HasInterface()
        view = get_view(obj, None, None)
        self.assertIsInstance(view, AView)
        self.assertTrue(view.initialized)


class TestViewRegistration(TestCase):
    """Test that views that inherit from BaseView are registered."""

    def test_registration(self):
        """Create a view class, and make sure it is registered."""
        class IHasInterface(Interface):
            pass

        @implementer(IHasInterface)
        class HasInterface(object):
            pass

        class AView(BaseView):
            for_interface = IHasInterface
            name = 'name'
        obj = HasInterface()
        view = get_view(obj, 'name', None)
        self.assertIsInstance(view, AView)
        self.addCleanup(unregister_view, AView)
