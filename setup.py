import os
from setuptools import setup, find_packages

tests_require = [
    'zope.app.testing',
    'zope.testbrowser',
    'zope.testing',
    'zope.security',
    'zope.securitypolicy'
    ]

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='grokui.admin',
      version='0.6dev',
      description="The Grok administration and development UI (base)",
      long_description=(
          read(os.path.join('src', 'grokui', 'admin', 'README.txt')) +
          '\n\n' +
          read('CHANGES.txt')
        ),
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'], 
      keywords="zope3 grok grokadmin",
      author="Uli Fouquet and lots of contributors from grok community",
      author_email="grok-dev@zope.org",
      url="http://svn.zope.org/grokui.admin",
      license="ZPL 2.1",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      namespace_packages = ['grokui'],
      install_requires=[
          'ZODB3',
          'grok',
          'grokui.base',
          'setuptools',
          'z3c.flashmessage',
          'zope.annotation',
          'zope.app.applicationcontrol',
          'zope.app.appsetup',
          'zope.component',
          'zope.contentprovider',
          'zope.exceptions',
          'zope.interface',
          'zope.schema',
          'zope.site',
          'zope.traversing',
          ],
      tests_require = tests_require,
      extras_require = dict(test=tests_require),
      entry_points="""
      # Add entry points here
      """,
      )
