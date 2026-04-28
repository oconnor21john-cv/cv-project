# Task 1: Smith and Co Second-Hand Bookshop
## Normalisation Table

### Analysis of the Customer History Form

From the sample customer history form, the following data elements have been identified:

**Customer Details (Level 1 - Single values per customer):**
- Customer Name
- Customer Email
- Address Line 1
- Address Line 2
- Address Line 3
- Postcode

**Purchase History (Level 2 - Repeating group):**
- Author ID
- Author Name
- Book Title
- Purchase Date
- Sales Price

---

## Normalisation Table (UNF to 3NF)

### Assumptions and Identifiers (to match the scenario)
- The form does not include explicit IDs for customers/books/transactions, so the design introduces surrogate identifiers:
  - `customer_id` to uniquely identify a customer (email may change).
  - `copy_id` to uniquely identify a physical copy of a second-hand book.
  - `transaction_id` to uniquely identify each buy/sell event.
- A book “work/title” is identified by the combination (`author_id`, `book_title`). This avoids assuming titles are globally unique.
- The scenario states books may be bought and sold several times. To represent the same physical book being bought back later, transactions must reference a **book copy** (`copy_id`), not just a title.
- The provided form shows a “Purchase History” list; the scenario also requires tracking **both** shop purchases (buying from customer) and shop sales (selling to customer). This is represented using `transaction_type` ∈ {`PURCHASE`, `SALE`}.

### UNF (Unnormalised form)

- Customer details stored together: Customer_name, Customer_email, Address_line1, Address_line2, Address_line3, Postcode.
- Purchase history stored as a repeating group inside the same customer record: Author_id, Author_name, Book_title, Purchase_date, Sales_price.
- Result: customer details are duplicated for every purchase row.

### 1NF (First Normal Form)

- Remove the repeating group so each row holds one purchase/transaction event (atomic values only).
- 1NF relation (one row per history line):
  - `CUSTOMER_HISTORY_1NF(customer_email, customer_name, address_line1, address_line2, address_line3, postcode, author_id, author_name, book_title, transaction_date, sales_price)`
- Candidate key for the 1NF “history line” (no ID on the form):
  - \(`customer_email`, `author_id`, `book_title`, `transaction_date`\)

### 2NF (Second Normal Form)

- Remove partial dependencies by separating AUTHOR and BOOK data out of the transaction rows.
- Partial dependencies in the 1NF relation (examples):
  - `customer_email → customer_name, address_line1, address_line2, address_line3, postcode`
  - `author_id → author_name`
- Decompose into (up to 2NF):
  - `CUSTOMER(customer_id PK, customer_email, customer_name, address_line1, address_line2, address_line3, postcode)`
  - `AUTHOR(author_id PK, author_name)`
  - `BOOK_WORK(author_id PK/FK, book_title PK)`
  - `TRANSACTION_2NF(transaction_id PK, customer_id FK, author_id FK, book_title FK, transaction_date, sales_price, transaction_type)`
- Note: using the composite key `BOOK_WORK(author_id, book_title)` avoids assuming titles are globally unique.

### 3NF (Third Normal Form)

- Remove transitive dependencies (non-key attributes depend only on the key).
- Ensure the design matches the scenario “books may be bought and sold several times” by tracking **physical copies**:
  - `BOOK_COPY(copy_id PK, author_id FK, book_title FK)`
- Final 3NF set:
  - `CUSTOMER(customer_id PK, customer_email, customer_name, address_line1, address_line2, address_line3, postcode)`
  - `AUTHOR(author_id PK, author_name)`
  - `BOOK_WORK(author_id PK/FK, book_title PK)`
  - `BOOK_COPY(copy_id PK, author_id FK, book_title FK)`
  - `TRANSACTION(transaction_id PK, customer_id FK, copy_id FK, transaction_date, sales_price, transaction_type)`

**Key:**
- **<u>Underlined Bold</u>** = Primary Key (PK)
- *Asterisk* = Foreign Key (FK)

---

## Final 3NF Entity Definitions

### CUSTOMER
| Attribute | Key Type | Description |
|-----------|----------|-------------|
| <u>**customer_id**</u> | PK | Unique identifier for each customer |
| customer_name | | Full name of the customer |
| customer_email | | Email address of the customer |
| address_line1 | | First line of address |
| address_line2 | | Second line of address (optional) |
| address_line3 | | City/Town |
| postcode | | Postal code |

### AUTHOR
| Attribute | Key Type | Description |
|-----------|----------|-------------|
| <u>**author_id**</u> | PK | Unique identifier for each author |
| author_name | | Full name of the author |

### BOOK_WORK
| Attribute | Key Type | Description |
|-----------|----------|-------------|
| <u>**author_id**</u> | PK, FK | References AUTHOR(author_id) |
| <u>**book_title**</u> | PK | Title of the book (with author_id identifies the work) |

### BOOK_COPY
| Attribute | Key Type | Description |
|-----------|----------|-------------|
| <u>**copy_id**</u> | PK | Unique identifier for a physical (second-hand) copy |
| *author_id* | FK | Part of composite FK to BOOK_WORK(author_id, book_title) |
| *book_title* | FK | Part of composite FK to BOOK_WORK(author_id, book_title) |

### TRANSACTION
| Attribute | Key Type | Description |
|-----------|----------|-------------|
| <u>**transaction_id**</u> | PK | Unique identifier for each transaction |
| *customer_id* | FK | References CUSTOMER(customer_id) |
| *copy_id* | FK | References BOOK_COPY(copy_id) |
| transaction_date | | Date of the purchase/sale |
| sales_price | | Price of the transaction |
| transaction_type | | Type: 'PURCHASE' (shop buys from customer) or 'SALE' (shop sells to customer) |

