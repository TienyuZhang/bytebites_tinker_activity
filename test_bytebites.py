"""Test suite for ByteBites data models.

Tests for Customer, Item, Menu, and Order classes, including filtering,
sorting, and cost computation methods.
"""

from decimal import Decimal
import unittest

from models import Customer, Item, Menu, Order


class TestItem(unittest.TestCase):
    """Test cases for the Item class."""

    def setUp(self):
        """Set up test fixtures."""
        self.item1 = Item("Spicy Burger", Decimal("12.99"), "Burgers", 8)
        self.item2 = Item("Large Soda", Decimal("3.50"), "Drinks", 7)
        self.item3 = Item("Chocolate Cake", Decimal("7.99"), "Desserts", 9)

    def test_item_creation(self):
        """Test that items are created with correct attributes."""
        self.assertEqual(self.item1.name, "Spicy Burger")
        self.assertEqual(self.item1.price, Decimal("12.99"))
        self.assertEqual(self.item1.category, "Burgers")
        self.assertEqual(self.item1.popularity_rating, 8)


class TestMenu(unittest.TestCase):
    """Test cases for the Menu class."""

    def setUp(self):
        """Set up test fixtures."""
        self.menu = Menu()
        self.item1 = Item("Spicy Burger", Decimal("12.99"), "Burgers", 8)
        self.item2 = Item("Large Soda", Decimal("3.50"), "Drinks", 7)
        self.item3 = Item("Chocolate Cake", Decimal("7.99"), "Desserts", 9)

    def test_menu_creation(self):
        """Test that menu is created empty."""
        self.assertEqual(len(self.menu.items), 0)

    def test_add_item(self):
        """Test adding items to the menu."""
        # self.menu.add_item(self.item1)
        # self.assertEqual(len(self.menu.items), 1)
        pass

    def test_filter_by_category(self):
        """Test filtering items by category."""
        # Add items to menu (assuming add_item is implemented)
        self.menu.items = [self.item1, self.item2, self.item3]
        
        # Filter for Drinks category
        drinks = self.menu.filter_by_category("Drinks")
        self.assertEqual(len(drinks), 1)
        self.assertEqual(drinks[0].name, "Large Soda")
        
        # Filter for Desserts category
        desserts = self.menu.filter_by_category("Desserts")
        self.assertEqual(len(desserts), 1)
        self.assertEqual(desserts[0].category, "Desserts")
        
        # Filter for category with no items
        empty_result = self.menu.filter_by_category("Pizza")
        self.assertEqual(len(empty_result), 0)

    def test_filter_by_price_range(self):
        """Test filtering items by price range."""
        pass

    def test_sort_by_price(self):
        """Test sorting items by price."""
        pass

    def test_sort_by_popularity(self):
        """Test sorting items by popularity."""
        pass

    def test_average_price(self):
        """Test calculating average item price."""
        pass


class TestOrder(unittest.TestCase):
    """Test cases for the Order class."""

    def setUp(self):
        """Set up test fixtures."""
        self.order = Order()
        self.item1 = Item("Spicy Burger", Decimal("12.99"), "Burgers", 8)
        self.item2 = Item("Large Soda", Decimal("3.50"), "Drinks", 7)

    def test_order_creation(self):
        """Test that order is created empty."""
        self.assertEqual(len(self.order.selected_items), 0)

    def test_add_item_to_order(self):
        """Test adding items to an order."""
        # Add single item
        self.order.add_item(self.item1, 2)
        self.assertEqual(len(self.order.selected_items), 1)
        self.assertEqual(self.order.selected_items[self.item1], 2)
        
        # Add another item
        self.order.add_item(self.item2, 1)
        self.assertEqual(len(self.order.selected_items), 2)

    def test_total_cost(self):
        """Test calculating total order cost with items."""
        # Add items to order (assuming add_item is implemented)
        self.order.selected_items = {self.item1: 2, self.item2: 1}
        
        # Expected total: (12.99 * 2) + (3.50 * 1) = 25.98 + 3.50 = 29.48
        expected_total = Decimal("29.48")
        actual_total = self.order.total_cost()
        self.assertEqual(actual_total, expected_total)
    
    def test_total_cost_empty(self):
        """Test calculating total cost of an empty order."""
        # Empty order should have zero cost
        self.assertEqual(self.order.total_cost(), Decimal("0.00"))

    def test_item_subtotal(self):
        """Test calculating subtotal for a single item."""
        # Add items to order
        self.order.selected_items = {self.item1: 3}
        
        # Subtotal for item1: 12.99 * 3 = 38.97
        self.assertEqual(self.order.item_subtotal(self.item1), Decimal("38.97"))
        
        # Subtotal for item not in order should be 0
        self.assertEqual(self.order.item_subtotal(self.item2), Decimal("0.00"))

    def test_item_count(self):
        """Test counting total items in order."""
        # Add items to order
        self.order.selected_items = {self.item1: 3, self.item2: 2}
        
        # Total items: 3 + 2 = 5
        self.assertEqual(self.order.item_count(), 5)
        
        # Empty order should have 0 items
        empty_order = Order()
        self.assertEqual(empty_order.item_count(), 0)

    def test_calculate_total_with_multiple_items(self):
        """Logic Test (Happy Path): Calculate total with multiple distinct items.
        
        Scenario: User adds a $10 burger and a $5 soda. Total should be $15.
        """
        # Set up items with simple prices for clarity
        burger = Item("Simple Burger", Decimal("10.00"), "Burgers", 7)
        soda = Item("Simple Soda", Decimal("5.00"), "Drinks", 6)
        
        # Add items to order: 1 burger + 1 soda
        self.order.selected_items = {burger: 1, soda: 1}
        
        # Expected: 10.00 + 5.00 = 15.00
        self.assertEqual(self.order.total_cost(), Decimal("15.00"))

    def test_order_total_is_zero_when_empty(self):
        """Edge Case Test: Verify empty order returns $0, not an error.
        
        Scenario: User opens a transaction but adds nothing. System should
        return $0.00, not crash or raise an exception.
        """
        # Create new empty order
        new_order = Order()
        self.assertEqual(len(new_order.selected_items), 0)
        
        # Calling total_cost on empty order should return 0, not raise exception
        self.assertEqual(new_order.total_cost(), Decimal("0.00"))


class TestCustomer(unittest.TestCase):
    """Test cases for the Customer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.customer = Customer("Alice")

    def test_customer_creation(self):
        """Test that customer is created with correct name."""
        self.assertEqual(self.customer.name, "Alice")
        self.assertEqual(len(self.customer.purchase_history), 0)

    def test_is_real_user(self):
        """Test customer verification."""
        pass

    def test_add_purchase(self):
        """Test recording a purchase in customer history."""
        pass


if __name__ == "__main__":
    unittest.main()
