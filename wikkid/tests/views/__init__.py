#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The wikkid tests for the wikkid.view package."""

import unittest


def test_suite():
    names = [
        'breadcrumbs',
        'utils',
        'edit',
        'root',
        'urls',
        'view',
        ]
    module_names = ['wikkid.tests.views.test_' + name for name in names]
    loader = unittest.TestLoader()
    return loader.loadTestsFromNames(module_names)
