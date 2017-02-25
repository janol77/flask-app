"""User Test."""
import unittest2
from app.test_server import app
from pyquery import PyQuery
from tools import (
    init_users,
    init_products,
    randomword,
    remove_users,
    remove_products,
    products,
    users
)


class TestInventory(unittest2.TestCase):
    """User Test."""

    def setUp(self):
        self.user_email = users[0]['email']
        self.user_password = users[0]['password']
        self.product_optico = products[0]['optico']
        self.product_tipo = products[0]['tipo']
        self.csrf = ""
        self.client = app.test_client()  # we instantiate a flask test client
        self.users_ids = init_users()
        self.products_ids = init_products()
        self.login_user()

    def tearDown(self):
        remove_users()
        remove_products()

    def login_user(self):
        data = {'email': self.user_email,
                'password': self.user_password}
        response = self.client.get(
            '/auth/login'
        )
        pq = PyQuery(response.data)
        tag = pq('input#csrf_token')
        headers = {}
        if tag:
            self.csrf = tag[0].value
            headers = {'X-CSRFToken': self.csrf}
        if response.status_code == 200:
            login = self.client.post(
                '/auth/login', data=data, headers=headers
            )
            if login.status_code == 302:
                return True

    def test_load_edit_product(self):
        # the test client can request a route
        headers = {'X-CSRFToken': self.csrf}
        response = self.client.get(
            '/inventory/edit/%s' % self.products_ids[self.product_optico],
            headers=headers
        )
        pq = PyQuery(response.data)
        optico = pq('input#optico')[0].value
        options = pq('select#tipo').find("option")
        tipo = ''
        for option in options:
            if 'selected' in option.attrib:
                tipo = option.attrib['value']
        self.assertEqual(optico, self.product_optico)
        self.assertEqual(tipo, self.product_tipo)
        self.assertEqual(response.status_code, 200)

    def test_change_edit_product(self):
        # the test client can request a route
        headers = {'X-CSRFToken': self.csrf}
        data = {'optico': randomword(8),
                'tipo': self.product_tipo,
                'ean': randomword(8),
                'id': self.products_ids[self.product_optico]}
        response = self.client.post(
            '/inventory/edit/%s' % self.products_ids[self.product_optico],
            data=data,
            headers=headers
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            '/inventory/list', headers=headers
        )
        self.assertEqual(response.status_code, 200)
        pq = PyQuery(response.data)
        data = pq('script').text()
        self.assertIn("Elemento Actualizado", data)

    def test_list_products(self):

        headers = {'X-CSRFToken': self.csrf}
        response = self.client.get(
            '/inventory/list', headers=headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):

        headers = {'X-CSRFToken': self.csrf}
        response = self.client.get(
            '/inventory/delete/%s' % self.products_ids[self.product_optico],
            headers=headers
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            '/inventory/list', headers=headers
        )
        self.assertEqual(response.status_code, 200)
        pq = PyQuery(response.data)
        data = pq('script').text()
        self.assertIn("Elemento Eliminado", data)


if __name__ == '__main__':
    unittest2.main()
