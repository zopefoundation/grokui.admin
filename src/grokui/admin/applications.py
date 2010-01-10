# -*- coding: utf-8 -*-

import grok
from ZODB.broken import Broken
from zope.traversing.browser import absoluteURL
from zope.contentprovider.interfaces import IContentProvider
from zope.component import getMultiAdapter, getAllUtilitiesRegisteredFor
from grokui.base.layout import AdminView
from grokui.base.namespace import GrokUILayer
from grokui.base.interfaces import IInstallableApplication, \
                                   IInstalledApplication, \
                                   IApplicationRepresentation


grok.templatedir("templates")


from zope.annotation import IAnnotations
class InstalledApplication(object):
    """
    """
    grok.implements(IInstalledApplication)
   
    def __init__(self, obj, request):
        self.__name__ = obj.__name__
        grokui_info = IAnnotations(request).get('grokui')
        if not grokui_info:
            self.url = absoluteURL(obj, request)
        else:
            self.url = grokui_info.get('root_url')
        self.description = obj.__doc__
        self.__parent__ = obj.__parent__
        self.classname = ".".join((obj.__class__.__module__,
                                   obj.__class__.__name__))

    def __cmp__(self, a, b):
        return cmp(a.__name__, b.__name__)


class BrokenApplication(object):
    grok.implements(IApplicationRepresentation)

    def __init__(self, name, obj):
        self.__name__ = name
        self.classname = ".".join((obj.__class__.__module__,
                                   obj.__class__.__name__))

    def __cmp__(self, a, b):
        return cmp(a.__name__, b.__name__)


class InstallableApplication(object):
    grok.implements(IInstallableApplication)
    
    def __init__(self, klass):
        self.__name__ = klass.__name__
        self.classname = ".".join((klass.__module__, klass.__name__))
        self.description = unicode(klass.__doc__)

    
class ApplicationInfo(grok.View):
    grok.name('info')
    grok.context(IApplicationRepresentation)

    def render(self):
        info = getMultiAdapter(
            (self.context, self.request, self),
            IContentProvider,
            name='grokui_application_info')
        info.update()
        return info.render()


class Applications(AdminView):
    """View for application management.
    """
    grok.layer(GrokUILayer)
    grok.name('applications')
    grok.title('Applications')
    grok.require('grok.ManageApplications')

    def update(self):
        # Available apps...
        apps = getAllUtilitiesRegisteredFor(grok.interfaces.IApplication)
        self.installable = (InstallableApplication(x) for x in apps)

        # Installed apps...
        self.broken = []
        self.installed = []

        for name, app in self.context.root.items():
            is_broken = isinstance(app, Broken)
            if is_broken:
                self.broken.append(BrokenApplication(name, app))
            else:
                self.installed.append(InstalledApplication(app, self.request))

        self.broken.sort()
        self.installed.sort()
        self.has_apps = bool(len(self.installed) + len(self.broken))
