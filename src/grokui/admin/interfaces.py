"""Interfaces for the admin UI.
"""

from zope.interface import Interface
from zope.schema import TextLine, Bool


class ISecurityNotifier(Interface):
    """A notifier the looks up security warnings somewhere.
    """

    lookup_url = TextLine(
        title="Lookup URL",
        description="URL to use when doing lookups",
        required=True,
        default='http://grok.zope.org/releasinfo/')

    enabled = Bool(
        title="Enabled",
        description="Notifier instance is enabled or disabled",
        required=True,
        default=False)

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
