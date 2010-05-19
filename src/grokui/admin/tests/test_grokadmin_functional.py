# -*- coding: utf-8 -*-

import doctest
import re
import unittest
import os.path
import grokui.admin

from pkg_resources import resource_listdir
from zope.testing import renormalizing
from zope.app.wsgi.testlayer import BrowserLayer

ftesting_zcml = os.path.join(
    os.path.dirname(__file__), 'ftesting.zcml')

FunctionalLayer = BrowserLayer(grokui.admin.tests, zcml_file=ftesting_zcml)

checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])


def test_suite():
    suite = unittest.TestSuite()
    files = resource_listdir(__name__, '')
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue
        if filename.startswith('test_'):
            continue

        dottedname = 'grokui.admin.tests.%s' % (filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            checker=checker,
            extraglobs=dict(getRootFolder=FunctionalLayer.getRootFolder),
            optionflags=(doctest.ELLIPSIS +
                         doctest.NORMALIZE_WHITESPACE +
                         doctest.REPORT_NDIFF),
            )
        test.layer = FunctionalLayer

        suite.addTest(test)
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
