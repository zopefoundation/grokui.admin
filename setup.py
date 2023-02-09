import os

from setuptools import find_packages
from setuptools import setup


tests_require = [
    'zc.buildout',
    'zope.exceptions',
    'zope.fanstatic',
    'zope.principalregistry',
    'zope.security',
    'zope.securitypolicy',
    'zope.session',
    'zope.testbrowser',
    'zope.testing',
]


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(name='grokui.admin',
      version='1.0.dev0',
      description="The Grok administration and development UI",
      long_description=(
          read('README.rst') +
          '\n\n' +
          read('CHANGES.rst')
      ),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: Implementation :: CPython',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope :: 3',
      ],
      keywords="zope3 grok grokadmin",
      author="Zope Foundation and Contributors",
      author_email="grok-dev@zope.org",
      url="https://github.com/zopefoundation/grokui.admin",
      project_urls={
          'Issue Tracker': ('https://github.com/zopefoundation/'
                            'grokui.admin/issues'),
          'Sources': 'https://github.com/zopefoundation/grokui.admin',
      },
      license="ZPL 2.1",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['grokui'],
      python_requires='>=3.7',
      install_requires=[
          'BTrees',
          'ZODB >= 5.0',
          'grok >= 1.10',
          'grokcore.site >= 1.6.1',
          'grokui.base >= 0.8.2',
          'persistent',
          'setuptools',
          'z3c.flashmessage',
          'zope.applicationcontrol',
          'zope.component',
          'zope.configuration',
          'zope.contentprovider',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.location',
          'zope.login',
          'zope.schema',
          'zope.site',
          'zope.size',
          'zope.traversing',
      ],
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      )
