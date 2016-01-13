# -*- coding: utf-8 -*-

from zope import schema
from zope.location import ILocation
from zope.interface import Interface
from zope.configuration.fields import PythonIdentifier
from zope.contentprovider.interfaces import IContentProvider


class IApplicationRepresentation(Interface):
    """Defines an Grok application
    """
    __name__ = schema.TextLine(
        title=u"Name",
        required=True)

    classname = PythonIdentifier(
        title=u"Dotted name of the Application class",
        required=True)

    description = schema.Text(
        title=u"Description of the Application",
        default=u"",
        required=False)


class IInstallableApplication(IApplicationRepresentation):
    """Defines an installable application.
    """


class IInstalledApplication(IApplicationRepresentation, ILocation):
    """Defines an application that is installed in our system.
    """
    url = schema.URI(
        title=u"Absolute URL of the application",
        required=True)


class IApplicationInformation(IContentProvider):
    """Marker interface for the Application information content provider.
    """
