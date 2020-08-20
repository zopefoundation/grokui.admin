import doctest
import re
import unittest
import grokui.admin

import zc.buildout.testing
from zope.testing import renormalizing
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer

checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])


def test_suite():
    suite = unittest.TestSuite()
    functional_layer = ZopeFanstaticBrowserLayer(grokui.admin.tests)
    optionflags = (doctest.ELLIPSIS +
                   doctest.NORMALIZE_WHITESPACE +
                   doctest.REPORT_NDIFF +
                   doctest.IGNORE_EXCEPTION_DETAIL
    )
    globs = dict(getRootFolder=functional_layer.getRootFolder)
    
    tests = [
        'apps',
        'brokenapps',
        'brokenobjs',
        'events',
        'infoviews',
        'packdatabase',
        'server']

    for filename in tests:
        test = doctest.DocTestSuite(
            'grokui.admin.tests.' + filename,
            checker=checker,
            globs=globs,
            optionflags=optionflags,
            )
        test.layer = functional_layer
        suite.addTest(test)

    security_test = doctest.DocTestSuite(
        'grokui.admin.tests.security',
        checker=checker,
        globs=globs,
        optionflags=optionflags,
        # In order to start a tiny http server in the test.
        setUp=zc.buildout.testing.buildoutSetUp,
        tearDown=zc.buildout.testing.buildoutTearDown)
    security_test.layer = functional_layer
    suite.addTest(security_test)
    return suite
