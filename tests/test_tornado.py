
import os
import sys

#from aspen.configuration import Configurable
#from aspen.testing import assert_raises, attach_teardown, fix, FSFIX, mk
#from aspen.testing.fsfix import convert_path
#from tornado.template import ParseError


def assert_body(harness, uripath, expected_body):
    actual = harness.simple(filepath=None, uripath=uripath, want='output.body',
                            return_after='render_resource')
    assert actual == expected_body


def test_basic_tornado_template(harness):
    SIMPLATE = """
    name="program"
    [----] via tornado
    Greetings, {{name}}!
    """
    harness.request_processor.renderer_default = 'stdlib_format'
    harness.fs.www.mk(('index.html.spt', SIMPLATE),)
    assert_body(harness, '/', 'Greetings, program!\n')


def test_unicode_tornado_template(harness):
    SIMPLATE = u"""
    # coding: latin9
    [----] via tornado
    \u20ac
    """
    harness.request_processor.renderer_default = 'stdlib_format'
    harness.fs.www.mk(('index.html.spt', SIMPLATE, True, 'latin9'),)
    assert_body(harness, '/', u'\u20ac\n')


def test_tornado_can_load_bases(harness):
    harness.fs.project.mk(("base.html", "{% block foo %}{% end %} Blam."))
    SIMPLATE = """
                  [----] via tornado
                  {% extends base.html %}
                  {% block foo %}Some bytes!{% end %}"""
    harness.fs.www.mk(('index.html.spt', SIMPLATE),)
    assert_body(harness, '/', 'Some bytes! Blam.')

'''

def test_tornado_base_failure_fails():
    mk(("base.html", "{% block foo %}{% end %} Blam."))
    make_renderer = tornado_factory_factory()
    assert_raises( ParseError
                 , make_renderer
                 , "dummy/filepath.txt"
                 , "{% extends base.html %}"
                   "{% block foo %}Some bytes!{% end %}"
                  )

def test_tornado_caches_by_default_after_make_renderer():
    mk(("base.html", "{% block foo %}{% end %} Blam."))
    make_renderer = tornado_factory_factory(["--project_root", FSFIX])
    open(fix("base.html"), "w+").write("{% block foo %}{% end %} Blar.")
    render = make_renderer( "<string>"
                          , "{% extends base.html %}"
                            "{% block foo %}Some bytes!{% end %}"
                           )
    actual = render({})
    assert actual == "Some bytes! Blar.", actual

def test_tornado_caches_by_default():
    mk(("base.html", "{% block foo %}{% end %} Blam."))
    make_renderer = tornado_factory_factory(["--project_root", FSFIX])
    render = make_renderer( "<string>"
                          , "{% extends base.html %}"
                            "{% block foo %}Some bytes!{% end %}"
                           )
    open(fix("base.html"), "w+").write("{% block foo %}{% end %} Blar.")
    actual = render({})
    assert actual == "Some bytes! Blam.", actual

def test_tornado_obeys_changes_reload():
    mk(("base.html", "{% block foo %}{% end %} Blam."))
    make_renderer = tornado_factory_factory([ "--project_root", FSFIX
                                            , "--changes_reload=yes"
                                             ])
    render = make_renderer( "<string>"
                          , "{% extends base.html %}"
                            "{% block foo %}Some bytes!{% end %}"
                           )
    open(fix("base.html"), "w+").write("{% block foo %}{% end %} Blar.")
    actual = render({})
    assert actual == "Some bytes! Blar.", actual

def test_tornado_obeys_changes_reload_for_meta():
    mk(("base.html", "{% block foo %}{% end %} Blam."))
    make_renderer = tornado_factory_factory([ "--project_root", FSFIX
                                            , "--changes_reload=yes"
                                             ])
    open(fix("base.html"), "w+").write("{% block foo %}{% end %} Blar.")
    render = make_renderer( "<string>"
                          , "{% extends base.html %}"
                            "{% block foo %}Some bytes!{% end %}"
                           )
    actual = render({})
    assert actual == "Some bytes! Blar.", actual

def test_cheese_example():
    mk(('configure-aspen.py', """\
from aspen.renderers import Renderer, Factory

class Cheese(Renderer):
    def render_content(self, context):
        return self.compiled.replace("cheese", "CHEESE!!!!!!")

class CheeseFactory(Factory):
    Renderer = Cheese

website.renderer_factories['excited-about-cheese'] = CheeseFactory(website)
"""))
    website = Configurable.from_argv(["--project_root", FSFIX])
    make_renderer = website.renderer_factories['excited-about-cheese']
    render = make_renderer("", "I like cheese!")  # test specline elsewhere
    actual = render({})
    assert actual == "I like CHEESE!!!!!!!", actual


def test_tornado_loader_shim_resolves_path_from_absolute_nested_parent_path():
    mk(("base.html", "Resolved."), "www")
    make_renderer = tornado_factory_factory(["--project_root", FSFIX])
    path = os.path.abspath(os.path.join(FSFIX, convert_path("www/index.html")))
    render = make_renderer(path, "{% extends base.html %}")
    actual = render({})
    assert actual == "Resolved.", actual

'''

