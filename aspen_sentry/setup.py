from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup( author = 'Chad Whitacre'
     , author_email = 'chad@zetaweb.com'
     , description = ('Sentry plugin for Aspen')
     , name = 'aspen-sentry'
     , py_modules = [ 'distribute_setup', 'aspen_sentry' ]
     , url = 'http://aspen.io/'
     , version = '1.0.0'
     , zip_safe = False
     , install_requires = [ 'aspen>=0.23'
                          , 'raven'
                           ]
      )
