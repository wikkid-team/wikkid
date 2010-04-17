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

"""The skin is the outer look and feel of the wikkid wiki pages.

It is intended that the user will be able to use one of the pre-defined skins
(of which there is only the default right now) or provide a directory to their
own skin as a command line argument.
"""

import logging
import os.path

import bzrlib.urlutils as urlutils
from jinja2 import Environment, PackageLoader


class Skin(object):
    """A Wikkid wiki skin."""

    def __init__(self, skin_name=None):
        """Load the required templates."""
        # Need to load the initial templates for the skin.
        if skin_name is None:
            skin_name = 'default'
        self.logger = logging.getLogger('wikkid')
        # TODO: if we are using a user defined directory for the skin, here is
        # where we'd use a different loader.
        loader = PackageLoader('wikkid.skin', skin_name)
        self.env = Environment(loader=loader)
        self.templates = {
            'view_page': self.env.get_template('page.html'),
            'edit_page': self.env.get_template('edit.html'),
            'view_directory': self.env.get_template('page.html'),
            'missing': self.env.get_template('missing-page.html'),
            }
        module_location = urlutils.dirname(__file__)
        self.dir_name = urlutils.joinpath(module_location, skin_name)

    def get_template(self, template_name):
        return self.templates[template_name]

    @property
    def favicon(self):
        location = os.path.abspath(
            urlutils.joinpath(self.dir_name, 'favicon.ico'))
        if os.path.exists(location):
            return location
        else:
            return None

    @property
    def static_dir(self):
        location = os.path.abspath(
            urlutils.joinpath(self.dir_name, 'static'))
        if os.path.exists(location):
            return location
        else:
            return None
