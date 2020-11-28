from .. import create_app


def test_config():
    app_settings = 'department_app.config.TestingConfig'
    assert create_app(app_settings).testing
