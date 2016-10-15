from setuptools import setup, find_packages
import os

version = '2.2'

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
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Programming Language :: Python :: Implementation :: Jython',
          'Topic :: Multimedia :: Graphics'
          ],
      keywords='svg path maths',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='https://github.com/regebro/svg.path',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['svg'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
      ],
      test_suite='svg.path.tests',
      )
