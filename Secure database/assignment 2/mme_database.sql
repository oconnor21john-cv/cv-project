-- Millie's Musical Emporium (MME) - PostgreSQL script (Task 1)


-- 1) Reset objects 
DROP VIEW IF EXISTS vw_sales_by_store CASCADE;
DROP VIEW IF EXISTS vw_store_summary CASCADE;

DROP TABLE IF EXISTS "transaction" CASCADE;
DROP TABLE IF EXISTS warehouse_item CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS store CASCADE;
DROP TABLE IF EXISTS customer CASCADE;

DROP SEQUENCE IF EXISTS customer_id_seq CASCADE;
DROP SEQUENCE IF EXISTS transaction_id_seq CASCADE;
DROP SEQUENCE IF EXISTS product_id_seq CASCADE;
DROP SEQUENCE IF EXISTS store_id_seq CASCADE;

-- 2) Sequences 

CREATE SEQUENCE customer_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE transaction_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE product_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE store_id_seq START WITH 1 INCREMENT BY 1;


-- 3) Tables 

-- CUSTOMER
CREATE TABLE customer (
    customer_id       VARCHAR(3) PRIMARY KEY,
    customer_fname    VARCHAR(20) NOT NULL,
    customer_sname    VARCHAR(20) NOT NULL,
    address_line1     VARCHAR(60) NOT NULL,
    address_line2     VARCHAR(60),
    city              VARCHAR(30) NOT NULL,
    postcode          VARCHAR(10) NOT NULL,
    telephone         VARCHAR(20) NOT NULL,
    date_of_birth     DATE NOT NULL,
    email             VARCHAR(80),
    bank_name         VARCHAR(30) NOT NULL,
    bank_address      VARCHAR(80) NOT NULL,
    sort_code         CHAR(8) NOT NULL,                    
    account_number    CHAR(8) NOT NULL,                    
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT chk_sort_code CHECK (sort_code ~ '^[0-9]{2}-[0-9]{2}-[0-9]{2}$'),
    CONSTRAINT chk_account_number CHECK (account_number ~ '^[0-9]{8}$'),
    CONSTRAINT chk_dob_past CHECK (date_of_birth < CURRENT_DATE),
    CONSTRAINT chk_customer_age CHECK (date_of_birth <= CURRENT_DATE - INTERVAL '18 years')
);


CREATE UNIQUE INDEX uk_customer_email_lower
ON customer (LOWER(email))
WHERE email IS NOT NULL;

-- STORE
CREATE TABLE store (
    store_id     VARCHAR(3) PRIMARY KEY,
    store_name   VARCHAR(40) NOT NULL,
    address_line1 VARCHAR(60) NOT NULL,
    address_line2 VARCHAR(60),
    city         VARCHAR(30) NOT NULL,
    postcode     VARCHAR(10) NOT NULL,
    telephone    VARCHAR(20) NOT NULL,
    opening_time TIME NOT NULL DEFAULT '09:00',
    closing_time TIME NOT NULL DEFAULT '18:00',
    CONSTRAINT chk_store_hours CHECK (opening_time < closing_time)
);

-- PRODUCT
CREATE TABLE product (
    product_id          VARCHAR(3) PRIMARY KEY,
    product_type        VARCHAR(20) NOT NULL,
    product_name        VARCHAR(50) NOT NULL,
    product_description VARCHAR(120),
    product_cost        NUMERIC(10,2) NOT NULL,
    CONSTRAINT chk_product_cost CHECK (product_cost >= 0),
    CONSTRAINT chk_product_type CHECK (
        product_type IN ('Instrument', 'Media', 'Accessory', 'Book', 'CD', 'DVD')
    )
);


