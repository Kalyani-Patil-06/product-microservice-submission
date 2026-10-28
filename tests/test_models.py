import unittest
from service import create_app, db
from service.models import Product
from tests.factories import ProductFactory


class TestProductModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.drop_all()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def test_read_a_product(self):
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertAlmostEqual(found.price, product.price)

    def test_update_a_product(self):
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        product.description = "testing"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "testing")
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "testing")

    def test_delete_a_product(self):
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        self.assertEqual(Product.all(), [])
        for _ in range(5):
            product = ProductFactory()
            product.id = None
            product.create()
        self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        products = ProductFactory.create_batch(5)
        for p in products:
            p.id = None
            p.create()
        name = products[0].name
        count = len([p for p in products if p.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(len(found), count)
        self.assertTrue(all(p.name == name for p in found))

    def test_find_by_category(self):
        products = ProductFactory.create_batch(10)
        for p in products:
            p.id = None
            p.create()
        category = products[0].category
        category_value = category.value if hasattr(category, "value") else category
        count = len([p for p in products if p.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(len(found), count)
        self.assertTrue(all(p.category == category_value for p in found))

    def test_find_by_availability(self):
        products = ProductFactory.create_batch(10)
        for p in products:
            p.id = None
            p.create()
        available = products[0].available
        count = len([p for p in products if p.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(len(found), count)
        self.assertTrue(all(p.available == available for p in found))


if __name__ == "__main__":
    unittest.main()
