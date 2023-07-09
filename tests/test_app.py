def test_app_is_created(app):
    assert app.name == 'project'

def test_config_is_loaded(config):
    assert config["DEBUG"] is False

def test_request_returns_404(client):
    assert client.get("/fakeUrljustFoRtests").status_code == 404