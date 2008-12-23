##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
Information views
*****************

`grokui.admin` provides info views that can be fetched with `curl` or
similar tools to get a quick overview over the installation status.

They provide minimal information bits about for example the current
grok version and are provided for site administrators that want to
keep track of the site status via usual system administration tools.

We must have a browser available::

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()

We must be authenticated to fetch those infos::

  >>> browser.open('http://localhost/@@grokadmin/@@version')
  Traceback (most recent call last):
  ...
  HTTPError: HTTP Error 401: Unauthorized

Getting the current grok version
--------------------------------
  
When we are authenticated, we can retrieve the grok version used::
  
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/@@grokadmin/@@version')
  >>> print browser.contents
  grok ...

The returned string has the format 'grok <MAJ>.<MIN>[.<BUGFIX>]' with
a major release number (<MAJ>), a minor release number (<MIN>) and an
oiptional bugfix release number like 'grok 0.14.1'::

  >>> import re
  >>> re.match('^grok \d+\.\d+(\.\d+)?.*$', browser.contents)
  <_sre.SRE_Match object at 0x...>

Getting the current security notification
-----------------------------------------

We can get the current security notification::

  >>> browser.open('http://localhost/@@grokadmin/@@secnote')
  >>> print browser.contents
  Security notifications are disabled.

"""
