"""
Tests for security notifications.

The `SecurityNotifier`
======================

A security notifier is an object that checks an URL for security
warnings and delivers them. It keeps track of lookup-dates etc., so
that lookups are not performed too often.

Because this is a 'calling-home' feature, it is disabled by
default. SecurityNotifiers know about their status (enabled or
disabled) and do no lookups when disabled.

Security notifications are handled by a `SecurityNotifier`::

  >>> from grokui.admin.security import SecurityNotifier
  >>> sn = SecurityNotifier()

Instances provide the `ISecurityNotifier` interface.

  >>> from grokui.admin.interfaces import ISecurityNotifier
  >>> ISecurityNotifier.providedBy(sn)
  True


Enabling and disabling the notifier
-----------------------------------

By default a security notifier is not enabled::

  >>> sn.enabled
  False

We enable it::

  >>> sn.enable()
  >>> sn.enabled
  True

and disable again::

  >>> sn.disable()
  >>> sn.enabled
  False

While being disabled, the notifier will do no lookups, even if
`updateMessage` or similar methods are called.

Getting notifications
---------------------

We can get a notification, of course. Asking for that will not trigger
a lookup, while the notifier is disabled::

  >>> assert sn.getNotification() == 'Security notifications are disabled.'

Even an explicit lookup request will not do lookups, while the
notifier is not enabled::

  >>> sn.updateMessage()
  >>> assert sn.getNotification() == 'Security notifications are disabled.'


Where to look for notifications
-------------------------------

When we want to do real lookups, then by default the Grok site is
asked::

  >>> sn.lookup_url
  'http://grok.zope.org/releaseinfo/'

But we can change the place to look for security warnings. We prepared
a local directory with some warnings, which we will use as our
information source::

  >>> import tempfile
  >>> release_info_tmpdir = tempfile.mkdtemp()
  >>> release_info_server = start_server(release_info_tmpdir)
  >>> sn.setLookupURL(release_info_server)

Now we can safely enable the notifier and see, whether there are infos
for us. It is sufficient to call `getNotification()` as this will
update the stored information automatically.

Before we really start, we will have a look at the lookup timestamp,
that stores our last tries::

  >>> last_lookup = sn.last_lookup
  >>> last_lookup is None
  True

  >>> sn.enable()
  >>> note = sn.getNotification()
  >>> assert note == u''

Ah, there is no security warning for our version. So let us create
one::

  >>> from grokui.admin.utilities import getVersion
  >>> version = getVersion('grok')
  >>> import os.path
  >>> fake_warning_file = 'grok-%s.security.txt' % version
  >>> fake_warning_file = os.path.join(release_info_tmpdir, fake_warning_file)
  >>> with open(fake_warning_file, 'w') as fd:
  ...     _ = fd.write('You better smash %s' % version)


When we now ask the security notifier again::

  >>> assert sn.getNotification() == ''

We got the same answer as before. Why? The lookups are done only in
certain intervals to reduce the amount of outgoing traffic. When we
fix the lookup timestamp, we get the real value::

  >>> sn.last_lookup = None
  >>> assert sn.getNotification() == u'You better smash 3.1'   

To decide, whether the delivered string is actually a warning, we can
call the `isWarning` method::

  >>> sn.isWarning()
  True


`SecurityNotifier` in `grokui.admin`
====================================

In `grokui.admin` the security notifier is installed at startup as
local utility, that can be looked up by the `ISecurityNotifer`
interface.

Currently, as `grokui.admin` is merely a collection of views bound to
root folders, also the security notification utility is normally
managed by the local site manager of the root folder.

The utility is local, because different root folders might want
different settings for security notifications.

The utility is persistent, so that the settings are preserved when
shutting down.

Immediately after startup, the notifier doesn't exists::

  >>> from grokui.admin.interfaces import ISecurityNotifier

  >>> root = getRootFolder()
  >>> sm = root.getSiteManager()
  >>> notifier = sm.queryUtility(ISecurityNotifier)
  >>> notifier is None
  True

We log into the admin screen to set a new notifier URL::

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/++grokui++/@@server')

On the server administration page we can see the status of our
notifier (enabled or disabled)::

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ... Status: Security notifications are disabled
  ...

We can also see the current message which also informs us, if security
notifications are disabled. This message is displayed on (nearly)
every `grokui.admin` page::

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...<div id="grokui-messages"><div class="grokui-security message">Security notifications are disabled.</div>
  ...

But we are not bound to the default URL to do lookups. We can set
another one ourselves::

  >>> browser.getControl(name='secnotesource').value=release_info_server
  >>> browser.getControl('Set URL').click()

Now, as we set a lookup URL which we can control better, we can enable
the security notifications::

  >>> browser.getControl('Enable').click()

The result of the lookup again is displayed. This time we get a 'real'
result::

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...<div id="grokui-messages"><div class="grokui-security message">You better smash ...</div>
  ...

We can of course disable security notifications at any time::

  >>> browser.getControl('Disable').click()
  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...<div id="grokui-messages"><div class="grokui-security message">Security notifications are disabled.</div>
  ...


Clean up::

  >>> import os
  >>> os.unlink(fake_warning_file)

"""