-- WAREHOUSE_ITEM 
CREATE TABLE warehouse_item (
    warehouse_item_id SERIAL PRIMARY KEY,
    product_id        VARCHAR(3) NOT NULL,
    store_id          VARCHAR(3) NOT NULL,
    quantity          INTEGER NOT NULL DEFAULT 0,
    last_updated      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_wh_product FOREIGN KEY (product_id)
        REFERENCES product(product_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_wh_store FOREIGN KEY (store_id)
        REFERENCES store(store_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT chk_wh_qty CHECK (quantity >= 0),
    CONSTRAINT uk_wh_product_store UNIQUE (product_id, store_id)
);


-- TRANSACTION 
CREATE TABLE "transaction" (
    transaction_id     VARCHAR(3) PRIMARY KEY,
    customer_id        VARCHAR(3) NOT NULL,
    product_id         VARCHAR(3) NOT NULL,
    store_id           VARCHAR(3) NOT NULL,
    quantity           INTEGER NOT NULL DEFAULT 1,
    transaction_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    delivery_date      DATE NOT NULL,
    delivery_time      TIME NOT NULL,
    total_amount       NUMERIC(10,2) NOT NULL,
    transaction_status VARCHAR(12) NOT NULL DEFAULT 'Confirmed',
    CONSTRAINT fk_tr_customer FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_tr_product FOREIGN KEY (product_id)
        REFERENCES product(product_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_tr_store FOREIGN KEY (store_id)
        REFERENCES store(store_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_tr_qty CHECK (quantity > 0),
    CONSTRAINT chk_tr_total CHECK (total_amount >= 0),
    CONSTRAINT chk_tr_delivery_date CHECK (delivery_date >= transaction_date),
    CONSTRAINT chk_tr_status CHECK (transaction_status IN ('Pending','Confirmed','Delivered','Cancelled'))
);


-- 4) Indexes 

CREATE INDEX idx_customer_sname ON customer(customer_sname);
CREATE INDEX idx_product_type ON product(product_type);
CREATE INDEX idx_wh_product ON warehouse_item(product_id);
CREATE INDEX idx_wh_store ON warehouse_item(store_id);
CREATE INDEX idx_tr_customer ON "transaction"(customer_id);
CREATE INDEX idx_tr_store ON "transaction"(store_id);
CREATE INDEX idx_tr_date ON "transaction"(transaction_date);


-- 5) Sample data

-- Stores
INSERT INTO store (store_id, store_name, address_line1, address_line2, city, postcode, telephone, opening_time, closing_time)
VALUES
    ('S01', 'MME Belfast',     '27 Castle Lane',         NULL,              'Belfast',     'BT1 1AA',  '028 9000 1200', '09:30', '18:00'),
    ('S02', 'MME Derry',       '14 Shipquay Street',     'City Centre',     'Derry',       'BT48 6AF', '028 7100 2450', '10:00', '17:30'),
    ('S03', 'MME Lisburn',     '8 Bow Street',           NULL,              'Lisburn',     'BT28 1BN', '028 9200 3321', '09:00', '18:00'),
    ('S04', 'MME Newry',       '52 Hill Street',         'Canal Quay',      'Newry',       'BT34 1AQ', '028 3000 4815', '09:00', '17:00'),
    ('S05', 'MME Coleraine',   '3 Church Street',        'Riverside',       'Coleraine',   'BT52 1AR', '028 7030 7788', '09:30', '17:30');

-- Products
INSERT INTO product (product_id, product_type, product_name, product_description, product_cost)
VALUES
    ('P01', 'Instrument', 'Yamaha Acoustic Guitar', 'FG-series acoustic guitar', 199.99),
    ('P02', 'Instrument', 'Fender Stratocaster',    'Electric guitar',           649.99),
    ('P03', 'Instrument', 'Roland Digital Piano',   'Stage piano',               599.00),
    ('P04', 'Instrument', 'Pearl Drum Kit',         '5-piece kit',               799.99),
    ('P05', 'Instrument', 'Yamaha Flute',           'Student flute',             449.00),
    ('P06', 'Book',       'Guitar Method Book',     'Method book',               19.99),
    ('P07', 'Book',       'Piano Grade 5',          'Grade pieces',              12.99),
    ('P08', 'CD',         'Classical Masterpieces', 'Compilation',               14.99),
    ('P09', 'DVD',        'Learn Drums DVD',        'Beginner lessons',          24.99),
    ('P10', 'Accessory',  'Guitar Strings Pack',    '6-pack strings',            29.99);

-- Stock (warehouse items)
INSERT INTO warehouse_item (product_id, store_id, quantity)
VALUES
    ('P01','S01', 15), ('P02','S01', 8),  ('P03','S01', 5),  ('P04','S01', 3),  ('P05','S01', 10), ('P06','S01', 50),
    ('P07','S01', 40), ('P08','S01', 25), ('P09','S01', 20), ('P10','S01',100),
    ('P01','S02', 12), ('P02','S02', 6),  ('P03','S02', 4),  ('P04','S02', 2),  ('P06','S02', 35), ('P08','S02', 15),
    ('P01','S03', 10), ('P02','S03', 5),  ('P05','S03', 8),  ('P06','S03', 30), ('P07','S03', 25), ('P10','S03', 60),
    ('P01','S04',  8), ('P03','S04', 3),  ('P04','S04', 1),  ('P06','S04', 20), ('P09','S04', 10),
    ('P01','S05',  7), ('P02','S05', 4),  ('P05','S05', 6),  ('P07','S05', 15), ('P08','S05', 12), ('P10','S05', 45);

-- Customers
INSERT INTO customer (customer_id, customer_fname, customer_sname, address_line1, address_line2, city, postcode, telephone,
                      date_of_birth, email, bank_name, bank_address, sort_code, account_number)
VALUES
    ('C01','Niamh','O''Neill','12 Ardenlee Avenue',NULL,'Belfast','BT6 8QX','028 9012 4455','1990-05-15','niamh.oneill@email.com',
     'Danske Bank','Donegall Square West, Belfast','20-00-00','12345678'),
    ('C02','Ryan','McKenna','4 Laurelbank',NULL,'Lisburn','BT27 4YH','028 9266 1188','1985-11-22','ryan.mckenna@email.com',
     'Ulster Bank','Donegall Square East, Belfast','40-00-00','87654321'),
    ('C03','Aoife','Gallagher','78 Strand Road','Flat 2','Derry','BT48 7AB','028 7122 9030','1992-03-08','aoife.gallagher@email.com',
     'Bank of Ireland','7-15 Bedford Street, Belfast','30-00-00','11223344'),
    ('C04','Conor','O''Donnell','23 Ashgrove',NULL,'Newry','BT34 2DJ','028 3026 7700','1988-07-30','conor.odonnell@email.com',
     'Santander','Royal Avenue, Belfast','60-00-00','55667788'),
    ('C05','Erin','Crawford','91 Lough Road','House 5','Coleraine','BT52 1PS','028 7035 2210','1995-12-01','erin.crawford@email.com',
     'Nationwide','1-3 Donegall Place, Belfast','09-00-00','99887766');

-- ransactions (fixed historic sample)
INSERT INTO "transaction" (transaction_id, customer_id, product_id, store_id, quantity, transaction_date,
                           delivery_date, delivery_time, total_amount, transaction_status)
VALUES
    ('T01','C01','P01','S01',1,'2025-12-01','2025-12-05','14:00',199.99,'Delivered'),
    ('T02','C02','P06','S02',2,'2025-12-10','2025-12-12','10:30',39.98,'Delivered'),
    ('T03','C03','P02','S03',1,'2025-12-15','2025-12-20','16:00',649.99,'Confirmed'),
    ('T04','C01','P08','S01',3,'2025-12-18','2025-12-22','11:00',44.97,'Pending'),
    ('T05','C04','P03','S04',1,'2025-12-20','2025-12-28','15:30',599.00,'Confirmed');

-- sequences generate new IDs
SELECT setval('customer_id_seq', 5, true);
SELECT setval('transaction_id_seq', 5, true);
SELECT setval('store_id_seq', 5, true);
SELECT setval('product_id_seq', 10, true);


-- 6) helper functions

-- Generate IDs (VARCHAR(3) formats)
CREATE OR REPLACE FUNCTION generate_customer_id()
RETURNS VARCHAR(3)
LANGUAGE plpgsql
AS $$
DECLARE
    v_next INTEGER;
BEGIN
    SELECT nextval('customer_id_seq') INTO v_next;
    IF v_next > 99 THEN
        RAISE EXCEPTION 'Customer ID sequence exhausted (limit is 99 with 3-char IDs)';
    END IF;
    RETURN 'C' || lpad(v_next::text, 2, '0');
END;
$$;

CREATE OR REPLACE FUNCTION generate_transaction_id()
RETURNS VARCHAR(3)
LANGUAGE plpgsql
AS $$
DECLARE
    v_next INTEGER;
BEGIN
    SELECT nextval('transaction_id_seq') INTO v_next;
    IF v_next > 99 THEN
        RAISE EXCEPTION 'Transaction ID sequence exhausted (limit is 99 with 3-char IDs)';
    END IF;
    RETURN 'T' || lpad(v_next::text, 2, '0');
END;
$$;

CREATE OR REPLACE FUNCTION validate_sort_code(p_sort_code VARCHAR)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN (p_sort_code ~ '^[0-9]{2}-[0-9]{2}-[0-9]{2}$');
END;
$$;

CREATE OR REPLACE FUNCTION validate_account_number(p_account VARCHAR)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN (p_account ~ '^[0-9]{8}$');
END;
$$;

CREATE OR REPLACE FUNCTION customer_exists(p_email VARCHAR)
RETURNS VARCHAR(3)
LANGUAGE plpgsql
AS $$
DECLARE
    v_customer_id VARCHAR(3);
BEGIN
    SELECT customer_id
    INTO v_customer_id
    FROM customer
    WHERE email IS NOT NULL
      AND LOWER(email) = LOWER(p_email);

    RETURN v_customer_id;
END;
$$;

CREATE OR REPLACE FUNCTION check_stock(p_product_id VARCHAR, p_store_id VARCHAR)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_qty INTEGER;
BEGIN
    SELECT quantity INTO v_qty
    FROM warehouse_item
    WHERE product_id = p_product_id AND store_id = p_store_id;

    RETURN COALESCE(v_qty, 0);
END;
$$;

-- Delivery slot capacity check (slot defined as store+date+time)
CREATE OR REPLACE FUNCTION check_delivery_slot(
    p_store_id VARCHAR,
    p_delivery_date DATE,
    p_delivery_time TIME
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    v_slot_count INTEGER;
    v_max_slots CONSTANT INTEGER := 5; -- allows up to 5 deliveries per slot
BEGIN
    SELECT COUNT(*) INTO v_slot_count
    FROM "transaction"
    WHERE store_id = p_store_id
      AND delivery_date = p_delivery_date
      AND delivery_time = p_delivery_time
      AND transaction_status <> 'Cancelled';

    RETURN (v_slot_count < v_max_slots);
END;
$$;

CREATE OR REPLACE FUNCTION get_product_price(p_product_id VARCHAR)
RETURNS NUMERIC(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_price NUMERIC(10,2);
BEGIN
    SELECT product_cost INTO v_price
    FROM product
    WHERE product_id = p_product_id;

    RETURN v_price;
END;
$$;


-- 7) Stored procedures



CREATE OR REPLACE PROCEDURE register_customer(
    p_fname VARCHAR,
    p_sname VARCHAR,
    p_address_line1 VARCHAR,
    p_address_line2 VARCHAR,
    p_city VARCHAR,
    p_postcode VARCHAR,
    p_telephone VARCHAR,
    p_dob DATE,
    p_email VARCHAR,
    p_bank_name VARCHAR,
    p_bank_address VARCHAR,
    p_sort_code VARCHAR,
    p_account_number VARCHAR,
    INOUT p_customer_id VARCHAR,
    INOUT p_message VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_existing_customer VARCHAR(3);
    v_age INTEGER;
    v_email_clean VARCHAR(80);
BEGIN
    p_customer_id := NULL;
    p_message := '';

    -- Mandatory checks 
    IF p_fname IS NULL OR btrim(p_fname) = '' THEN RAISE EXCEPTION 'First name is required'; END IF;
    IF p_sname IS NULL OR btrim(p_sname) = '' THEN RAISE EXCEPTION 'Surname is required'; END IF;
    IF p_address_line1 IS NULL OR btrim(p_address_line1) = '' THEN RAISE EXCEPTION 'Address line 1 is required'; END IF;
    IF p_city IS NULL OR btrim(p_city) = '' THEN RAISE EXCEPTION 'City is required'; END IF;
    IF p_postcode IS NULL OR btrim(p_postcode) = '' THEN RAISE EXCEPTION 'Postcode is required'; END IF;
    IF p_telephone IS NULL OR btrim(p_telephone) = '' THEN RAISE EXCEPTION 'Telephone is required'; END IF;
    IF p_dob IS NULL THEN RAISE EXCEPTION 'Date of birth is required'; END IF;
    IF p_bank_name IS NULL OR btrim(p_bank_name) = '' THEN RAISE EXCEPTION 'Bank name is required'; END IF;
    IF p_bank_address IS NULL OR btrim(p_bank_address) = '' THEN RAISE EXCEPTION 'Bank address is required'; END IF;
    IF p_sort_code IS NULL OR btrim(p_sort_code) = '' THEN RAISE EXCEPTION 'Sort code is required'; END IF;
    IF p_account_number IS NULL OR btrim(p_account_number) = '' THEN RAISE EXCEPTION 'Account number is required'; END IF;

    -- Date validation
    IF p_dob >= CURRENT_DATE THEN
        RAISE EXCEPTION 'Date of birth must be in the past';
    END IF;

    v_age := EXTRACT(YEAR FROM AGE(CURRENT_DATE, p_dob));
    IF v_age < 18 THEN
        RAISE EXCEPTION 'Customer must be at least 18 years old (age=%)', v_age;
    END IF;

    -- Banking validations
    IF NOT validate_sort_code(p_sort_code) THEN
        RAISE EXCEPTION 'Invalid sort code format (expected XX-XX-XX)';
    END IF;
    IF NOT validate_account_number(p_account_number) THEN
        RAISE EXCEPTION 'Invalid account number (expected 8 digits)';
    END IF;

    -- Duplicate check by email (if supplied)
    v_email_clean := NULLIF(LOWER(btrim(p_email)), '');
    IF v_email_clean IS NOT NULL THEN
        v_existing_customer := customer_exists(v_email_clean);
        IF v_existing_customer IS NOT NULL THEN
            RAISE EXCEPTION 'Customer with email % already exists (ID=%)', v_email_clean, v_existing_customer;
        END IF;
    END IF;

    -- Insert
    p_customer_id := generate_customer_id();

    INSERT INTO customer (
        customer_id, customer_fname, customer_sname,
        address_line1, address_line2, city, postcode, telephone,
        date_of_birth, email,
        bank_name, bank_address, sort_code, account_number, registration_date
    ) VALUES (
        p_customer_id, btrim(p_fname), btrim(p_sname),
        btrim(p_address_line1), NULLIF(btrim(p_address_line2), ''),
        btrim(p_city), UPPER(btrim(p_postcode)), btrim(p_telephone),
        p_dob, v_email_clean,
        btrim(p_bank_name), btrim(p_bank_address), p_sort_code, p_account_number, CURRENT_DATE
    );

    p_message := 'Customer registered successfully (ID=' || p_customer_id || ')';
    RAISE NOTICE '%', p_message;

EXCEPTION
    WHEN unique_violation THEN
        p_customer_id := NULL;
        p_message := 'Error: duplicate customer record';
        RAISE NOTICE '%', p_message;
    WHEN check_violation THEN
        p_customer_id := NULL;
        p_message := 'Error: validation failed - ' || SQLERRM;
        RAISE NOTICE '%', p_message;
    WHEN OTHERS THEN
        p_customer_id := NULL;
        p_message := 'Error: ' || SQLERRM;
        RAISE NOTICE '%', p_message;
END;
$$;


-- Procedure: purchase_product

CREATE OR REPLACE PROCEDURE purchase_product(
    p_customer_id VARCHAR,
    p_product_id VARCHAR,
    p_store_id VARCHAR,
    p_quantity INTEGER,
    p_delivery_date DATE,
    p_delivery_time TIME,
    INOUT p_transaction_id VARCHAR,
    INOUT p_total_amount NUMERIC,
    INOUT p_message VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_customer_ok BOOLEAN;
    v_product_ok BOOLEAN;
    v_store_ok BOOLEAN;
    v_product_price NUMERIC(10,2);
    v_available_stock INTEGER;
    v_slot_ok BOOLEAN;
    v_open TIME;
    v_close TIME;
BEGIN
    p_transaction_id := NULL;
    p_total_amount := 0;
    p_message := '';

    -- Mandatory checks
    IF p_customer_id IS NULL OR btrim(p_customer_id) = '' THEN RAISE EXCEPTION 'Customer ID is required'; END IF;
    IF p_product_id IS NULL OR btrim(p_product_id) = '' THEN RAISE EXCEPTION 'Product ID is required'; END IF;
    IF p_store_id IS NULL OR btrim(p_store_id) = '' THEN RAISE EXCEPTION 'Store ID is required'; END IF;
    IF p_quantity IS NULL OR p_quantity <= 0 THEN RAISE EXCEPTION 'Quantity must be > 0'; END IF;
    IF p_delivery_date IS NULL THEN RAISE EXCEPTION 'Delivery date is required'; END IF;
    IF p_delivery_time IS NULL THEN RAISE EXCEPTION 'Delivery time is required'; END IF;

    -- Validate entities exist
    SELECT EXISTS (SELECT 1 FROM customer WHERE customer_id = p_customer_id) INTO v_customer_ok;
    IF NOT v_customer_ok THEN RAISE EXCEPTION 'Customer % does not exist', p_customer_id; END IF;

    SELECT EXISTS (SELECT 1 FROM product WHERE product_id = p_product_id) INTO v_product_ok;
    IF NOT v_product_ok THEN RAISE EXCEPTION 'Product % does not exist', p_product_id; END IF;

    SELECT EXISTS (SELECT 1 FROM store WHERE store_id = p_store_id) INTO v_store_ok;
    IF NOT v_store_ok THEN RAISE EXCEPTION 'Store % does not exist', p_store_id; END IF;

    -- Validate delivery date/time
    IF p_delivery_date < CURRENT_DATE THEN
        RAISE EXCEPTION 'Delivery date cannot be in the past';
    END IF;
    IF p_delivery_date = CURRENT_DATE AND p_delivery_time <= CURRENT_TIME THEN
        RAISE EXCEPTION 'Delivery time must be in the future for same-day delivery';
    END IF;

    SELECT opening_time, closing_time INTO v_open, v_close
    FROM store WHERE store_id = p_store_id;

    IF p_delivery_time < v_open OR p_delivery_time > v_close THEN
        RAISE EXCEPTION 'Delivery time must be within store hours (% - %)', v_open, v_close;
    END IF;

    -- Lock per delivery slot to avoid race conditions within the same slot
    PERFORM pg_advisory_xact_lock(hashtext(p_store_id || '|' || p_delivery_date::text || '|' || p_delivery_time::text));

    -- Check delivery slot availability
    v_slot_ok := check_delivery_slot(p_store_id, p_delivery_date, p_delivery_time);
    IF NOT v_slot_ok THEN
        RAISE EXCEPTION 'Delivery slot % % at store % is fully booked', p_delivery_date, p_delivery_time, p_store_id;
    END IF;

    -- Lock stock row and check availability
    SELECT quantity
    INTO v_available_stock
    FROM warehouse_item
    WHERE product_id = p_product_id AND store_id = p_store_id
    FOR UPDATE;

    v_available_stock := COALESCE(v_available_stock, 0);
    IF v_available_stock = 0 THEN
        RAISE EXCEPTION 'Product % is not available at store %', p_product_id, p_store_id;
    END IF;
    IF v_available_stock < p_quantity THEN
        RAISE EXCEPTION 'Insufficient stock (requested %, available %)', p_quantity, v_available_stock;
    END IF;

    -- Calculate totals and insert transaction
    v_product_price := get_product_price(p_product_id);
    p_total_amount := v_product_price * p_quantity;
    p_transaction_id := generate_transaction_id();

    INSERT INTO "transaction" (
        transaction_id, customer_id, product_id, store_id, quantity,
        transaction_date, delivery_date, delivery_time, total_amount, transaction_status
    ) VALUES (
        p_transaction_id, p_customer_id, p_product_id, p_store_id, p_quantity,
        CURRENT_DATE, p_delivery_date, p_delivery_time, p_total_amount, 'Confirmed'
    );

    -- Decrement stock
    UPDATE warehouse_item
    SET quantity = quantity - p_quantity,
        last_updated = CURRENT_TIMESTAMP
    WHERE product_id = p_product_id AND store_id = p_store_id;

    p_message := FORMAT(
        'Purchase successful (transaction=%s, total=£%s, delivery=%s %s)',
        p_transaction_id,
        to_char(p_total_amount, 'FM999999990.00'),
        p_delivery_date,
        p_delivery_time
    );
    RAISE NOTICE '%', p_message;

EXCEPTION
    WHEN foreign_key_violation THEN
        p_transaction_id := NULL;
        p_total_amount := 0;
        p_message := 'Error: invalid reference (customer/product/store)';
        RAISE NOTICE '%', p_message;
    WHEN check_violation THEN
        p_transaction_id := NULL;
        p_total_amount := 0;
        p_message := 'Error: validation failed - ' || SQLERRM;
        RAISE NOTICE '%', p_message;
    WHEN OTHERS THEN
        p_transaction_id := NULL;
        p_total_amount := 0;
        p_message := 'Error: ' || SQLERRM;
        RAISE NOTICE '%', p_message;
END;
$$;

-- 8) Trigger (simple low-stock notice)

CREATE OR REPLACE FUNCTION check_low_stock()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_product_name VARCHAR(50);
    v_store_name VARCHAR(40);
    v_threshold CONSTANT INTEGER := 5;
BEGIN
    IF NEW.quantity < v_threshold THEN
        SELECT product_name INTO v_product_name FROM product WHERE product_id = NEW.product_id;
        SELECT store_name INTO v_store_name FROM store WHERE store_id = NEW.store_id;

        RAISE NOTICE 'Low stock: % (%), remaining=%',
            v_product_name, v_store_name, NEW.quantity;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_low_stock_alert ON warehouse_item;
CREATE TRIGGER trg_low_stock_alert
AFTER UPDATE OF quantity ON warehouse_item
FOR EACH ROW
EXECUTE FUNCTION check_low_stock();

-- 9) Views (basic reporting)

CREATE OR REPLACE VIEW vw_sales_by_store AS
SELECT
    s.store_id,
    s.store_name,
    s.city,
    t.transaction_date,
    COUNT(t.transaction_id) AS number_of_transactions,
    SUM(t.quantity) AS total_items_sold,
    SUM(t.total_amount) AS total_revenue
FROM store s
LEFT JOIN "transaction" t
    ON s.store_id = t.store_id
   AND t.transaction_status <> 'Cancelled'
GROUP BY s.store_id, s.store_name, s.city, t.transaction_date
ORDER BY t.transaction_date DESC, s.store_name;

CREATE OR REPLACE VIEW vw_store_summary AS
SELECT
    s.store_id,
    s.store_name,
    s.city,
    COUNT(t.transaction_id) AS total_transactions,
    COALESCE(SUM(t.total_amount), 0) AS total_revenue
FROM store s
LEFT JOIN "transaction" t
    ON s.store_id = t.store_id
   AND t.transaction_status <> 'Cancelled'
GROUP BY s.store_id, s.store_name, s.city
ORDER BY total_revenue DESC;

-- 10) Test procedure calls (valid + invalid)

-- Test 1: Register new customer (SUCCESS)
DO $$
DECLARE
    v_customer_id VARCHAR(3);
    v_message VARCHAR(300);
BEGIN
    RAISE NOTICE 'Test 1 - register_customer (valid)';

    CALL register_customer(
        'Thomas',
        'Anderson',
        '55 Matrix Road',
        'Floor 3',
        'London',
        'EC1A 1BB',
        '07700-111222',
        '1990-03-11'::DATE,
        'thomas.anderson@email.com',
        'Metro Bank',
        '1 Southampton Row, London',
        '23-05-80',
        '12348765',
        v_customer_id,
        v_message
    );

    RAISE NOTICE 'Returned: id=%, message=%', v_customer_id, v_message;
END $$;

-- Test 2: Register customer with invalid sort code (FAIL)
DO $$
DECLARE
    v_customer_id VARCHAR(3);
    v_message VARCHAR(300);
BEGIN
    RAISE NOTICE 'Test 2 - register_customer (invalid sort code)';

    CALL register_customer(
        'Jane',
        'Doe',
        '99 Test Street',
        NULL,
        'Manchester',
        'M1 1AA',
        '07700-333444',
        '1988-06-20'::DATE,
        'jane.doe@email.com',
        'Test Bank',
        'Test Address',
        '123456',        -- invalid
        '87654321',
        v_customer_id,
        v_message
    );
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Caught expected error: %', SQLERRM;
END $$;

-- Test 3: Purchase product (SUCCESS)
DO $$
DECLARE
    v_transaction_id VARCHAR(3);
    v_total NUMERIC(10,2);
    v_message VARCHAR(300);
BEGIN
    RAISE NOTICE 'Test 3 - purchase_product (valid)';

    CALL purchase_product(
        'C01',
        'P01',
        'S01',
        1,
        (CURRENT_DATE + INTERVAL '7 days')::DATE,
        '14:00'::TIME,
        v_transaction_id,
        v_total,
        v_message
    );

    RAISE NOTICE 'Returned: transaction=%, total=£%, message=%', v_transaction_id, v_total, v_message;
END $$;

-- Test 4: Purchase with insufficient stock (FAIL)
DO $$
DECLARE
    v_transaction_id VARCHAR(3);
    v_total NUMERIC(10,2);
    v_message VARCHAR(300);
BEGIN
    RAISE NOTICE 'Test 4 - purchase_product (insufficient stock)';

    CALL purchase_product(
        'C02',
        'P04', -- Pearl Drum Kit
        'S04', -- Edinburgh has 1
        1000,
        (CURRENT_DATE + INTERVAL '5 days')::DATE,
        '11:00'::TIME,
        v_transaction_id,
        v_total,
        v_message
    );
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Caught expected error: %', SQLERRM;
END $$;

-- Test 5: Purchase with invalid customer (FAIL)
DO $$
DECLARE
    v_transaction_id VARCHAR(3);
    v_total NUMERIC(10,2);
    v_message VARCHAR(300);
BEGIN
    RAISE NOTICE 'Test 5 - purchase_product (invalid customer)';

    CALL purchase_product(
        'ZZZ',
        'P01',
        'S01',
        1,
        (CURRENT_DATE + INTERVAL '3 days')::DATE,
        '15:00'::TIME,
        v_transaction_id,
        v_total,
        v_message
    );
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Caught expected error: %', SQLERRM;
END $$;

-- 11) Quick verification queries

SELECT 'Customers' AS info;
SELECT customer_id, customer_fname, customer_sname, email, registration_date
FROM customer
ORDER BY customer_id;

SELECT 'Stock levels (sample)' AS info;
SELECT p.product_id, p.product_name, s.store_name, w.quantity
FROM product p
JOIN warehouse_item w ON p.product_id = w.product_id
JOIN store s ON w.store_id = s.store_id
ORDER BY p.product_id, s.store_id;

SELECT 'Transactions' AS info;
SELECT
    t.transaction_id,
    (c.customer_fname || ' ' || c.customer_sname) AS customer,
    p.product_name,
    s.store_name,
    t.quantity,
    t.total_amount,
    t.delivery_date,
    t.delivery_time,
    t.transaction_status
FROM "transaction" t
JOIN customer c ON t.customer_id = c.customer_id
JOIN product p ON t.product_id = p.product_id
JOIN store s ON t.store_id = s.store_id
ORDER BY t.transaction_date DESC, t.transaction_id;

SELECT 'Store sales summary' AS info;
SELECT * FROM vw_store_summary;

-- END


