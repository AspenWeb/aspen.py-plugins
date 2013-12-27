
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

