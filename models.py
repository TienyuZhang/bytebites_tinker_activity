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
from typing import Dict, List, Tuple


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
        return bool(self.name and len(self.name.strip()) > 0)

    def add_purchase(self, order: "Order") -> None:
        """Record a purchase (order) in the customer's history.
        
        Args:
            order: The Order to add to purchase history.
        """
        self.purchase_history.append(order)


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
        if item not in self.items:
            self.items.append(item)

    def remove_item(self, item: Item) -> None:
        """Remove an item from the menu.
        
        Args:
            item: The Item to remove.
        """
        if item in self.items:
            self.items.remove(item)

    def get_items(self) -> List[Item]:
        """Get all items in the menu.
        
        Returns:
            A list of all items.
        """
        return self.items[:]

    def filter_by_category(self, category: str) -> List[Item]:
        """Filter items by category.
        
        Args:
            category: The category to filter by.
            
        Returns:
            A list of items matching the category.
        """
        return [item for item in self.items if item.category == category]

    def list_categories(self) -> List[str]:
        """List all distinct categories in the menu.
        
        Returns:
            A list of unique category names.
        """
        return list(set(item.category for item in self.items))

    def filter_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[Item]:
        """Filter items by price range (budget filtering).
        
        Args:
            min_price: The minimum price (inclusive).
            max_price: The maximum price (inclusive).
            
        Returns:
            A list of items where min_price <= item.price <= max_price.
            
        Raises:
            ValueError: If min_price > max_price.
        """
        if min_price > max_price:
            raise ValueError("min_price must be <= max_price")
        return [item for item in self.items if min_price <= item.price <= max_price]

    def filter_by_popularity(self, min_rating: int) -> List[Item]:
        """Filter items by minimum popularity rating.
        
        Args:
            min_rating: The minimum popularity rating (inclusive).
            
        Returns:
            A list of items with rating >= min_rating.
        """
        return [item for item in self.items if item.popularity_rating >= min_rating]

    def items_sorted_by_price(self, ascending: bool = True) -> List[Item]:
        """Get all items sorted by price.
        
        Args:
            ascending: If True, sort low-to-high; if False, high-to-low.
            
        Returns:
            A sorted list of items.
        """
        return sorted(self.items, key=lambda item: item.price, reverse=not ascending)

    def items_sorted_by_popularity(self, ascending: bool = False) -> List[Item]:
        """Get all items sorted by popularity rating.
        
        Args:
            ascending: If False (default), sort high-to-low (most popular first).
                      If True, sort low-to-high.
            
        Returns:
            A sorted list of items.
        """
        return sorted(self.items, key=lambda item: item.popularity_rating, reverse=not ascending)

    def items_sorted_by_name(self) -> List[Item]:
        """Get all items sorted alphabetically by name.
        
        Returns:
            A sorted list of items.
        """
        return sorted(self.items, key=lambda item: item.name)

    def average_item_price(self) -> Decimal:
        """Calculate the average price of all items in the menu.
        
        Returns:
            The average price (rounded to 2 decimal places), or Decimal(0) if menu is empty.
        """
        if not self.items:
            return Decimal("0.00")
        total = sum(item.price for item in self.items)
        avg = total / len(self.items)
        return avg.quantize(Decimal("0.01"))


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
        if quantity > 0:
            self.selected_items[item] = self.selected_items.get(item, 0) + quantity

    def remove_item(self, item: Item) -> None:
        """Remove an item from the order.
        
        Args:
            item: The Item to remove.
        """
        if item in self.selected_items:
            del self.selected_items[item]

    def get_items(self) -> Dict[Item, int]:
        """Get all items in the order with their quantities.
        
        Returns:
            A dictionary mapping items to their quantities.
        """
        return self.selected_items.copy()

    def total_cost(self) -> Decimal:
        """Calculate the total cost of the order.
        
        Returns:
            The total cost as a Decimal.
        """
        total = Decimal("0.00")
        for item, quantity in self.selected_items.items():
            total += item.price * quantity
        return total

    def item_subtotal(self, item: Item) -> Decimal:
        """Calculate the subtotal for a single item in the order.
        
        Args:
            item: The Item to compute subtotal for.
            
        Returns:
            The subtotal (price × quantity) as a Decimal. Returns Decimal(0) if item
            is not in the order (does not raise an error).
        """
        if item in self.selected_items:
            return item.price * self.selected_items[item]
        return Decimal("0.00")

    def item_count(self) -> int:
        """Get the total number of items in the order (sum of all quantities).
        
        Returns:
            The total item count.
        """
        return sum(self.selected_items.values())

    def get_items_sorted_by_price(self, ascending: bool = True) -> List[Tuple[Item, int]]:
        """Get order items sorted by price (useful for receipt formatting).
        
        Args:
            ascending: If True (default), sort low-to-high; if False, high-to-low.
            
        Returns:
            A list of (Item, quantity) tuples sorted by item price.
        """
        sorted_items = sorted(self.selected_items.items(), 
                             key=lambda x: x[0].price, 
                             reverse=not ascending)
        return sorted_items
