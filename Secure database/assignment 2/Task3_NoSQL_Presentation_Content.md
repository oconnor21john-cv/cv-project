# Task 3: NoSQL Document Store Presentation Content

## PowerPoint Outline for 5-10 Minute Screencast

This document provides suggested content for your NoSQL Document Store presentation about Millie's Musical Emporium.

---

## Slide 1: Title Slide

**Title:** The Benefits of NoSQL Document Stores for Millie's Musical Emporium

**Focus:** Using the Task 1 PostgreSQL prototype as the baseline for comparison


---

## Slide 2: What is a NoSQL Document Store? (Overview 1/2)

### Key Points:
- **Definition**: A NoSQL document store is a non-relational database that stores data as semi-structured documents (typically JSON or BSON format) rather than in traditional rows and columns (Sadalage and Fowler, 2012).

- **Document Structure**: Data is organised into documents containing key-value pairs, arrays, and nested documents, allowing for flexible schemas.

- **Examples**: Common document stores include MongoDB, CouchDB, Amazon DocumentDB, and Firebase Firestore.

### Speaker Notes:
"In Task 1, MME is modelled in PostgreSQL using separate tables for customer, products, stock and transactions. A document store takes a different approach: it stores records as documents (usually JSON). The key idea is that related data can be kept together in one document, and the database is less strict about enforcing one fixed schema across all records. In this screencast I’ll use our PostgreSQL prototype as the reference point, and then discuss when a document store could add value for MME."

---

## Slide 3: How Document Stores Work (Overview 2/2)

### Key Points:
- **Schema Flexibility**: Documents in the same collection can have different fields - no need for ALTER TABLE operations (Chodorow, 2013).

- **Data Model Example for MME**:
```json
{
  "customer_id": "C01",
  "name": { "first": "Niamh", "last": "O'Neill" },
  "address": {
    "line1": "12 Ardenlee Avenue",
    "city": "Belfast",
    "postcode": "BT6 8QX"
  },
  "purchases": [
    { "transaction_id": "T01", "product_id": "P01", "date": "2025-12-01", "qty": 1, "amount": 199.99 }
  ]
}
```

- **Collections**: Documents are grouped into collections (equivalent to tables), but without enforced schemas.

### Speaker Notes:
"This is a simplified example of what a customer document could look like. Compared to our PostgreSQL design, where customer and transaction data are separate tables linked by foreign keys, a document store can embed purchase history directly inside the customer document. That can reduce the need for joins for common screens like 'my account' or 'my orders'. The trade-off is duplication and consistency: if product prices or product names change, you need a strategy to avoid stale embedded data."

---

## Slide 4: Benefits for MME (Critical Discussion 1/2)

### Key Points:

**1. Flexible Schema Evolution**
- In PostgreSQL, adding fields typically means schema changes and migration planning
- In a document store, MME can add new fields gradually (e.g., loyalty points, instrument preferences, lesson subscriptions)
- "Schema-less design allows for rapid iteration and adaptation to business needs" (Banker et al., 2016)

**2. Improved Read Performance**
- For read-heavy pages (account overview, order history), data can be retrieved as one document
- Fewer joins can reduce query complexity for certain user journeys
- Significant performance improvement for e-commerce applications (Han et al., 2011)

**3. Horizontal Scalability**
- Built-in sharding distributes data across multiple servers
- MME can scale to handle increased customer base and transactions
- Systematic review evidence highlights stronger horizontal scaling characteristics in NoSQL systems (Khan et al., 2023)

### Speaker Notes:
"For MME, schema change is a realistic pressure point. In PostgreSQL, adding a new customer attribute or a new product attribute is straightforward, but it still requires a controlled migration and careful testing if the database is live. A document store can be more forgiving: you can add a new field to new documents first, and backfill old documents later if needed. 

On performance, the benefit is not 'NoSQL is faster' in general; it depends on the access pattern. If the common requirement is to fetch a customer profile plus recent purchases, embedding can reduce joins and simplify application code. However, for reporting-style queries across many stores and dates, PostgreSQL remains strong.

Finally, on scaling, document stores are often designed to spread data across multiple servers. That can matter if MME grows into a larger online business with big seasonal spikes in traffic, although PostgreSQL can also scale using replicas and partitioning depending on the workload."

---

## Slide 5: Benefits for MME (Critical Discussion 2/2)

### Key Points:

**4. Developer Productivity**
- JSON format maps directly to programming language objects
- Less “mapping” between application objects and database tables
- Faster development cycles for web and mobile applications (Plugge et al., 2010)

**5. High Availability**
- Built-in replication ensures data redundancy
- Automatic failover if a server fails
- Critical for 24/7 e-commerce operations

### Critical Considerations (Balanced View):

**Potential Drawbacks:**
- **Integrity vs flexibility**: PostgreSQL enforces relationships with foreign keys; document stores often rely on application checks or schema validation rules
- **Transactions**: PostgreSQL provides strong ACID guarantees by default; some document stores support multi-document transactions, but the operational and performance costs can be higher than keeping updates within one document (Schultz and Demirbas, 2025)
- **Complex reporting**: queries like “sales by store between dates” are very natural in SQL; document aggregation can be more verbose and harder to maintain
- **Storage overhead**: denormalising data can duplicate values, which increases storage and can make updates harder

