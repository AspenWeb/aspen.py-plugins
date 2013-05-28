import os
import sys
from optparse import make_option
from fabricate import main, run, shell, autoclean

# Build
# =====
PLUGINS = [ 'aspen_pystache', 'aspen_tornado' ]

def _build(plugdir):
    print "Building " + plugdir
    env = os.environ
    env['PYTHONPATH'] = '.'
    run(main.options.python, os.path.join(plugdir, 'setup.py'), 'bdist_egg', env=env)

def _clean_build(plugdir):
    print "Cleaning " + plugdir
    env = os.environ
    env['PYTHONPATH'] = '.'
    shell(main.options.python, os.path.join(plugdir, 'setup.py'), 'clean', '-a', env=env)
    shell('rm', '-rf', 'build', 'dist')
    shell('find', '.', '-name', '*.pyc', '-delete')

# make a target for each plugin
#PLUGIN_TARGS = dict([ (plugin, lambda: _build(plugin)) for plugin in PLUGINS ])
#locals().update(PLUGIN_TARGS)

aspen_pystache = lambda : _build('aspen_pystache')
aspen_tornado = lambda : _build('aspen_tornado')

def build():
    for name in PLUGINS:
        _build(name)

def clean():
    autoclean()
    for plugin in PLUGINS:
        _clean_build(plugin)

def show_targets():
    print("""Valid targets:

    show_targets (default) - this
    build - build all the plugins
    """ +
    ', '.join(PLUGINS) + """ - build individual plugin
    clean - remove all build artifacts
    clean_{build} - clean some build artifacts
    
    """)
    sys.exit()

extra_options = [
                 make_option('--python', action="store", dest="python", default="python"),
                ]

main(extra_options=extra_options, default='show_targets')
