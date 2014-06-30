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
    'pyramid_chameleon',
]

if sys.version_info < (2,7):
    requires.append('unittest2')


# chmod some file
os.chmod("initscripts/storlever", 0755)

setup(name='storlever',
      version='0.1.0',
      description='Management/Configure System for network and storage '
                  'resource in linux system, with RESTful API',
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
      keywords='storage restful web',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="storlever.tests",
      data_files=[
          ('/etc/', ['storlever.ini']),
          ('/etc/init.d', ['initscripts/storlever']),
      ],	  
      entry_points="""\
      [paste.app_factory]
      main = storlever.app:main
      """,
      )
