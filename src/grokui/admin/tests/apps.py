"""
Applications management
=======================

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = True
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

We fetch the standard page, which should provide us a menu to get all
installable grok applications/components.

  >>> browser.open("http://localhost/")
  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...      <legend>Add application</legend>
  ...

The opening screen should inform us, that there are no applications
installed yet:

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ... Currently no working...applications are installed.
  ...

We are able to add a mammoth manager...

  >>> subform = browser.getForm(name='grokui.admin.tests.apps.MammothManager')
  >>> subform.getControl(name='name').value = 'my-mammoth-manager'
  >>> subform.getControl('Create').click()

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...<legend>Installed applications</legend>
  ...
  ...<a href="http://localhost/my-mammoth-manager">
  ...

Launch the added mammoth manager

  >>> mylink = browser.getLink('my-mammoth-manager').click()
  >>> print(browser.contents)
  Let's manage some mammoths!

  >>> print(browser.url)
  http://localhost/my-mammoth-manager

We can also rename applications. For this we choose the application we
installed and click `Rename`::

  >>> browser.open("http://localhost/++grokui++/applications")
  >>> ctrl = browser.getControl(name='items')
  >>> ctrl.getControl(value='my-mammoth-manager').selected = True
  >>> browser.getControl('Rename').click()


We get a form were we can enter new names::

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...<legend> Rename applications: </legend>...

  >>> subform = browser.getForm()
  >>> subform.getControl(
  ...     name='new_names:list').value = 'my-new-mammoth-manager'
  >>> subform.getControl('Rename').click()

Our app was indeed renamed::

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...<legend>Installed applications</legend>
  ...<a href="http://localhost/my-new-mammoth-manager">
  ...my-new-mammoth-manager...

If we try to create an application with an already existing name, this
won't work, but the UI will tell us:

  >>> browser.open("http://localhost/++grokui++/applications")
  >>> subform = browser.getForm(name='grokui.admin.tests.apps.MammothManager')
  >>> subform.getControl(name='name').value = 'my-new-mammoth-manager'
  >>> subform.getControl('Create').click()

  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...Name `my-new-mammoth-manager` already in use.
  ...Please choose another name...

We are able to delete installed mammoth-managers

  >>> browser.open("http://localhost/++grokui++/applications")
  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ... <legend>Installed applications</legend>
  ...
  >>> ctrl = browser.getControl(name='items')
  >>> ctrl.getControl(value='my-new-mammoth-manager').selected = True
  >>> browser.getControl('Delete Selected').click()
  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ... Currently no working applications are installed.
  ...
  ...<legend>Add application</legend>
  ...

"""

import grok


class MammothManager(grok.Application, grok.Container):
    """A mammoth manager.
    """
    pass


class Index(grok.View):
    """A mammoth manager view.
    """

    def render(self):
        return u"Let's manage some mammoths!"
