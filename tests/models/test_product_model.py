from src.models.product_model import Product


def test_product_initialization() -> None:
    """Test product initialization with default and custom values.

    Returns:
        None
    """
    # Default initialization
    default_product = Product()
    assert default_product.id is None
    assert default_product.name == ""
    assert default_product.price == 0.0

    # Custom initialization
    custom_product = Product(id=1, name="Test Product", price=99.99)
    assert custom_product.id == 1
    assert custom_product.name == "Test Product"
    assert custom_product.price == 99.99


def test_product_from_db_tuple() -> None:
    """Test creating a Product from a database tuple.

    Returns:
        None
    """
    db_tuple = (5, "Database Product", "149.99")
    product = Product.from_db_tuple(db_tuple)
    assert product.id == 5
    assert product.name == "Database Product"
    assert product.price == 149.99
    # Test with None
    assert Product.from_db_tuple(None) is None


def test_product_to_dict() -> None:
    """Test converting a Product to dictionary.

    Returns:
        None
    """
    product = Product(id=10, name="Dictionary Product", price=50.25)
    product_dict = product.to_dict()
    assert product_dict["id"] == 10
    assert product_dict["name"] == "Dictionary Product"
    assert product_dict["price"] == 50.25


def test_product_str() -> None:
    """Test string representation of Product.

    Returns:
        None
    """
    product = Product(id=7, name="String Product", price=75.50)
    product_str = str(product)
    assert product_str == "ID 7 - String Product - $75.50"
