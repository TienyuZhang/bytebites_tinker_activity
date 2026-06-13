Here's a UML-style class diagram using Mermaid (renders in most markdown previewers):


classDiagram
    class Customer {
        +String name
        +List~Order~ purchaseHistory
        +isRealUser() bool
        +addPurchase(order Order) void
    }

    class Item {
        +String name
        +float price
        +String category
        +int popularityRating
    }

    class Menu {
        +List~Item~ items
        +addItem(item Item) void
        +filterByCategory(category String) List~Item~
    }

    class Order {
        +List~Item~ selectedItems
        +addItem(item Item) void
        +totalCost() float
    }

    Customer "1" --> "*" Order : places / history
    Menu "1" o-- "*" Item : catalogs
    Order "1" o-- "*" Item : contains
And the same structure as ASCII, in case the preview doesn't render Mermaid:


┌─────────────────────────┐         ┌─────────────────────────┐
│        Customer         │         │          Menu           │
├─────────────────────────┤         ├─────────────────────────┤
│ - name: String          │         │ - items: List<Item>     │
│ - purchaseHistory:      │         ├─────────────────────────┤
│       List<Order>       │         │ + addItem(item)         │
├─────────────────────────┤         │ + filterByCategory(cat) │
│ + isRealUser(): bool    │         └───────────┬─────────────┘
│ + addPurchase(order)    │                     │ 1
└───────────┬─────────────┘                     │ catalogs
            │ 1                                  │ *
            │ places                  ┌──────────▼──────────────┐
            │ *                       │          Item           │
┌───────────▼─────────────┐          ├─────────────────────────┤
│          Order          │  *       │ - name: String          │
├─────────────────────────┤ contains │ - price: float          │
│ - selectedItems:        │◆─────────│ - category: String      │
│       List<Item>        │ 1      * │ - popularityRating: int │
├─────────────────────────┤          └─────────────────────────┘
│ + addItem(item)         │
│ + totalCost(): float    │
└─────────────────────────┘
Relationships:

Customer → Order (association): a customer places orders; past ones form their purchaseHistory.
Menu ◇→ Item (aggregation): the menu catalogs many items, but items can exist independently of the menu.
Order ◇→ Item (aggregation): an order contains the items the customer selected.