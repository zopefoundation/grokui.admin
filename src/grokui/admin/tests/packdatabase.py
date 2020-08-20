"""
ZODB packing
============

Create a mammoth-manager, and stuff it with data which can be packed.
  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open("http://localhost/")

  >>> subform = browser.getForm(
  ...    name='grokui.admin.tests.packdatabase.StuffedMammoth')
  >>> subform.getControl(name='name').value = 'my-stuffed-mammoth'
  >>> subform.getControl('Create').click()
  >>> mylink = browser.getLink('my-stuffed-mammoth').click()

Stuff this mammoth.
  >>> url = browser.url
  >>> browser.open(url+"?stuffing=fresh+vegetables")
  >>> print(browser.contents)
  Today's meal is stuffed mammoth!

Time to pull the stuffing out again.
  >>> browser.open(url)
  >>> print(browser.contents)
  Time to stuff a mammoth!

Check the size of the ZODB.
  >>> browser.open("http://localhost/++grokui++/server")
  >>> lines = [ l.strip() for l in browser.contents.split('\\n') ]
  >>> zodb_size = lines[lines.index("main")+  1]
  >>> num_zodb_size = int(zodb_size.split(' ')[0])

Now, pack the database.

  >>> lines = [ l.strip() for l in browser.contents.split('\\n') ]
  >>> zodb_size = lines[lines.index("main")+  1]
  >>> new_num_zodb_size = int(zodb_size.split(' ')[0])

And clean up after ourselves.
  >>> browser.open("http://localhost/++grokui++/applications")
  >>> ctrl = browser.getControl(name='items')
  >>> ctrl.getControl(value='my-stuffed-mammoth').selected = True
  >>> browser.getControl('Delete Selected').click()

"""

import grok


class StuffedMammoth(grok.Application, grok.Container):
    """A stuffed mammoth.
    """
    stuffing = None


class Index(grok.View):

    def update(self, stuffing=None):
        if stuffing is not None:
            self.context.stuffing = stuffing * 1000
        else:
            self.context.stuffing = None

    def render(self):
        if self.context.stuffing is None:
            return u"Time to stuff a mammoth!"
        else:
            return u"Today's meal is stuffed mammoth!"
