Task 1: Smith and Co Second-Hand Bookshop
Short Report: Potential Database Attacks

Introduction

Smith and Co’s second-hand bookshop database is a realistic target because it holds a mix of personal data (names, emails and addresses) and commercial data (what was bought/sold, when, and for how much). Even if the business is relatively small, the data is still useful for criminals: customer contact details support phishing and fraud, while transaction and pricing history can reveal sales patterns and business performance (Splunk, n.d.).

Attack 1: SQL Injection

Why the Database Might Be a Target

In practice, the bookshop is likely to use a website or internal admin screen to do everyday tasks such as looking up customers, searching titles/authors, and recording purchases/sales. If those screens are connected directly to the database and user input is not handled safely, they become a convenient entry point for SQL injection. Small businesses also often have fewer resources for secure development and testing, which increases the chance that issues like this slip through (OWASP, n.d.).

Type of Attack

SQL injection (SQLi) happens when an application builds a database query using unsanitised input. For example, if a customer-search box takes whatever is typed and stitches it into a SQL statement, an attacker can inject extra SQL to change what the query does (Halfond et al., 2006). A simple example is entering something like `' OR '1'='1' --` into a login or search field so the condition becomes “always true”, which can lead to authentication bypass or wider data exposure. More advanced approaches (e.g. UNION-based SQLi) can be used to pull data from other tables entirely (Halfond et al., 2006).

Data That Might Be Extracted

If successful, SQL injection could expose the customer table (names, emails and addresses) and the customer history information shown on the form (what titles were bought/sold, dates and prices). That combination is valuable for targeted scams because a message can be personalised with “real” details. It could also reveal business-sensitive information such as typical selling prices and which titles/copies are repeatedly bought back and resold in the second-hand model. If staff/admin login details are stored in the same database, password hashes could also be extracted and cracked offline (Halfond et al., 2006).

Attack 2: Data Breach via Insider Threat

Why the Database Might Be a Target

Unlike many attacks, an insider does not need to “break in” if they already have legitimate access (even if it is only partial). In this scenario, staff may need access to customer records and transaction history to run the shop. That makes the database attractive for misuse because the data can be copied quickly and quietly: customer contact details can be used for spam or phishing, and the shop’s buying/selling patterns could be useful to competitors. Motivation could be financial (selling a list), resentment, or being manipulated by an external attacker (Verizon, 2023).

Type of Attack

An insider threat is when someone with authorised access uses it in an unauthorised way (Ponemon Institute, 2022). For Smith and Co, that could be a staff member exporting customer records before leaving, taking screenshots/printouts, or running “legitimate” database queries that pull far more data than their job requires. It could also involve a staff account being used under pressure or bribery. These incidents can be harder to detect because the activity may look normal in the system logs unless auditing and permissions are strong (Ponemon Institute, 2022).

Data That Might Be Extracted

An insider could copy the full customer list (names, emails, addresses and postcodes) and the history of purchases/sales that sits behind the “customer history” form. They could also extract inventory-related information (authors/titles held, typical prices, and what sells fastest), which is commercially sensitive. Because it’s a second-hand business, repeated buy-back/resale history for particular copies/titles can reveal which stock is most profitable over time, and that kind of pattern data is valuable for both competitors and targeted marketing (Verizon, 2023).

Conclusion

Overall, SQL injection is a credible technical risk if Smith and Co relies on a web/admin front end that is not securely coded, while insider misuse is a people/process risk because staff access is necessary for day-to-day operations. Practical controls include parameterised queries and strong input handling to reduce SQLi exposure (OWASP, n.d.), alongside least-privilege access, audit logging, and staff awareness training to reduce and detect insider misuse (Ponemon Institute, 2022).

References

Halfond, W.G.J., Viegas, J. and Orso, A. (2006) 'A classification of SQL injection attacks and countermeasures'. In: Proceedings of the IEEE International Symposium on Secure Software Engineering (ISSSE 2006). pp. 13–15. Available at: `https://faculty.cc.gatech.edu/~orso/papers/halfond.viegas.orso.ISSSE06.pdf` (Accessed: 20 January 2026).

OWASP (n.d.) SQL Injection. Available at: `https://owasp.org/www-community/attacks/SQL_Injection` (Accessed: 19 January 2026).

Ponemon Institute (2022) 2022 Cost of Insider Threats: Global Report. Proofpoint. Available at: `https://www.proofpoint.com/us/resources/threat-reports/cost-of-insider-threats` (Accessed: 21 January 2026).

Splunk (n.d.) Data Security Today: Threats, Techniques and Solutions. Available at: `https://www.splunk.com/en_us/blog/learn/data-security.html` (Accessed: 21 January 2026).

Verizon (2023) 2023 Data Breach Investigations Report. Available at: `https://www.verizon.com/business/resources/Td36/reports/2023-data-breach-investigations-report-dbir.pdf` (Accessed: 21 January 2026).

Word Count: Approximately 520 words