### Speaker Notes:
"It’s important to be clear about what we give up. In our Task 1 PostgreSQL model, foreign keys and constraints help prevent inconsistent data (for example, a transaction referencing a non-existent customer or product). In a document store, you typically need to enforce this in application logic, or accept a looser consistency model.

Transactions are another key difference. PostgreSQL makes multi-table updates routine. With a purchase, we can insert a transaction row and reduce the stock quantity safely in the same transaction. In document databases, the simplest approach is to design so the key change happens inside one document, because that is the easiest way to guarantee “all-or-nothing” updates. If the design needs multiple documents updated together, some products support that, but it is more complex and can be slower under load.

For MME’s management reporting, the relational model is still very attractive. Aggregating sales by store, date, and product category is exactly what SQL excels at. So a sensible recommendation is not to replace PostgreSQL completely, but to consider a hybrid approach where each database is used for what it is best at."

---

## Slide 6: Summary

### Key Takeaways:

| Aspect | Benefit for MME |
|--------|-----------------|
| **Schema Flexibility** | Rapid adaptation to new products and features |
| **Performance** | Faster customer data retrieval |
| **Scalability** | Support for business growth |
| **Development** | Quicker feature implementation |

### Conclusion:
NoSQL document stores offer compelling benefits for MME, particularly for customer-facing applications requiring flexibility and scalability. However, a **polyglot persistence** approach - using PostgreSQL for financial reporting alongside a document store for product catalogues/customer profiles - may provide the optimal solution (Sadalage and Fowler, 2012; Lajam and Mohammed, 2022).

### Speaker Notes:
"In conclusion, document stores can help MME where the system is user-facing and change is frequent: customer profiles, preferences, browsing history, and parts of the product catalogue that evolve quickly. PostgreSQL should still be the default choice for the structured core of the business: stock control, transactions, and management reporting, because integrity and querying are strong and well understood.

The best recommendation is polyglot persistence. Keep PostgreSQL as the system of record, and add a document store where it reduces friction or improves user experience. For example, a document store could store a customer “account view” document that is fast to read (profile plus recent purchases), while PostgreSQL remains the authoritative source for the underlying transactional data."

---

## Slide 7: References (1/2)

**References:**

Banker, K., Bakkum, P., Verch, S., Garrett, D. and Hawkins, T. (2016) *MongoDB in Action*. 2nd edn. Shelter Island: Manning Publications.

Cattell, R. (2011) 'Scalable SQL and NoSQL data stores', *ACM SIGMOD Record*, 39(4), pp. 12-27. doi: 10.1145/1978915.1978919.

Chodorow, K. (2013) *MongoDB: The Definitive Guide*. 2nd edn. Sebastopol: O'Reilly Media.

Han, J., Haihong, E., Le, G. and Du, J. (2011) 'Survey on NoSQL database', *2011 6th International Conference on Pervasive Computing and Applications*, Port Elizabeth, pp. 363-366. doi: 10.1109/ICPCA.2011.6106531.

Khan, W., Kumar, T., Zhang, C., Raj, K., Roy, A.M. and Luo, B. (2023) 'SQL and NoSQL database software architecture performance analysis and assessments—A systematic literature review', *Big Data and Cognitive Computing*, 7(2), 97. doi: 10.3390/bdcc7020097.

---

## Slide 8: References (2/2)

**References (continued):**

Lajam, O. and Mohammed, S. (2022) 'Revisiting polyglot persistence: From principles to practice', *International Journal of Advanced Computer Science and Applications*, 13(5), pp. 872–882.

MongoDB (2024) *MongoDB Documentation*. Available at: https://docs.mongodb.com/ (Accessed: 4 February 2026).

Schultz, W. and Demirbas, M. (2025) 'Design and modular verification of distributed transactions in MongoDB', *Proceedings of the VLDB Endowment*, 18(12), pp. 5045–5058. doi: 10.14778/3750601.3750626.

Plugge, E., Membrey, P. and Hawkins, T. (2010) *The Definitive Guide to MongoDB*. Berkeley: Apress.

Sadalage, P.J. and Fowler, M. (2012) *NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence*. Upper Saddle River: Addison-Wesley Professional.

---

## Recording Tips for Screencast

1. **Duration**: Aim for 7-8 minutes (not exceeding 10 minutes)
2. **Software**: Use Screencast-O-Matic or OBS as recommended
3. **Pace**: Speak clearly and at a moderate pace
4. **Structure**: Follow the slides in order
5. **Critical Analysis**: Ensure you discuss both benefits AND limitations
6. **Harvard Referencing**: Cite sources verbally and on slides
7. **Export**: Save as .mp4 format

---

## Additional Academic Sources to Consider

- Strauch, C. (2011) *NoSQL Databases*. Stuttgart: Stuttgart Media University.
- Leavitt, N. (2010) 'Will NoSQL databases live up to their promise?', *Computer*, 43(2), pp. 12-14.
- Moniruzzaman, A.B.M. and Hossain, S.A. (2013) 'NoSQL database: New era of databases for big data analytics', *International Journal of Database Theory and Application*, 6(4), pp. 1-14.

