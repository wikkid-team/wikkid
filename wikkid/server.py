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

"""The server class for the wiki."""

import logging

from wikkid.page import Page
from jinja2 import Environment, PackageLoader


class Server(object):
    """The Wikkid wiki server.
    """

    def __init__(self, filestore, user_factory, skin=None):
        """Construct the Wikkid Wiki server.

        :param filestore: An `IFileStore` instance.
        :param user_factory: A factory to create users.
        :param skin: A particular skin to use.
        """
        self.filestore = filestore
        self.user_factory = user_factory
        # Need to load the initial templates for the skin.
        if skin is None:
            skin = 'default'
        self.logger = logging.getLogger('wikkid')
        self.env = Environment(loader=PackageLoader('wikkid.skins', skin))
        self.page_template = self.env.get_template('page.html')
        self.edit_template = self.env.get_template('edit.html')
        self.missing_page_template = self.env.get_template('missing-page.html')

    def get_page(self, path):
        return Page(path, self.filestore.get_file(path))