---

## Functional Dependencies (FDs) used
- `customer_id → customer_email, customer_name, address_line1, address_line2, address_line3, postcode`
- `author_id → author_name`
- (`author_id`, `book_title`) is the key of BOOK_WORK
- `copy_id → author_id, book_title`
- `transaction_id → customer_id, copy_id, transaction_date, sales_price, transaction_type`

---

## Normalisation Process Explanation

### UNF → 1NF (First Normal Form)
- Removed repeating groups (purchase history items)
- Created a separate 1NF relation where each row stores one history line
- Ensured all attributes contain atomic values
- Identified a candidate key for the 1NF history line (since the form shows no explicit transaction ID)

### 1NF → 2NF (Second Normal Form)
- Removed partial dependencies
- Customer attributes depend on customer (email/id), not the full 1NF candidate key
- Author_name depends on author_id
- Introduced BOOK_WORK to store book_title and its author once

### 2NF → 3NF (Third Normal Form)
- Removed transitive dependencies
- Ensured no non-key attribute depends on another non-key attribute
- Ensured the design matches the “bought and sold several times” requirement by linking transactions to a physical `BOOK_COPY`
- CUSTOMER, AUTHOR, BOOK_WORK, BOOK_COPY store only attributes dependent on their keys
- TRANSACTION links customer and copy and stores only transaction-specific attributes

---

## Relationship Summary

```
AUTHOR (1) ----< (M) BOOK_WORK (1) ----< (M) BOOK_COPY (1) ----< (M) TRANSACTION (M) >---- (1) CUSTOMER
```
- One CUSTOMER can have many TRANSACTIONS
- One TRANSACTION involves one BOOK_COPY
- One BOOK_COPY is of exactly one BOOK_WORK (title)
- One BOOK_WORK has one AUTHOR; one AUTHOR can write many BOOK_WORK rows
- A BOOK_COPY can appear in many TRANSACTIONS over time (bought/sold multiple times)

---

## Normalisation Table (template headings)

Key marking used below (to match the template):
- Primary keys are shown as <u>**underlined bold**</u>
- Foreign keys are shown in *italics*

<table>
  <colgroup>
    <col style="width: 26%;">
    <col style="width: 10%;">
    <col style="width: 16%;">
    <col style="width: 20%;">
    <col style="width: 28%;">
  </colgroup>
  <thead>
    <tr>
      <th>Unnormalized</th>
      <th>UNF Level</th>
      <th>1NF</th>
      <th>2NF</th>
      <th>3NF</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>customer_name</td><td align="center">1</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>CUSTOMER</code></td><td><code>CUSTOMER</code></td></tr>
    <tr><td>customer_email</td><td align="center">1</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>CUSTOMER</code></td><td><code>CUSTOMER</code></td></tr>
    <tr><td>address_line1</td><td align="center">1</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>CUSTOMER</code></td><td><code>CUSTOMER</code></td></tr>
    <tr><td>address_line2</td><td align="center">1</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>CUSTOMER</code></td><td><code>CUSTOMER</code></td></tr>
    <tr><td>address_line3</td><td align="center">1</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>CUSTOMER</code></td><td><code>CUSTOMER</code></td></tr>
    <tr><td>postcode</td><td align="center">1</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>CUSTOMER</code></td><td><code>CUSTOMER</code></td></tr>

    <tr><td>author_id</td><td align="center">2</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>AUTHOR</code>, <code>BOOK_WORK</code>, <code>TRANSACTION_2NF</code></td><td><code>AUTHOR</code>, <code>BOOK_WORK</code>, <code>BOOK_COPY</code>, <code>TRANSACTION</code></td></tr>
    <tr><td>author_name</td><td align="center">2</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>AUTHOR</code></td><td><code>AUTHOR</code></td></tr>
    <tr><td>book_title</td><td align="center">2</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>BOOK_WORK</code>, <code>TRANSACTION_2NF</code></td><td><code>BOOK_WORK</code>, <code>BOOK_COPY</code>, <code>TRANSACTION</code></td></tr>
    <tr><td>purchase_date</td><td align="center">2</td><td><code>CUSTOMER_HISTORY_1NF</code> (as <code>transaction_date</code>)</td><td><code>TRANSACTION_2NF</code></td><td><code>TRANSACTION</code></td></tr>
    <tr><td>sales_price</td><td align="center">2</td><td><code>CUSTOMER_HISTORY_1NF</code></td><td><code>TRANSACTION_2NF</code></td><td><code>TRANSACTION</code></td></tr>

    <tr><td>(derived) customer_id</td><td align="center">-</td><td>-</td><td><u><b>customer_id</b></u> in <code>CUSTOMER</code>; <i>customer_id</i> in <code>TRANSACTION_2NF</code></td><td><u><b>customer_id</b></u> in <code>CUSTOMER</code>; <i>customer_id</i> in <code>TRANSACTION</code></td></tr>
    <tr><td>(derived) transaction_id</td><td align="center">-</td><td>-</td><td><u><b>transaction_id</b></u> in <code>TRANSACTION_2NF</code></td><td><u><b>transaction_id</b></u> in <code>TRANSACTION</code></td></tr>
    <tr><td>(derived) copy_id</td><td align="center">-</td><td>-</td><td>-</td><td><u><b>copy_id</b></u> in <code>BOOK_COPY</code>; <i>copy_id</i> in <code>TRANSACTION</code></td></tr>
    <tr><td>(scenario) transaction_type</td><td align="center">-</td><td>-</td><td><code>TRANSACTION_2NF</code></td><td><code>TRANSACTION</code></td></tr>
  </tbody>
</table>


