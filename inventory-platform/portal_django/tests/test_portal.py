from django.contrib.auth.models import User, Group
from django.test import Client
from unittest.mock import patch


def setup_user():
    user = User.objects.create_user(username='u1', password='pass123')
    group, _ = Group.objects.get_or_create(name='Manager')
    user.groups.add(group)
    return user


def test_login_flow(db):
    setup_user()
    c = Client()
    assert c.login(username='u1', password='pass123')


def test_token_endpoint(db):
    user = setup_user()
    c = Client()
    c.force_login(user)
    resp = c.get('/accounts/api/token')
    assert resp.status_code == 200
    assert 'access_token' in resp.json()


def test_dashboard_handles_outage(db):
    user = setup_user()
    c = Client()
    c.force_login(user)

    with patch('dashboard.views.requests.get') as mocked:
        mocked.side_effect = Exception('FastAPI down')
        resp = c.get('/')
        assert resp.status_code == 200
