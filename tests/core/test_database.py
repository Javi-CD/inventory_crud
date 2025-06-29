import sqlite3

import pytest


class TestDatabaseManager:
    """Test database operations for the inventory system."""

    def test_create_tables(self, temp_database) -> None:
        """Test if the products table is created in the database.

        Args:
            temp_database (tuple): The temporary database manager and path.
        """

        db_manager, temp_path = temp_database

        # Check if the products table exists
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
        )
        result = cursor.fetchone()
        conn.close()

        assert result is not None
        assert result[0] == "products"

    def test_add_product(self, temp_database) -> None:
        """Test adding a product to the database.

        Args:
            temp_database (tuple): The temporary database manager and path.
        """
        db_manager, _ = temp_database

        # Add a test product
        db_manager.add_product("Test Product", "99.99")

        # Verify product was added
        products = db_manager.get_all_products()
        assert len(products) == 1
        assert products[0][1] == "Test Product"
        assert float(products[0][2]) == 99.99

    def test_update_product(self, temp_database) -> None:
        """Test updating a product in the database.

        Args:
            temp_database (tuple): The temporary database manager and path.
        """
        db_manager, _ = temp_database

        # Add a test product
        db_manager.add_product("Original Product", "50.00")
        products = db_manager.get_all_products()
        product_id = products[0][0]

        # Update the product
        db_manager.update_product(product_id, "Updated Product", "75.50")

        # Verify update worked
        updated_product = db_manager.get_product_by_id(product_id)
        assert updated_product[1] == "Updated Product"
        assert float(updated_product[2]) == 75.50

    def test_delete_product(self, temp_database) -> None:
        """Test deleting a product from the database.

        Args:
            temp_database (tuple): The temporary database manager and path.
        """
        db_manager, _ = temp_database

        # Add a test product
        db_manager.add_product("Delete Me", "10.00")
        products = db_manager.get_all_products()
        product_id = products[0][0]

        # Delete the product
        db_manager.delete_product(product_id)

        # Verify deletion
        products_after = db_manager.get_all_products()
        assert len(products_after) == 0

    def test_get_product_by_id(self, temp_database) -> None:
        """Test retrieving a product by its ID.

        Args:
            temp_database (tuple): The temporary database manager and path.
        """
        db_manager, _ = temp_database

        # Add a test product
        db_manager.add_product("Find Me", "25.75")
        products = db_manager.get_all_products()
        product_id = products[0][0]

        # Get product by ID
        found_product = db_manager.get_product_by_id(product_id)

        # Verify correct product retrieved
        assert found_product is not None
        assert found_product[1] == "Find Me"

    def test_get_product_stats_empty(self, temp_database) -> None:
        """Test stats on empty database.

        Args:
            temp_database (tuple): The temporary database manager and path.
        """
        db_manager, _ = temp_database
        stats = db_manager.get_product_stats()
        assert stats["total_products"] == 0

    def test_get_product_stats(self, temp_database) -> None:
        """Test product statistics.

        Args:
            temp_database (tuple): The temporary database manager and path.
        """
        db_manager, _ = temp_database

        # Add test products
        db_manager.add_product("Laptop XPS", "1200.00")
        db_manager.add_product("Laptop Thinkpad", "900.00")
        db_manager.add_product("Mouse Logitech", "25.00")

        stats = db_manager.get_product_stats()

        # Verify stats
        assert stats["total_products"] == 3
        assert float(stats["avg_price"]) == (1200.00 + 900.00 + 25.00) / 3
        assert float(stats["total_value"]) == 1200.00 + 900.00 + 25.00

        # Verify max and min products
        assert stats["max_price_product"][1] == "Laptop XPS"
        assert float(stats["max_price_product"][2]) == 1200.00

        assert stats["min_price_product"][1] == "Mouse Logitech"
        assert float(stats["min_price_product"][2]) == 25.00

        # Verify categories
        categories = {category: count for category, count in stats["categories"]}
        assert categories["Laptop"] == 2
        assert categories["Mouse"] == 1

    @pytest.mark.parametrize(
        "name,price,expected_price",
        [
            ("Product A", "10.50", 10.50),
            ("Product B", "99.99", 99.99),
            ("Product C", "0.01", 0.01),
        ],
    )
    def test_add_product_parametrized(
        self, temp_database, name, price, expected_price
    ) -> None:
        """Test adding products with different prices.

        Args:
            temp_database (tuple): The temporary database manager and path.
            name (str): The name of the product.
            price (str): The price of the product.
            expected_price (float): The expected price of the product.
        """
        db_manager, _ = temp_database

        db_manager.add_product(name, price)
        products = db_manager.get_all_products()

        assert len(products) == 1
        assert products[0][1] == name
        assert float(products[0][2]) == expected_price
