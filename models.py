"""ByteBites data models.

This module defines the four core classes for the ByteBites backend:

- Customer: a user; tracks `name` and `purchaseHistory` (past orders), and can
  verify whether they are a real user via `isRealUser()`.
- Item: a single food product (e.g. "Spicy Burger"); has `name` (str),
  `price` (Decimal for currency safety), `category` (str), and
  `popularityRating` (int, range 1-10).
- Menu: the full catalog; holds all Items, supports filtering by category via
  `filterByCategory()`, item removal via `removeItem()`, and category listing
  via `listCategories()`.
- Order: a single transaction; stores selected items with quantities as
  `Map<Item, int>`, supports item add/remove operations, and computes the
  total cost via `totalCost()`.

Relationships:
- Customer 1 --> * Order   (a customer places orders; past ones form history)
- Menu    1 o-- * Item     (the menu catalogs items that exist independently)
- Order   1 o-- * Item     (an order contains the selected items)

Key design decisions:
- Quantity tracking: Order uses Map<Item, int> to store both item and quantity.
- Price safety: Item.price uses Decimal (not float) to avoid currency rounding.
- Validation: popularityRating must be in valid range; customer name must be
  non-empty; prices must be non-negative.

See bytebites_design.md for the full UML class diagram and design notes.
"""
