import json
from unittest.mock import patch
from django.contrib.auth.models import Group, User
from django.test import Client
import requests


def _login_user(client):
    group, _ = Group.objects.get_or_create(name='Manager')
    user = User.objects.create_user(username='u1', password='pass123')
    user.groups.add(group)
    client.login(username='u1', password='pass123')
    return user


def test_login_flow(db):
    user = User.objects.create_user(username='test', password='pass123')
    client = Client()
    resp = client.post('/accounts/login/', {'username': user.username, 'password': 'pass123'})
    assert resp.status_code in (302, 200)


def test_token_endpoint(db):
    client = Client()
    _login_user(client)
    resp = client.get('/accounts/api/token/')
    assert resp.status_code == 200
    body = json.loads(resp.content)
    assert 'access_token' in body


@patch('dashboard.views._call_fastapi')
@patch('dashboard.views.requests.get')
def test_dashboard_handles_outage(mock_get, mock_call, db):
    client = Client()
    _login_user(client)

    class FakeResp:
        ok = True
        def json(self):
            return {'access_token': 'abc'}

    mock_get.return_value = FakeResp()
    mock_call.return_value = (None, 'Service temporarily unavailable.')
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Service temporarily unavailable' in resp.content
