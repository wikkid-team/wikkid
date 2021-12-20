#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of text pages."""

import logging

from webob.exc import HTTPSeeOther

from wikkid.filestore import UpdateConflicts
from wikkid.interface.resource import ITextFile
from wikkid.view.edit import BaseEditView
from wikkid.view.wiki import format_content


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


class SaveNewTextContent(BaseEditView):
    """Update the text of a file."""

    name = 'save'

    def _render(self, skin):
        """Save the text file.

        If it conflicts, render the edit, otherwise render the page (ideally
        redirect back to the plain page.
        """
        # TODO: barf on a GET
        # TODO: barf if there is no user.
        params = self.request.params
        content = params['content']
        description = params['description']
        rev_id = (
            params['rev-id'].encode('utf-8') if 'rev-id' in params else None)
        preview = params.get('preview', None)
        if preview is not None:
            self.rev_id = rev_id
            self.description = description
            self.content = content
            default_format = self.execution_context.default_format
            self.preview_content = format_content(
                content, self.context.base_name, default_format)
        else:
            try:
                self.context.put_bytes(
                    content.encode('utf-8'), self.user.committer_id, rev_id,
                    description)

                location = self.canonical_url(self.context)
                raise HTTPSeeOther(location=location)
            except UpdateConflicts as e:
                # Show the edit page again.
                logger = logging.getLogger('wikkid')
                logger.info('Conflicts detected: \n%r\n', e.content)
                self.rev_id = e.basis_rev
                self.content = e.content
                self.message = "Conflicts detected during merge."

        self.description = description
        return super(SaveNewTextContent, self)._render(skin)


class UpdateTextFile(SaveNewTextContent):

    for_interface = ITextFile
