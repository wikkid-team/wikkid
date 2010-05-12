#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Utility methods for wikkid views."""

import re


WIKI_PAGE = re.compile('^([A-Z]+[a-z]*)+$')
WIKI_PAGE_ELEMENTS = re.compile('([A-Z][a-z]+)')


def expand_wiki_name(name):
    """A wiki name like 'FrontPage' is expanded to 'Front Page'.

    Names that don't match wiki names are unaltered.
    """
    if WIKI_PAGE.match(name):
        name_parts = [
            part for part in WIKI_PAGE_ELEMENTS.split(name) if part]
        return ' '.join(name_parts)
    else:
        return name


def title_for_filename(filename):
    """Generate a title based on the basename of the file object."""
    if filename.endswith('.txt'):
        return expand_wiki_name(filename[:-4])
    else:
        return expand_wiki_name(filename)
