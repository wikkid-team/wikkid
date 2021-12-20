#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View URL functions."""

import re


VIEW_MATCHER = re.compile(r'^(.*)/\+(\w+)$')


def parse_url(path):
    """Convert a path into a resource path and a view."""
    match = VIEW_MATCHER.match(path)
    if match is not None:
        resource_path, view = match.groups()
        if resource_path == '':
            resource_path = '/'
        return (resource_path, view)
    else:
        return (path, None)


def canonical_url(context, request, view=None):
    """The one true URL for the context object."""
    path = context.preferred_path
    if view is None:
        return '{0}{1}'.format(request.script_name, path)
    else:
        if path == '/':
            path = ''
        return '{0}{1}/+{2}'.format(request.script_name, path, view)
