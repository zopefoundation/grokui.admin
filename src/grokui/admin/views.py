# -*- coding: utf-8 -*-
"""Views for the grok admin UI"""

from zope.component import getUtility, queryUtility
from BTrees.OOBTree import OOBTree
import grok
from grokcore.site.util import create_application
from grokui.base import IGrokUIRealm
from grokui.admin.interfaces import ISecurityNotifier
from grokui.admin.utilities import getVersion, getURLWithParams
from grokui.admin.security import MSG_DISABLED

grok.context(IGrokUIRealm)
grok.templatedir("templates")


class ManageApplications(grok.Permission):
    grok.name('grok.ManageApplications')


class GrokAdminInfoView(grok.View):
    """A base to provide machinereadable views.
    """
    grok.name('admin')
    grok.require('grok.ManageApplications')

    def render(self):
        return u'go to @@version or @@secnotes'


class GrokAdminVersion(grok.View):
    """Display version of a package.

    Call this view via http://localhost:8080/@@admin/@@version to
    get the used grok version. Call
    http://localhost:8080/++grokui++/@@admin/@@version?pkg=<pkgname>
    to get the used version of package <pkgname>.
    """
    grok.name('version')
    grok.context(GrokAdminInfoView)
    grok.require('grok.ManageApplications')

    def render(self, pkg='grok'):
        return u'%s %s' % (pkg, getVersion(pkg))


class GrokAdminSecurityNotes(grok.View):
    """Display current security notification.

    Call this view via http://localhost:8080/++grokui++/@@admin/@@secnote
    """
    grok.name('secnote')
    grok.context(GrokAdminInfoView)
    grok.require('grok.ManageApplications')

    def render(self):
        notifier = queryUtility(ISecurityNotifier, default=None)
        return (notifier is not None and notifier.getNotification()
                or MSG_DISABLED)


class Add(grok.View):
    """Add an application.
    """
    grok.require('grok.ManageApplications')

    def render(self, application, name):
        if name is None or name == "":
            self.redirect(self.url(self.context, 'applications'))
            return
        app = getUtility(grok.IApplication, name=application)
        if name in self.context.root.keys():
            self.flash(u'Name `%s` already in use. '
                       u'Please choose another name.' % (name,))
        else:
            create_application(app, self.context.root, name)
            self.flash(u'Added %s `%s`.' % (application, name))
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
        
        if items is not None:
            if not isinstance(items, list):
                items = [items]

            if delete is not None:
                return self.delete(items)
            elif rename is not None:
                return self.redirect(getURLWithParams(
                    self.url(self.context, '@@rename'),
                    data=dict(items=items)))

        return self.redirect(self.url(self.context, 'applications'))


class Rename(grok.Page):
    """Rename Grok applications.
    """
    grok.name('rename')
    grok.template('rename')
    grok.require('grok.ManageApplications')

    def update(self, cancel=None, items=None, new_names=None):
        """Renaming applications process.
        """
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
        root = self.context.__parent__
        existing = root.keys()

        for oldname, newname in mapping.items():
            if oldname == newname:
                continue
            if oldname not in existing:
                self.flash('Could not rename %s: not found' % oldname)
                continue
            if newname in existing:
                self.flash('`%s` already exists.' % newname)
                continue
            root[newname] = root[oldname]
            root[newname].__name__ = newname
            del root[oldname]
            self.flash('Renamed `%s` to `%s`.' % (oldname, newname))
        self.redirect(self.url(self.context, 'applications'))
        return
