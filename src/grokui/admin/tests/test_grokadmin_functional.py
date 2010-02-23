# -*- coding: utf-8 -*-

import re
import unittest
import os.path

from pkg_resources import resource_listdir
from zope.testing import doctest, renormalizing
from zope.app.testing.functional import (
    HTTPCaller, getRootFolder, FunctionalTestSetup, sync, ZCMLLayer)


ftesting_zcml = os.path.join(
    os.path.dirname(__file__), 'ftesting.zcml')

GrokAdminFunctionalLayer = ZCMLLayer(
    ftesting_zcml, __name__, 'GrokAdminFunctionalLayer', allow_teardown=True)


def setUp(test):
    FunctionalTestSetup().setUp()


def tearDown(test):
    FunctionalTestSetup().tearDown()


checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])


def http_call(method, path, data=None, **kw):
    """Function to help make RESTful calls.

    method - HTTP method to use
    path - testbrowser style path
    data - (body) data to submit
    kw - any request parameters
    """

    if path.startswith('http://localhost'):
        path = path[len('http://localhost'):]
    request_string = '%s %s HTTP/1.1\n' % (method, path)
    for key, value in kw.items():
        request_string += '%s: %s\n' % (key, value)
    if data is not None:
        request_string += '\r\n'
        request_string += data
    return HTTPCaller()(request_string, handle_errors=False)


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
            dottedname, setUp=setUp, tearDown=tearDown,
            checker=checker,
            extraglobs=dict(http=HTTPCaller(),
                            http_call=http_call,
                            getRootFolder=getRootFolder,
                            sync=sync),
            optionflags=(doctest.ELLIPSIS +
                         doctest.NORMALIZE_WHITESPACE +
                         doctest.REPORT_NDIFF),
            )
        test.layer = GrokAdminFunctionalLayer

        suite.addTest(test)
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
