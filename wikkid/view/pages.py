#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of the content."""

from twisted.web.util import redirectTo

from wikkid.errors import UpdateConflicts
from wikkid.formatter.pygmentsformatter import PygmentsFormatter
from wikkid.formatter.restformatter import RestructuredTextFormatter
from wikkid.interface.resource import (
    IMissingResource,
    IRootResource,
    ISourceTextFile,
    ITextFile,
    IWikiTextFile,
    )
from wikkid.view.base import BaseView, DirectoryBreadcrumbView


class MissingPage(BaseView):
    """A wiki page that does not exist."""

    for_interface = IMissingResource
    name = 'view'
    is_default = True
    template = 'missing'

    @property
    def content(self):
        '%s Not found' % self.path


class RootPage(BaseView):
    """The default view for the root page redirects to the home page."""

    for_interface = IRootResource
    name = 'view'
    is_default = True

    def _render(self, skin):
        """Redirect to Home (or the default page)."""
        preferred = self.context.preferred_path
        return redirectTo(preferred, self.request)


class WikiPage(BaseView):
    """A wiki page is a page that is going to be rendered for viewing."""

    for_interface = IWikiTextFile
    name = 'view'
    is_default = True
    template = 'view_page'

    @property
    def content(self):
        bytes = self.context.get_bytes()
        # Check the first line of the content to see if it specifies a
        # formatter.

        # Format the content.  Right not this is hard coded to ReST, although
        # I want to offer multiple ways to do this.
        formatter = RestructuredTextFormatter()
        return formatter.format(
            self.context.base_name, bytes)

    def _render(self, skin):
        """If the page is not being viewed with the preferred path, redirect.

        For example, /FrontPage.txt will redirect to /FrontPage
        """
        preferred = self.context.preferred_path
        if self.context.path != preferred:
            return redirectTo(preferred, self.request)
        else:
            return super(WikiPage, self)._render(skin)


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


class NewWikiPage(BaseView):
    """Show the edit page with no existing content."""

    for_interface = IMissingResource
    name = 'edit'
    template = 'edit_page'

    @property
    def rev_id(self):
        return None

    @property
    def content(self):
        return ''


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


class SaveNewTextFile(SaveNewTextContent):

    for_interface = IMissingResource
    name = 'save'


class ConflictedEditWikiPage(BaseView):
    """The page shows the wiki content in a large edit field."""

    for_interface = ITextFile
    name = 'conflicted'
    template = 'edit_page'

    # TODO: fix this too...

    def __init__(self, skin, resource, path, user, conflict_text,
                 rev_id):
        BaseView.__init__(self, skin, resource, path, user)
        self.content = conflict_text
        self.rev_id = rev_id
