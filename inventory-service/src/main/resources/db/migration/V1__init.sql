CREATE TABLE products (
  sku TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0)
);

CREATE TABLE inventory (
  sku TEXT PRIMARY KEY REFERENCES products(sku) ON DELETE CASCADE,
  on_hand INTEGER NOT NULL CHECK (on_hand >= 0),
  reserved INTEGER NOT NULL CHECK (reserved >= 0),
  version BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE reservations (
  order_id UUID PRIMARY KEY,
  status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE reservation_items (
  id BIGSERIAL PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES reservations(order_id) ON DELETE CASCADE,
  sku TEXT NOT NULL REFERENCES products(sku),
  quantity INTEGER NOT NULL CHECK (quantity > 0)
);

CREATE INDEX idx_reservation_items_order_id ON reservation_items(order_id);
