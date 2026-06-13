## Client Feature Request

We need to build the backend logic for the ByteBites app. The system needs to manage our customers, tracking their names and their past purchase history so the system can verify they are real users.

These customers need to browse specific food items (like a "Spicy Burger" or "Large Soda"), so we must track the name, price, category, and popularity rating for every item we sell.

We also need a way to manage the full collection of items — a digital list that holds all items and lets us filter by category such as "Drinks" or "Desserts".

Finally, when a user picks items, we need to group them into a single transaction. This transaction object should store the selected items and compute the total cost.

## Candidate Classes
Customer — represents a user, tracking their name and past purchase history (used to verify they're a real user). 

Item (e.g., FoodItem) — a single food product like "Spicy Burger" or "Large Soda", with name, price, category, and popularity rating. 

Menu — the full collection that holds all items and supports filtering by category like "Drinks" or "Desserts". 

Order (the transaction) — groups the customer's selected items into a single transaction, storing the selected items and computing the total cost.