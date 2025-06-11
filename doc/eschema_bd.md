# Inventory Database Schema

This document describes the database schema used in the Inventory Management System.

## Overview

The application uses SQLite as the database engine. The main database file is located at `src/db/inventory.db`.

## Tables

### Products

The `products` table stores information about inventory items.

| Column | Type | Description | Constraints |
|--------|------|-------------|------------|
| id | INTEGER | Unique identifier for each product | PRIMARY KEY, AUTOINCREMENT |
| name | TEXT | Product name | NOT NULL |
| price | REAL | Product price | NOT NULL |

## SQL Creation Script

```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL
);
```

## Entity Relationship Diagram

```plaintext
+------------+
|  products  |
+------------+
| id         | PK
| name       |
| price      |
+------------+
```

>[!NOTE]
> - The ``id`` field is automatically incremented for each new product
> - The ``name`` field should be unique, although this is not enforced at the database level
> - The ``price`` field stores decimal values representing the product cost

## Future Enhancements
Potential future enhancements to the schema:

- Add a created_at timestamp column
- Add a category column for product categorization
- Create a separate categories table and establish relationships
- Add quantity and stock_status columns for inventory tracking