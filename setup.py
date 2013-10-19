from setuptools import setup, find_packages
import os

version = '1.1'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='svg.path',
      version=version,
      description='SVG path objects and parser',
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Topic :: Multimedia :: Graphics'
          ],
      keywords='svg path maths',
      author='Lenart Regebro',
      author_email='regebro@gmail.com',
      url='https://github.com/regebro/svg.path',
      license='CC0 1.0 Universal',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['svg'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
      ],
      test_suite='svg.path.tests',
      )
