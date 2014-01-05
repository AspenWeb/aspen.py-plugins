
def assert_body(harness, uripath, expected_body):
    actual = harness.simple(filepath=None, uripath=uripath, want='response.body')
    assert actual == expected_body

def test_basic_jinja2_template(harness):
    CONFIG = """
    website.renderer_default="stdlib_format"
    """
    SIMPLATE = """
    name="program"
    [----] via jinja2
    Greetings, {{name}}!
    """
    harness.fs.project.mk(('configure-aspen.py', CONFIG),)
    harness.fs.www.mk(('index.html.spt', SIMPLATE),)
    assert_body(harness, '/', 'Greetings, program!')


def test_global_context_jinja2_template(harness):
    CONFIG = """
    website.renderer_default="stdlib_format"
    website.renderer_factories['jinja2'].Renderer.global_context = {
        'len': len
    }
    """
    SIMPLATE = """
    longDict = {1,2,3}
    [----] via jinja2
    len: {{ len(longDict) }}
    """
    harness.fs.project.mk(('configure-aspen.py', CONFIG),)
    harness.fs.www.mk(('jinja2-global.html.spt', SIMPLATE),)
    assert_body(harness, '/jinja2-global.html', 'len: 3')

