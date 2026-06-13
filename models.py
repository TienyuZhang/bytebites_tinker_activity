"""ByteBites data models.

This module defines the four core classes for the ByteBites backend:

- Customer: a user; tracks `name` and `purchaseHistory` (past orders), and can
  verify whether they are a real user.
- Item: a single food product (e.g. "Spicy Burger"); has `name`, `price`,
  `category`, and `popularityRating`.
- Menu: the full catalog; holds all Items and filters them by category
  (e.g. "Drinks", "Desserts").
- Order: a single transaction; stores the customer's selected Items and
  computes the total cost.

Relationships:
- Customer 1 --> * Order   (a customer places orders; past ones form history)
- Menu    1 o-- * Item     (the menu catalogs items that exist independently)
- Order   1 o-- * Item     (an order contains the selected items)

See bytebites_design.md for the full UML class diagram.
"""
