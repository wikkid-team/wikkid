#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of the content."""

from wikkid.interface.resource import IMissingResource
from wikkid.view.base import BaseView
from wikkid.view.edit import BaseEditView
from wikkid.view.textfile import SaveNewTextContent


class MissingPage(BaseView):
    """A wiki page that does not exist."""

    for_interface = IMissingResource
    name = 'view'
    is_default = True
    template = 'missing'

    def make_response(self, body):
        response = super(BaseView, self).make_response(body)
        response.status = "404 Not Found"
        return response

    @property
    def content(self):
        '%s Not found' % self.path


class NewWikiPage(BaseEditView):
    """Show the edit page with no existing content."""

    for_interface = IMissingResource

    @property
    def rev_id(self):
        return None

    @property
    def content(self):
        return ''


class SaveNewTextFile(SaveNewTextContent):

    for_interface = IMissingResource
