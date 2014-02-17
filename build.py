import os
import sys
import shutil
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
          , 'aspen_sentry'
          , 'aspen_tornado'
          , 'aspen_twisted'
          ]

DEV_DEPS = [ 'aspen', 'pytest', 'pytest-cov' ]

ENV_ARGS = [
           './vendor/virtualenv-1.11.2.py',
           '--prompt=[aspen-plugins]',
           '--extra-search-dir=./vendor/',
           ]

def __setup(plugdir, cmd, runner=run, silent=True, python=None):
    if not os.path.exists(os.path.join(plugdir, 'ez_setup.py')): 
        shutil.copy('ez_setup.py', plugdir)
    py = python or main.options.python
    runner(py, 'setup.py', *cmd, cwd=plugdir, silent=silent)
   
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
    files = [ 'build', 'dist', 'ez_setup.py', plugdir + '.egg-info' ]
    files = [ os.path.join(plugdir, f) for f in files ]
    shell('rm', '-rf', *files, silent=False)
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
    clean_dev()

def _virt(cmd, envdir='./env'):
    return os.path.join(envdir, 'bin', cmd)

def dev(envdir='./env'):
    if os.path.exists(envdir): return
    args = [ main.options.python ] + ENV_ARGS + [ envdir ]
    shell(*args, silent=False)
    for plugin in PLUGINS:
        print("Running %s install -e %s..." % (_virt('pip', envdir=envdir), plugin))
        if not os.path.exists(os.path.join(plugin, 'ez_setup.py')):
            shutil.copy('ez_setup.py', plugin)
        # --find-links added for Cheroot which is current not hosted in PyPI
        shell(_virt('pip', envdir=envdir),
              'install', '-e', './'+plugin, '--find-links=./vendor', silent=False)
    for pkg in DEV_DEPS:
        shell(_virt('pip', envdir=envdir),
              'install', pkg, silent=False)

def clean_dev(envdir='./env'):
    shell('rm', '-rf', './env', silent=False)

def test(envdir='./env'):
    dev(envdir=envdir)
    shell(_virt('py.test', envdir=envdir), 'tests/', ignore_status=True, silent=False)

def analyse(envdir='./env'):
    dev(envdir=envdir)
    run(_virt('py.test'),
        '--junitxml=testresults.xml',
        '--cov-report', 'term',
        '--cov-report', 'xml',
        '--cov', 'aspen',
        'tests/',
        ignore_status=False)

def show_targets():
    print("""Valid targets:

    show_targets (default) - this
    build_""" +
    ',\n    build_'.join(PLUGINS) + """ - build individual plugin
    build - build all the plugins
    release_""" +
    ',\n    release_'.join(PLUGINS) + """ - release individual plugin
    release - release all plugins

    dev - make a dev environment in the 'env' directory
    test - build a test environment and run unit tests

    clean - remove all build artifacts
    clean_{build,dev} - clean some build artifacts
    """)
    sys.exit()

extra_options = [
                 make_option('--python', action="store", dest="python", default="python"),
                ]

# make a target for each plugin
PLUGIN_TARGS = dict([ ("build_" + plugin, _mkbuild(plugin)) for plugin in PLUGINS ])
PLUGIN_TARGS.update(dict([ ("release_" + plugin, _mkrelease(plugin)) for plugin in PLUGINS ]))

# add all existing targets
locals().update(PLUGIN_TARGS)

main(extra_options=extra_options, default='show_targets')

