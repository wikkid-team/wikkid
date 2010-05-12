#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The formatter registry is able to return formatters by name."""

from wikkid.formatter.creoleformatter import CreoleFomatter
from wikkid.formatter.pygmentsformatter import PygmentsFormatter
from wikkid.formatter.restformatter import RestructuredTextFormatter


class FormatterRegistry(object):
    """Has a dictionary of formatters based on name."""

    def __init__(self):
        self._formatters = {
            'rest': RestructuredTextFormatter(),
            'creole': CreoleFomatter(),
            'pygments': PygmentsFormatter()
            }

    def __getitem__(self, formatter):
        return self._formatters[formatter]
