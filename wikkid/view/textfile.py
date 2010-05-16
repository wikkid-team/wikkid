#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of text pages."""

from twisted.web.util import redirectTo

from wikkid.errors import UpdateConflicts
from wikkid.interface.resource import ITextFile
from wikkid.view.base import BaseView


class EditTextFile(BaseView):
    """The page shows the text content in a large edit field."""

    for_interface = ITextFile
    name = 'edit'
    template = 'edit_page'

    @property
    def rev_id(self):
        return self.context.last_modified_in_revision

    @property
    def content(self):
        return self.context.get_bytes()


class SaveNewTextContent(BaseView):
    """Update the text of a file."""

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
        except UpdateConflicts:
            # TODO: fix this
            assert False, "add conflict handling"


class UpdateTextFile(SaveNewTextContent):

    for_interface = ITextFile
    name = 'save'
