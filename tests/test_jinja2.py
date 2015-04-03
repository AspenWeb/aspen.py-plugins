
GREETINGS = """
name="%s"
[----] via jinja2
Greetings, {{name}}!
"""


def test_basic_jinja2_template(harness):
    harness.client.website.renderer_default = 'stdlib_format'
    harness.fs.www.mk(('index.html.spt', GREETINGS % 'program'),)
    r = harness.client.GET('/')
    assert r.body == 'Greetings, program!'


def test_global_context_jinja2_template(harness):
    SIMPLATE = """
    longDict = set([1,2,3])
    [----] via jinja2
    len: {{ len(longDict) }}
    """
    website = harness.client.website
    website.renderer_default = 'stdlib_format'
    website.renderer_factories['jinja2'].Renderer.global_context = {
        'len': len
    }
    harness.fs.www.mk(('jinja2-global.html.spt', SIMPLATE),)
    r = harness.client.GET('/jinja2-global.html')
    assert r.body == 'len: 3'


def test_autoescape_off(harness):
    harness.client.website.renderer_factories['jinja2'].Renderer.autoescape = False
    harness.fs.www.mk(('index.html.spt', GREETINGS % '<foo>'),)
    r = harness.client.GET('/')
    assert r.body == 'Greetings, <foo>!'


def test_autoescape_on(harness):
    harness.client.website.renderer_factories['jinja2'].Renderer.autoescape = True
    harness.fs.www.mk(('index.html.spt', GREETINGS % '<foo>'),)
    r = harness.client.GET('/')
    assert r.body == 'Greetings, &lt;foo&gt;!'

