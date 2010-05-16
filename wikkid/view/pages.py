#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of the content."""

from twisted.web.util import redirectTo

from wikkid.errors import UpdateConflicts
from wikkid.formatter.pygmentsformatter import PygmentsFormatter
from wikkid.interface.resource import (
    IRootResource,
    ISourceTextFile,
    ITextFile,
    )
from wikkid.view.base import BaseView, DirectoryBreadcrumbView


class RootPage(BaseView):
    """The default view for the root page redirects to the home page."""

    for_interface = IRootResource
    name = 'view'
    is_default = True

    def _render(self, skin):
        """Redirect to Home (or the default page)."""
        preferred = self.context.preferred_path
        return redirectTo(preferred, self.request)


class OtherTextPage(DirectoryBreadcrumbView):
    """Any other non-binary file is considered other text.

    Will be rendered using pygments.
    """

    for_interface = ISourceTextFile
    name = 'view'
    is_default = True
    template = 'view_page'

    @property
    def content(self):
        formatter = PygmentsFormatter()
        return formatter.format(
            self.context.base_name, self.context.get_bytes())


class EditWikiPage(BaseView):
    """The page shows the wiki content in a large edit field."""

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
