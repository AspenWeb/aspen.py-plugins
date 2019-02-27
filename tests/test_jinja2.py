import aspen_jinja2_renderer


GREETINGS = """
name="%s"
[----] via jinja2
Greetings, {{name}}!
"""


def test_basic_jinja2_template(harness):
    harness.hydrate_request_processor(renderer_default='stdlib_format')
    harness.fs.www.mk(('index.html.spt', GREETINGS % 'program'),)
    r = harness._hit('GET', '/')
    assert r.body == b'Greetings, program!'


def test_global_context_jinja2_template(harness):
    SIMPLATE = """
    longDict = set([1,2,3])
    [----] via jinja2
    len: {{ len(longDict) }}
    """
    harness.hydrate_request_processor(renderer_default='stdlib_format')
    aspen_jinja2_renderer.Renderer.global_context = {
        'len': len
    }
    harness.fs.www.mk(('jinja2-global.html.spt', SIMPLATE),)
    r = harness._hit('GET', '/jinja2-global.html')
    assert r.body == b'len: 3'


def test_autoescape_off(harness):
    aspen_jinja2_renderer.Renderer.autoescape = False
    harness.fs.www.mk(('index.html.spt', GREETINGS % '<foo>'),)
    r = harness._hit('GET', '/')
    assert r.body == b'Greetings, <foo>!'


def test_autoescape_on(harness):
    aspen_jinja2_renderer.Renderer.autoescape = True
    harness.fs.www.mk(('index.html.spt', GREETINGS % '<foo>'),)
    r = harness._hit('GET', '/')
    assert r.body == b'Greetings, &lt;foo&gt;!'

