import factory
from factory import fuzzy
from service.models import Category, Product


class ProductFactory(factory.Factory):
    """Creates fake products for testing."""
    class Meta:
        """Maps the factory to the Product model."""
        model = Product

    id = factory.Sequence(lambda n: n)
    name = fuzzy.FuzzyChoice(choices=["Hat", "Shoes", "Big Mac", "Sheets"])
    description = factory.Faker("text", max_nb_chars=120)
    price = fuzzy.FuzzyDecimal(0.5, 2000.0, 2)
    available = fuzzy.FuzzyChoice(choices=[True, False])
    category = fuzzy.FuzzyChoice(choices=[Category.UNKNOWN, Category.CLOTHS, Category.FOOD, Category.HOUSEWARES])
