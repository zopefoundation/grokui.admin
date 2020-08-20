"""
Information views
*****************

`grokui.admin` provides info views that can be fetched with `curl` or
similar tools to get a quick overview over the installation status.

They provide minimal information bits about for example the current
grok version and are provided for site administrators that want to
keep track of the site status via usual system administration tools.

We must have a browser available::

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()

We must be authenticated to fetch those infos::

  >>> browser.open('http://localhost/++grokui++/@@admin/@@version')
  Traceback (most recent call last):
  ...
  urllib.error.HTTPError: HTTP Error 401: Unauthorized

Getting the current grok version
--------------------------------

When we are authenticated, we can retrieve the grok version used::

  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/++grokui++/@@admin/@@version')
  >>> print(browser.contents)
  grok ...

The returned string has the format 'grok <MAJ>.<MIN>[.<BUGFIX>]' with
a major release number (<MAJ>), a minor release number (<MIN>) and an
oiptional bugfix release number like 'grok 0.14.1'::

  >>> import re
  >>> re.match(r'^grok \d+\.\d+(\.\d+)?.*$', browser.contents)
  <...Match object...>


Getting the version of any other installed package
--------------------------------------------------

If we want to determine the versions of packages, then we are not
restricted to the `grok` package. We can also ask for other packages
by passing a `pkg` parameter.

To determine the used version of `grokui.admin` we can call::

  >>> import pkg_resources
  >>> browser.open(
  ...   'http://localhost/++grokui++/@@admin/@@version?pkg=grokui.admin')
  >>> version = pkg_resources.get_distribution('grokui.admin').version
  >>> browser.contents == ('grokui.admin ' + version)
  True


Getting the current security notification
-----------------------------------------

We can get the current security notification::

  >>> browser.open('http://localhost/++grokui++/@@admin/@@secnote')
  >>> print(browser.contents)
  Security notifications are disabled.

"""
