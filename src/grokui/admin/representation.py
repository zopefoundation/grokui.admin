from zope import schema
from zope.configuration.fields import PythonIdentifier
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface
from zope.location import ILocation


class IApplicationRepresentation(Interface):
    """Defines an Grok application
    """
    __name__ = schema.TextLine(
        title="Name",
        required=True)

    classname = PythonIdentifier(
        title="Dotted name of the Application class",
        required=True)

    description = schema.Text(
        title="Description of the Application",
        default="",
        required=False)


class IInstallableApplication(IApplicationRepresentation):
    """Defines an installable application.
    """


class IInstalledApplication(IApplicationRepresentation, ILocation):
    """Defines an application that is installed in our system.
    """
    url = schema.URI(
        title="Absolute URL of the application",
        required=True)


class IApplicationInformation(IContentProvider):
    """Marker interface for the Application information content provider.
    """
