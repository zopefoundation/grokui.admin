##############################################################################
#
# Copyright (c) 2009 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
If we are not authenticated, we will be redirected to a login form::

    >>> print http(r'''
    ... GET / HTTP/1.1
    ... ''')
    HTTP/1.1 303 See Other
    Content-Length: 0
    Content-Type: text/plain
    Location: login.html?nextURL=http://localhost/index.html

If we are authenticated, then we will be redirected to the
applications overview page::

    >>> print http(r'''
    ... GET / HTTP/1.1
    ... Authorization: Basic mgr:mgrpw
    ... ''')
    HTTP/1.1 303 See Other
    Content-Length: 0
    Content-Type: text/plain
    Location: http://localhost/applications

"""
