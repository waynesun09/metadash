"""
Basic test boilerplate
"""
import json

from . import BasicTestCase


class LocalAuthTest(BasicTestCase):
    # If we shoudl keep fixtures generated by test case
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'passw0rd'
    keep_data = False

    def create_admin(self):
        from metadash.auth import user_signup, user_setrole
        user = user_signup('admin', 'passw0rd', 'local')
        assert user is not None
        user = user_setrole('admin', 'admin')
        assert user is not None

    def test_get_default_identity(self):
        rv = self.app.get('/api/me')
        data = json.loads(rv.data.decode())
        assert data['role'] == 'anonymous'

    def test_login_admin(self):
        rv = self.app.get('/api/me')
        data = json.loads(rv.data.decode())
        assert data['role'] == 'anonymous'

        self.create_admin()

        rv = self.app.post('/api/login', data=json.dumps({
            "username": self.ADMIN_USERNAME,
            "password": self.ADMIN_PASSWORD
        }), content_type='application/json')

        rv = self.app.get('/api/me')
        data = json.loads(rv.data.decode())
        assert data['role'] == 'admin'
