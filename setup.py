import os
from setuptools import setup, find_packages

tests_require = [
    'zope.app.wsgi',
    'zope.principalregistry',
    'zope.security',
    'zope.securitypolicy',
    'zope.testing',
    'zc.buildout',
    ]

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='grokui.admin',
      version='0.11',
      description="The Grok administration and development UI",
      long_description=(
          read(os.path.join('src', 'grokui', 'admin', 'README.txt')) +
          '\n\n' +
          read('CHANGES.txt')
        ),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3',
          ],
      keywords="zope3 grok grokadmin",
      author="Zope Foundation and Contributors",
      author_email="grok-dev@zope.org",
      url="http://svn.zope.org/grokui.admin",
      license="ZPL 2.1",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['grokui'],
      install_requires=[
          'ZODB3',
          'grok >= 1.10',
          'grokcore.site >= 1.6.1',
          'grokui.base',
          'setuptools',
          'z3c.flashmessage',
          'zope.applicationcontrol',
          'zope.component',
          'zope.configuration',
          'zope.contentprovider',
          'zope.exceptions',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.location',
          'zope.login',
          'zope.schema',
          'zope.site',
          'zope.size',
          'zope.traversing',
          ],
      tests_require = tests_require,
      extras_require = dict(test=tests_require),
      )
