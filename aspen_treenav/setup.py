try:
    import setuptools  # noqa
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup

setup( author = 'Chad Whitacre'
     , author_email = 'chad@zetaweb.com'
     , description = ('Tree navigation plugin for Aspen')
     , name = 'aspen-treenav'
     , py_modules = [ 'ez_setup', 'aspen_treenav' ]
     , url = 'http://aspen.io/'
     , version = '0.0.0-dev'
     , zip_safe = False
     , install_requires = ['aspen>=0.23']
      )
