"""
Broken applications
===================

When some broken application raises DuplicationErrors during creation,
these problem will not be hidden away.

We first setup the environment:

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

We have an application type available, which raises DuplicationError
during creation intentionally:

  >>> browser.open('http://localhost/++grokui++/applications')
  >>> 'IntentionallyBrokenApp' in browser.contents
  True

If we try to add an application of that type, the traceback will be
visible:

  >>> browser.handleErrors = False
  >>> subform = browser.getForm(
  ...             name='grokui.admin.tests.brokenapps.IntentionallyBrokenApp')
  >>> subform.getControl(name='name').value = 'mybrokenapp'
  >>> subform.getControl('Create').click()
  Traceback (most recent call last):
  ...
  zope.exceptions.interfaces.DuplicationError: Intentional DuplicationError

If, however, we try to add two working apps under same name, the UI
will inform us of the problem (without a traceback):

  >>> browser.open('http://localhost/++grokui++/applications')
  >>> subform = browser.getForm(
  ...             name='grokui.admin.tests.brokenapps.WorkingApp')
  >>> subform.getControl(name='name').value = 'somename'
  >>> subform.getControl('Create').click()

  >>> subform = browser.getForm(
  ...             name='grokui.admin.tests.brokenapps.WorkingApp')
  >>> subform.getControl(name='name').value = 'somename'
  >>> subform.getControl('Create').click()

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...Name `somename` already in use. Please choose another name...
  ...

"""
import grok
from zope.exceptions import DuplicationError

class IntentionallyBrokenApp(grok.Application, grok.Container):
    """An application that intentionally raises DuplicationError.
    """

    def __init__(self, *args, **kw):
        raise DuplicationError('Intentional DuplicationError')

class WorkingApp(grok.Application, grok.Container):
    """A working app.
    """
