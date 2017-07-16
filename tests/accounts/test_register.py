from rest_framework.test import APITestCase

import logging
logger = logging.getLogger(__name__)


class Test(APITestCase):

    def _post_register(self, drops=None, **kwargs):
        payload = {
            'username': 'user1',
            'email': '123@123.com',
            'password': 'password',
            'password2': 'password'
        }

        if drops is not None:
            for key in drops:
                payload.pop(key, None)

        payload.update(kwargs)

        return self.client.post('/api/users/register/', payload)

    def test_success(self):
        resp = self._post_register()

        self.assertEqual(resp.status_code, 200)

    def test_mismatch(self):
        resp = self._post_register(password2='2333')

        self.assertEqual(resp.status_code, 400)
        self.assertIn(b'mismatch', resp.content)

    def test_empty(self):
        resp = self._post_register(drops=['password'])

        self.assertEqual(resp.status_code, 400)
        self.assertIn(b'required', resp.content)

        resp = self._post_register(drops=['password2'])

        self.assertEqual(resp.status_code, 400)
        self.assertIn(b'required', resp.content)

        resp = self._post_register(password='', password2='')

        self.assertEqual(resp.status_code, 400)
        self.assertIn(b'blank', resp.content)

    def test_email(self):
        resp = self._post_register(email='1')

        self.assertEqual(resp.status_code, 400)
        self.assertIn(b'valid email', resp.content)

    def test_duplicate(self):
        from biohub.accounts.models import User

        User.objects.create_user(
            username='user1',
            email='123@123.com',
            password='12345')

        resp = self._post_register(email='123@12.com')

        self.assertEqual(resp.status_code, 400)
        self.assertIn(b'exists', resp.content)

    def test_response(self):
        resp = self._post_register()

        self.assertDictContainsSubset({
            'username': 'user1',
            'email': '123@123.com',
        }, resp.data)

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(
            str(resp.data['id']),
            self.client.session['_auth_user_id'])

    def test_logined(self):
        from biohub.accounts.models import User
        self.client.force_authenticate(
            User.objects.create_user(
                username='user1',
                email='123@123.com',
                password='12345'))

        resp = self._post_register()
        self.assertEqual(resp.status_code, 404)