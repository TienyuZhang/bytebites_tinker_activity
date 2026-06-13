"""ByteBites data models.

This module defines the four core classes for the ByteBites backend:

- Customer: a user; tracks `name` and `purchase_history` (past orders), and can
  verify whether they are a real user via `is_real_user()`.
- Item: a single food product (e.g. "Spicy Burger"); has `name` (str),
  `price` (Decimal for currency safety), `category` (str), and
  `popularity_rating` (int, range 1-10).
- Menu: the full catalog; holds all Items, supports filtering by category via
  `filter_by_category()`, item removal via `remove_item()`, and category listing
  via `list_categories()`.
- Order: a single transaction; stores selected items with quantities as
  `Dict[Item, int]`, supports item add/remove operations, and computes the
  total cost via `total_cost()`.

Relationships:
- Customer 1 --> * Order   (a customer places orders; past ones form history)
- Menu    1 o-- * Item     (the menu catalogs items that exist independently)
- Order   1 o-- * Item     (an order contains the selected items)

Key design decisions:
- Quantity tracking: Order uses Dict[Item, int] to store both item and quantity.
- Price safety: Item.price uses Decimal (not float) to avoid currency rounding.
- Validation: popularity_rating must be in valid range [1, 10]; customer name must be
  non-empty; prices must be non-negative.

See bytebites_design.md for the full UML class diagram and design notes.
"""

from decimal import Decimal
from typing import Dict, List


class Customer:
    """A user who places orders and has a purchase history."""

    def __init__(self, name: str):
        """Initialize a customer with a name.
        
        Args:
            name: The customer's name (must be non-empty).
        """
        self.name = name
        self.purchase_history: List[Order] = []

    def is_real_user(self) -> bool:
        """Verify whether this customer is a real user.
        
        Returns:
            True if the customer meets real user criteria, False otherwise.
        """
        raise NotImplementedError

    def add_purchase(self, order: "Order") -> None:
        """Record a purchase (order) in the customer's history.
        
        Args:
            order: The Order to add to purchase history.
        """
        raise NotImplementedError


class Item:
    """A single food product with price, category, and popularity."""

    def __init__(self, name: str, price: Decimal, category: str, popularity_rating: int):
        """Initialize a menu item.
        
        Args:
            name: The item's name.
            price: The item's price (Decimal for currency safety).
            category: The item's category (e.g., "Drinks", "Desserts").
            popularity_rating: A rating from 1-10 indicating popularity.
        """
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating


class Menu:
    """The full catalog of menu items with filtering and management."""

    def __init__(self):
        """Initialize an empty menu."""
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        """Add an item to the menu.
        
        Args:
            item: The Item to add.
        """
        raise NotImplementedError

    def remove_item(self, item: Item) -> None:
        """Remove an item from the menu.
        
        Args:
            item: The Item to remove.
        """
        raise NotImplementedError

    def get_items(self) -> List[Item]:
        """Get all items in the menu.
        
        Returns:
            A list of all items.
        """
        raise NotImplementedError

    def filter_by_category(self, category: str) -> List[Item]:
        """Filter items by category.
        
        Args:
            category: The category to filter by.
            
        Returns:
            A list of items matching the category.
        """
        raise NotImplementedError

    def list_categories(self) -> List[str]:
        """List all distinct categories in the menu.
        
        Returns:
            A list of unique category names.
        """
        raise NotImplementedError


class Order:
    """A single transaction containing selected items with quantities."""

    def __init__(self):
        """Initialize an empty order."""
        self.selected_items: Dict[Item, int] = {}

    def add_item(self, item: Item, quantity: int) -> None:
        """Add an item to the order with a specified quantity.
        
        Args:
            item: The Item to add.
            quantity: The quantity of the item to add.
        """
        raise NotImplementedError

    def remove_item(self, item: Item) -> None:
        """Remove an item from the order.
        
        Args:
            item: The Item to remove.
        """
        raise NotImplementedError

    def get_items(self) -> Dict[Item, int]:
        """Get all items in the order with their quantities.
        
        Returns:
            A dictionary mapping items to their quantities.
        """
        raise NotImplementedError

    def total_cost(self) -> Decimal:
        """Calculate the total cost of the order.
        
        Returns:
            The total cost as a Decimal.
        """
        raise NotImplementedError
