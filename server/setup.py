import io
import os

from catfacts import _VERSION_
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf8') as f:
    README = f.read()
with io.open(os.path.join(here, 'CHANGELOG.md'), encoding='utf8') as f:
    CHANGES = f.read()

extra_options = {
    "packages": find_packages(),
}


setup(name="CatFacts",
      version=_VERSION_,
      description='CatFacts Server Demo App for Push',
      long_description=README + '\n\n' + CHANGES,
      classifiers=["Topic :: Internet :: WWW/HTTP",
                   "Programming Language :: Python :: Implementation :: PyPy",
                   'Programming Language :: Python',
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7"
                   ],
      keywords='catfacts',
      author="JR Conlin",
      author_email="dev@jrconlin.com",
      url='http:///',
      license="MPL2",
      test_suite="nose.collector",
      include_package_data=True,
      zip_safe=False,
      tests_require=['nose', 'coverage', 'mock>=1.0.1'],
      install_requires=[
          "twisted>=15.0",
          "cyclone>=1.1",
          "configargparse>=0.9.3",
          "service-identity>=14.0.0",
      ],
      entry_points="""
      [console_scripts]
      catfacts = catfacts.main:main
      """,
      **extra_options
      )
