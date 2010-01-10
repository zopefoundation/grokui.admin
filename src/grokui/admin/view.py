# -*- coding: utf-8 -*-
"""Views for the grok admin UI"""

import grok
import zope.component

from BTrees.OOBTree import OOBTree
from grokui.base import IGrokuiRealm
from grokui.base.layout import AdminView
from grokui.admin.interfaces import ISecurityNotifier
from grokui.admin.utilities import getVersion, getURLWithParams

from zope.site.interfaces import IRootFolder
from zope.exceptions import DuplicationError
  
grok.context(IGrokuiRealm)
grok.templatedir("templates")


class ManageApplications(grok.Permission):
    grok.name('grok.ManageApplications')


class GrokAdminInfoView(grok.View):
    """A base to provide machinereadable views.
    """
    grok.name('grokadmin')
    grok.require('grok.ManageApplications')
    
    def render(self):
        return u'go to @@version or @@secnotes'


class GrokAdminVersion(grok.View):
    """Display version of a package.

    Call this view via http://localhost:8080/@@grokadmin/@@version to
    get the used grok version. Call
    http://localhost:8080/@@grokadmin/@@version?pkg=<pkgname> to get
    the used version of package <pkgname>.
    """
    grok.name('version')
    grok.context(GrokAdminInfoView)
    grok.require('grok.ManageApplications')
    def render(self, pkg='grok'):
        return u'%s %s' % (pkg, getVersion(pkg))


class GrokAdminSecurityNotes(grok.View):
    """Display current security notification.

    Call this view via http://localhost:8080/@@grokadmin/@@secnote
    """
    grok.name('secnote')
    grok.context(GrokAdminInfoView)
    grok.require('grok.ManageApplications')
    def render(self):
        site = grok.getSite()
        site_manager = site.getSiteManager()
        notifier = site_manager.queryUtility(ISecurityNotifier, default=None)
        return notifier.getNotification()


class Add(grok.View):
    """Add an application.
    """
    grok.require('grok.ManageApplications')

    def update(self, inspectapp=None, application=None):
        if inspectapp is not None:
            self.redirect(self.url("docgrok") + "/%s/index"%(
                    application.replace('.','/'),))
        return

    def render(self, application, name, inspectapp=None):
        if name is None or name == "":
            self.redirect(self.url(self.context, 'applications'))
            return
        if name is None or name == "":
            self.redirect(self.url(self.context, 'applications'))
            return
        app = zope.component.getUtility(grok.interfaces.IApplication,
                                        name=application)
        try:
            new_app = app()
            grok.notify(grok.ObjectCreatedEvent(new_app))
            self.context.root[name] = new_app
            self.flash(u'Added %s `%s`.' % (application, name))
        except DuplicationError:
            self.flash(u'Name `%s` already in use. '
                       u'Please choose another name.' % (name,))
        self.redirect(self.url(self.context, 'applications'))


class ManageApps(grok.View):
    """Manage applications (delete, rename).
    """

    grok.require('grok.ManageApplications')

    def delete(self, items):
        """Delete applications in items.
        """
        msg = u''
        for name in items:
            try:
                del self.context.root[name]
                msg = (u'%sApplication `%s` was successfully '
                       u'deleted.\n' % (msg, name))
            except AttributeError:
                # Object is broken.. Try it the hard way...
                # TODO: Try to repair before deleting.
                obj = self.context.root[name]
                if not hasattr(self.context.root, 'data'):
                    msg = (
                        u'%sCould not delete application `%s`: no '
                        u'`data` attribute found.\n' % (msg, name))
                    continue
                if not isinstance(self.context.root.data, OOBTree):
                    msg = (
                        u'%sCould not delete application `%s`: no '
                        u'`data` is not a BTree.\n' % (msg, name))
                    continue
                self.context.root.data.pop(name)
                self.context.root.data._p_changed = True
                msg = (u'%sBroken application `%s` was successfully '
                       u'deleted.\n' % (msg, name))

        self.flash(msg)
        self.redirect(self.url(self.context, 'applications'))

    def render(self, rename=None, delete=None, items=None):

        if items is None:
            return self.redirect(self.url(self.context, 'applications'))

        if not isinstance(items, list):
            items = [items]

        if delete is not None:
            return self.delete(items)
        elif rename is not None:
            return self.redirect(getURLWithParams(
                    self.url(self.context, '@@grokadmin_rename'),
                    data=dict(items=items)))
        self.redirect(self.url(self.context, 'applications'))


class Rename(AdminView):
    """Rename Grok applications.
    """
    grok.name('grokadmin_rename')
    grok.template('rename')
    grok.require('grok.ManageApplications')

    def update(self, cancel=None, items=None, new_names=None):
        msg = u''

        if cancel is not None or not items:
            return self.redirect(self.url(self.context, 'applications'))

        if not isinstance(items, list):
            items = [items]
        self.apps = items

        if new_names is not None and len(new_names) != len(items):
            return self.redirect(self.url(self.context, 'applications'))

        if new_names is None:
            return

        mapping = dict([(items[x], new_names[x]) for x in range(len(items))])

        for oldname, newname in mapping.items():
            if oldname == newname:
                continue
            if oldname not in self.context.keys():
                self.flash('Could not rename %s: not found' % oldname)
                continue
            if newname in self.context.keys():
                self.flash('`%s` already exists.' % newname)
                continue
            self.context[newname] = self.context[oldname]
            self.context[newname].__name__ = newname
            del self.context[oldname]
            self.flash('Renamed `%s` to `%s`.' % (oldname, newname))
        self.redirect(self.url(self.context, 'applications'))
        return


class Index(grok.View):
    """A redirector to the real frontpage.
    """
    grok.name('index.html') # The root folder is not a grok.Model
    grok.require('grok.ManageApplications')
    grok.context(IRootFolder)

    def render(self):
        grokui_url = self.url(self.context) + '/++grokui++/applications'
        self.redirect(grokui_url)
