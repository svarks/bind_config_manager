from bind_config_manager.tests import *
from bind_config_manager import model
from bind_config_manager.model import meta

class TestUsersController(TestController):
    
    def test_index(self):
        self._login()
        response = self.app.get(url('users'), status=200)
    def test_new(self):
        self._login()
        response = self.app.get(url('new_user'), status=200)
    def test_create(self):
        self._login()
        response = self.app.post(url('users'),
            params={
                'User--username': 'test_user',
                'User--password': 'test_password'
            },
            status=302
        )
    def test_edit(self):
        self._login()
        user = self._get_user()
        response = self.app.get(url('edit_user', id=user.id), status=200)
    def test_update(self):
        self._login()
        user = self._get_user()
        response = self.app.put(url('user', id=user.id),
            params={
                'User-%s-username' % user.id: 'test_username',
                'User-%s-password' % user.id: 'test_password1'
            },
            status=302
        )
    def test_delete(self):
        user = self._get_user()
        response = self.app.delete(url('user', id=user.id), status=302)
        
    def _get_user(self):
        return meta.Session.query(model.User).filter_by(username='test_user').first()
    