## Task 2 – User privileges (MME database)

### Roles used
MME has two database roles:
- admin: staff/administration tasks (full management access)
- customer: customer-facing access (browse catalogue and place orders)

This uses the principle of least privilege: customers should not be able to directly change core tables (stock, products, transactions). Instead, writes happen via stored procedures that validate inputs.

---

### Privileges by object (with brief justification)

Customer table
- admin: SELECT/INSERT/UPDATE/DELETE so staff can register customers, correct details, and handle deletion requests.
- customer: SELECT only (in a real system, row-level security would restrict this to “own record only”).

Store table
- admin: SELECT/INSERT/UPDATE/DELETE to manage store records.
- customer: SELECT only to view locations and opening hours.

Product table
- admin: SELECT/INSERT/UPDATE/DELETE to manage the product catalogue.
- customer: SELECT only to browse products and prices.

Warehouse_item table (stock per store)
- admin: SELECT/INSERT/UPDATE/DELETE for stock control, adjustments, and transfers.
- customer: SELECT only to check availability. Customers must not be able to update quantities.

Transaction table
- admin: SELECT/INSERT/UPDATE/DELETE for reporting and customer service.
- customer: SELECT only (in a real system, row-level security would restrict this to “own transactions only”).

Stored procedures and helper functions
- Both roles need EXECUTE on the two required procedures so registration and purchase go through validated routines.
- Customers may also be granted EXECUTE on read-only helper functions (e.g., check stock and delivery slot availability).

Views (reporting)
- admin: SELECT on management reports.
- customer: no access to management reporting views.

---

### GRANT commands (can be pasted into pgAdmin)

```sql
-- Create roles (optional for the assignment write-up)
CREATE ROLE admin LOGIN PASSWORD 'secure_admin_password';
CREATE ROLE customer LOGIN PASSWORD 'secure_customer_password';

-- Admin: full access to core tables
GRANT SELECT, INSERT, UPDATE, DELETE ON customer TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON store TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON product TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON warehouse_item TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON "transaction" TO admin;

-- Admin: sequences used by procedures and SERIAL columns
GRANT USAGE, SELECT ON SEQUENCE customer_id_seq TO admin;
GRANT USAGE, SELECT ON SEQUENCE transaction_id_seq TO admin;
GRANT USAGE, SELECT ON SEQUENCE product_id_seq TO admin;
GRANT USAGE, SELECT ON SEQUENCE store_id_seq TO admin;
GRANT USAGE, SELECT ON SEQUENCE warehouse_item_warehouse_item_id_seq TO admin;

-- Admin: reporting views
GRANT SELECT ON vw_sales_by_store TO admin;
GRANT SELECT ON vw_store_summary TO admin;

-- Customer: read-only access to tables
GRANT SELECT ON customer TO customer;
GRANT SELECT ON store TO customer;
GRANT SELECT ON product TO customer;
GRANT SELECT ON warehouse_item TO customer;
GRANT SELECT ON "transaction" TO customer;

-- Customer: execute validated workflows
GRANT EXECUTE ON PROCEDURE register_customer(
  VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, DATE,
  VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR
) TO customer;

GRANT EXECUTE ON PROCEDURE purchase_product(
  VARCHAR, VARCHAR, VARCHAR, INTEGER, DATE, TIME,
  VARCHAR, NUMERIC, VARCHAR
) TO customer;

-- Customer: helper functions (read-only)
GRANT EXECUTE ON FUNCTION check_stock(VARCHAR, VARCHAR) TO customer;
GRANT EXECUTE ON FUNCTION check_delivery_slot(VARCHAR, DATE, TIME) TO customer;
GRANT EXECUTE ON FUNCTION get_product_price(VARCHAR) TO customer;

-- Customer: sequences needed because procedures generate IDs using nextval()
GRANT USAGE, SELECT ON SEQUENCE customer_id_seq TO customer;
GRANT USAGE, SELECT ON SEQUENCE transaction_id_seq TO customer;

-- Admin: execute procedures and internal helper functions
GRANT EXECUTE ON PROCEDURE register_customer(
  VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, DATE,
  VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR
) TO admin;

GRANT EXECUTE ON PROCEDURE purchase_product(
  VARCHAR, VARCHAR, VARCHAR, INTEGER, DATE, TIME,
  VARCHAR, NUMERIC, VARCHAR
) TO admin;

GRANT EXECUTE ON FUNCTION generate_customer_id() TO admin;
GRANT EXECUTE ON FUNCTION generate_transaction_id() TO admin;
GRANT EXECUTE ON FUNCTION validate_sort_code(VARCHAR) TO admin;
GRANT EXECUTE ON FUNCTION validate_account_number(VARCHAR) TO admin;
GRANT EXECUTE ON FUNCTION customer_exists(VARCHAR) TO admin;
GRANT EXECUTE ON FUNCTION check_stock(VARCHAR, VARCHAR) TO admin;
GRANT EXECUTE ON FUNCTION check_delivery_slot(VARCHAR, DATE, TIME) TO admin;
GRANT EXECUTE ON FUNCTION get_product_price(VARCHAR) TO admin;

-- Ensure customers do not have access to management reports
REVOKE ALL ON vw_sales_by_store FROM customer;
REVOKE ALL ON vw_store_summary FROM customer;
```

---

### Notes (security)
- In a production system, enable row-level security on customer and transaction to restrict customers to their own rows.
- Use strong passwords and avoid shared accounts.