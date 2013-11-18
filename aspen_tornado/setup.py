from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

classifiers = [ 'Development Status :: 4 - Beta'
              , 'Environment :: Console'
              , 'Intended Audience :: Developers'
              , 'License :: OSI Approved :: MIT License'
              , 'Natural Language :: English'
              , 'Operating System :: MacOS :: MacOS X'
              , 'Operating System :: Microsoft :: Windows'
              , 'Operating System :: POSIX'
              , 'Programming Language :: Python :: 2.6'
              , 'Programming Language :: Python :: 2.7'
              , 'Programming Language :: Python :: Implementation :: CPython'
              , 'Programming Language :: Python :: Implementation :: Jython'
              , 'Topic :: Internet :: WWW/HTTP :: HTTP Servers'
               ]

setup( author = 'Chad Whitacre'
     , author_email = 'chad@zetaweb.com'
     , classifiers = classifiers
     , description = ('tornado plugin for Aspen')
     , name = 'aspen-tornado'
     , entry_points = { 'aspen.renderers' : 'tornado=aspen_tornado_renderer',
                        'aspen.network_engines' : 'tornado=aspen_tornado_engine'
                      }
     , py_modules = [ 'distribute_setup', 'aspen_tornado_renderer', 'aspen_tornado_engine' ]
     , url = 'http://aspen.io/'
     , version = '0.3'
     , zip_safe = False
     , install_requires = [ 'aspen>=0.23'
                          , 'tornado'
                           ]
      )
