import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'pyramid>=1.5.2',
    'pyramid_debugtoolbar>=2.2.2',
    'waitress>=0.8.9',
    'PyYaml>=3.11',
    'psutil>=1.1.3',
    'pyramid_chameleon>=0.3',
]

if sys.version_info < (2,7):
    requires.append('unittest2')


# chmod some file
os.chmod("initscripts/storlever", 0755)

setup(name='storlever',
      version='0.1.0',
      license='AGPLv3',
      url='https://github.com/OpenSight/StorLever',
      description='Management/Configure System for network and storage '
                  'resource in linux system, with RESTful API',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pyramid",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Systems Administration",
      ],
      author='OpenSight',
      author_email='',
      keywords='storage restful web',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="storlever.tests",
#     data_files=[
#         ('/etc/', ['storlever.ini']),
#         ('/etc/init.d', ['initscripts/storlever']),
#     ],
      entry_points="""\
      [paste.app_factory]
      main = storlever.app:main
      """,
      )
