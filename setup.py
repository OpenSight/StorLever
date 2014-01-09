import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'pyyaml',
    'psutil>=1.1.3',
]
test_requires = []

if sys.version_info < (2,7):
    test_requires.append('unittest2')




setup(name='storlever',
      version='0.0',
      description='storlever',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
      "Programming Language :: Python",
      "Framework :: Pyramid",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires + test_requires,
      test_suite="storlever.tests",
      entry_points="""\
      [paste.app_factory]
      main = storlever:main
      """,
      )
