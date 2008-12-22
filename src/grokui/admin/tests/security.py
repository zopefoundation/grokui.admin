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

  >>> sn.getNotification()
  u'Security notifications are disabled.'

Even an explicit lookup request will not do lookups, while the
notifier is not enabled::

  >>> sn.updateMessage()
  >>> sn.getNotification()
  u'Security notifications are disabled.'


Where to look for notifications
-------------------------------

When we want to do real lookups, then by default the Grok site is
asked::

  >>> sn.lookup_url
  'http://grok.zope.org/releaseinfo/'

But we can change the place to look for security warnings. We prepared
a local directory with some warnings, which we will use as our
information source::

  >>> import os.path
  >>> fake_source = os.path.join(os.path.dirname(__file__), 'releaseinfo')
  >>> fake_source_url = 'file://%s' % fake_source + os.path.sep
  >>> sn.lookup_url = fake_source_url

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
  >>> note
  u''

Ah, there is no security warning for our version. So let us create
one::

  >>> from grokui.admin.utilities import getGrokVersion
  >>> version = getGrokVersion()
  >>> fake_warning_file = 'grok-%s.security.txt' % version
  >>> fake_warning_file = os.path.join(fake_source, fake_warning_file)
  >>> open(fake_warning_file, 'w').write('You better smash %s' % version)

When we now ask the security notifier again::

  >>> sn.getNotification()
  u''

We got the same answer as before. Why? The lookups are done only in
certain intervals to reduce the amount of outgoing traffic. When we
fix the lookup timestamp, we get the real value::

  >>> sn.last_lookup = None
  >>> sn.getNotification()
  'You better smash ...'

Clean up::

  >>> import os
  >>> os.unlink(fake_warning_file)

  
`SecurityNotifier` in `grokui.admin`
====================================

In `grokui.admin` the security notifier is installed at startup as
local utility, that can be looked up by the `ISecurityNotifer`
interface.

Currently, as `grokui.admin` is merely a collection of views bound to
root folders, also the security notification utility is normally
managed by the local site manager of the root folder::

  >>> root = getRootFolder()
  >>> sm = root.getSiteManager()

Now we can lookup the utility::

  >>> from grokui.admin.interfaces import ISecurityNotifier
  >>> notifier = sm.getUtility(ISecurityNotifier)
  >>> notifier
  <grokui.admin.security.SecurityNotifier object at 0x...>

The utility is local, because different root folders might want
different settings for security notifications.

The utility is persistent, so that the settings are preserved when
shutting down.

Immediately after startup, the notifier exists, but is disabled::

  >>> notifier.enabled
  False

We can get notifications, of course::

  >>> notifier.getNotification()
  u'Security notifications are disabled.'

We can check in a formal way, whether the current notification is a
warning::

  >>> notifier.isWarning()
  False
  
"""
