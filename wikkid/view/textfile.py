#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of text pages."""

import logging

from twisted.web.util import redirectTo

from wikkid.errors import UpdateConflicts
from wikkid.interface.resource import ITextFile
from wikkid.view.base import BaseView
from wikkid.view.edit import BaseEditView


class EditTextFile(BaseEditView):
    """The page shows the text content in a large edit field."""

    for_interface = ITextFile

    @property
    def rev_id(self):
        return self.context.last_modified_in_revision

    @property
    def content(self):
        # We want to pass unicode to the view.
        byte_string = self.context.get_bytes()
        try:
            return byte_string.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return byte_string.decode('latin-1')
            except UnicodeDecodeError:
                return byte_string.decode('ascii', 'replace')


class SaveNewTextContent(BaseView):
    """Update the text of a file."""

    name = 'save'

    def _render(self, skin):
        """Save the text file.

        If it conflicts, render the edit, otherwise render the page (ideally
        redirect back to the plain page.
        """
        # TODO: barf if there is no user.
        content = self.request.args['content'][0]
        message = self.request.args['message'][0]
        if 'rev-id' in self.request.args:
            rev_id = self.request.args['rev-id'][0]
        else:
            rev_id = None
        try:
            self.context.put_bytes(
                content, self.user.committer_id, rev_id, message)

            return redirectTo(self.context.path, self.request)
        except UpdateConflicts, e:
            # Show the edit page again.
            logger = logging.getLogger('wikkid')
            logger.info('Conflicts detected: \n%r\n', e.content)
            self.template = 'edit_page'
            self.rev_id = e.basis_rev
            self.content = e.content
            self.message = "Conflicts detected during merge."
            self.cancel_url = self.context.preferred_path
            return super(SaveNewTextContent, self)._render(skin)


class UpdateTextFile(SaveNewTextContent):

    for_interface = ITextFile
