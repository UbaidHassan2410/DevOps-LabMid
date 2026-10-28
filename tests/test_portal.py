import pytest
import app as portal

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(portal, 'DB', str(tmp_path / 'test.db'))
    portal.app.config.update(TESTING=True)
    return portal.app.test_client()

def test_valid_submission_saved_and_listed(client):
    response = client.post('/', data={'name':'Ali','registration':'FA23-BSE-001','title':'Lab 1','url':'https://github.com/example/repo'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Ali' in response.data
    assert b'FA23-BSE-001' in response.data
    assert b'Submission saved successfully' in response.data

def test_missing_registration_rejected(client):
    response = client.post('/', data={'name':'Ali','registration':'','title':'Lab 1','url':'https://github.com/example/repo'})
    assert b'All fields are required' in response.data
    assert b'<td>Ali</td>' not in response.data

def test_invalid_url_rejected(client):
    response = client.post('/', data={'name':'Ali','registration':'FA23-BSE-001','title':'Lab 1','url':'not-a-url'})
    assert b'Invalid submission URL' in response.data
    assert b'<td>Ali</td>' not in response.data
