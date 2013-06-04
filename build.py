import os
import sys
from optparse import make_option
from fabricate import main, run, shell, autoclean

# Build
# =====
PLUGINS = [ 'aspen_cherrypy' 
          , 'aspen_eventlet'
          , 'aspen_diesel' 
          , 'aspen_gevent'
          , 'aspen_jinja2'
          , 'aspen_pants'
          , 'aspen_pystache'
          , 'aspen_rocket'
          , 'aspen_tornado'
          , 'aspen_twisted'
          ]

def __setup(plugdir, cmd, runner=run, silent=True):
    env = os.environ
    env['PYTHONPATH'] = '.'
    runner(main.options.python, os.path.join(plugdir, 'setup.py'), *cmd, env=env, silent=silent)
    
def _build(plugdir):
    print "Building " + plugdir
    __setup(plugdir, ['bdist_egg'])

def _mkbuild(name):
    def builder():
        return _build(name)
    return builder

def _clean_build(plugdir):
    print "Cleaning " + plugdir
    __setup(plugdir, ['clean', '-a'])
    shell('rm', '-rf', 'build', 'dist', plugdir + '.egg-info')
    shell('find', '.', '-name', '*.pyc', '-delete')

def build():
    for name in PLUGINS:
        _build(name)

def _release(plugdir):
    print "Releasing " + plugdir
    __setup(plugdir, ['sdist', '--formats=zip,gztar,bztar', 'upload'], runner=shell, silent=False)

def release():
    for name in PLUGINS:
        _release(name)

def _mkrelease(name):
    def releaser():
        return _release(name)
    return releaser

def clean():
    autoclean()
    for plugin in PLUGINS:
        _clean_build(plugin)

def show_targets():
    print("""Valid targets:

    show_targets (default) - this
    """ +
    ',\n    '.join(PLUGINS) + """ - build individual plugin
    build - build all the plugins
    release_""" +
    ',\n    release_'.join(PLUGINS) + """ - release individual plugin
    release - release all plugins
    clean - remove all build artifacts
    clean_{build} - clean some build artifacts
    
    """)
    sys.exit()

extra_options = [
                 make_option('--python', action="store", dest="python", default="python"),
                ]

# make a target for each plugin
PLUGIN_TARGS = dict([ (plugin, _mkbuild(plugin)) for plugin in PLUGINS ])
PLUGIN_TARGS.update(dict([ ("release_" + plugin, _mkrelease(plugin)) for plugin in PLUGINS ]))

# add all existing targets
locals().update(PLUGIN_TARGS)

main(extra_options=extra_options, default='show_targets')

