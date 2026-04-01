INSERT INTO products (sku, name, unit_price) VALUES
  ('SKU-APPLE', 'Apple', 0.50),
  ('SKU-BANANA', 'Banana', 0.30),
  ('SKU-COFFEE', 'Coffee', 4.99)
ON CONFLICT (sku) DO NOTHING;

INSERT INTO inventory (sku, on_hand, reserved) VALUES
  ('SKU-APPLE', 100, 0),
  ('SKU-BANANA', 200, 0),
  ('SKU-COFFEE', 25, 0)
ON CONFLICT (sku) DO NOTHING;
