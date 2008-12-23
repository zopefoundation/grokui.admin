##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
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
"""Interfaces for the admin UI."""

from zope.interface import Interface
from zope.schema import TextLine, Bool

class ISecurityNotifier(Interface):
    """A notifier the looks up security warnings somewhere.
    """

    lookup_url = TextLine(
        title=u"Lookup URL",
        description=u"URL to use when doing lookups",
        required=True,
        default=u'http://grok.zope.org/releasinfo/'
        )
        
    enabled = Bool(
        title=u"Enabled",
        description=u"Notifier instance is enabled or disabled",
        required=True,
        default=False
        )
    
    def enable():
        """Enable security notifications.
        """

    def disable():
        """Disable security notifications.
        """

    def getNotification():
        """Get the current security notification.
        """

    def setLookupURL(url):
        """Set the url to lookup notifications.

        Beside HTTP all protocols supported by `urllib2` like
        ``file://`` should be supported.
        """
