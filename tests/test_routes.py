import unittest
from http import HTTPStatus
from service import create_app, db
from service.models import Product
from tests.factories import ProductFactory

BASE_URL = "/products"


class TestProductRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def _create_products(self, count=1):
        result = []
        for _ in range(count):
            p = ProductFactory()
            p.id = None
            p.create()
            result.append(p)
        return result

    def get_product_count(self):
        return Product.query.count()

    def test_get_product(self):
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.get_json()["name"], test_product.name)

    def test_update_product(self):
        product = self._create_products(1)[0]
        response = self.client.put(f"{BASE_URL}/{product.id}", json={"description": "testing"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.get_json()["description"], "testing")

    def test_delete_product(self):
        product = self._create_products(5)[0]
        before = self.get_product_count()
        response = self.client.delete(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(response.data, b"")
        self.assertEqual(self.get_product_count(), before - 1)
        self.assertEqual(self.client.get(f"{BASE_URL}/{product.id}").status_code, HTTPStatus.NOT_FOUND)

    def test_list_all_products(self):
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.get_json()), 5)

    def test_list_by_name(self):
        product = self._create_products(5)[0]
        response = self.client.get(BASE_URL, query_string={"name": product.name})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(all(p["name"] == product.name for p in response.get_json()))

    def test_list_by_category(self):
        product = self._create_products(5)[0]
        category = product.category.value if hasattr(product.category, "value") else product.category
        response = self.client.get(BASE_URL, query_string={"category": category})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(all(p["category"] == category for p in response.get_json()))

    def test_list_by_availability(self):
        self._create_products(10)
        expected = Product.query.filter_by(available=True).count()
        response = self.client.get(BASE_URL, query_string={"available": "true"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.get_json()
        self.assertEqual(len(data), expected)
        self.assertTrue(all(p["available"] is True for p in data))


if __name__ == "__main__":
    unittest.main()
