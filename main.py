# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql(
    """SELECT firstName, lastName
    FROM employees AS e
    JOIN offices AS o ON e.officeCode = o.officeCode
    WHERE city = 'Boston'
    """, 
        conn,
)      
                        
# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql(
    """SELECT *
    FROM offices
    WHERE officeCode NOT IN (
        SELECT DISTINCT officeCode
        FROM employees
        WHERE officeCode IS NOT NULL
        )
    """,
        conn,
)    

# STEP 3
# Replace None with your code
df_employee = pd.read_sql(
    """SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees AS e
    LEFT JOIN offices AS o
    ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
    
    """,
        conn,
)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql(
    """
    SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber 
    FROM customers 
    WHERE customerNumber NOT IN (
        SELECT DISTINCT customerNumber 
        FROM orders
    )
    ORDER BY contactLastName
""",
    conn,
)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql(
    """
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate 
    FROM customers AS c
    JOIN payments AS p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""",
    conn,
)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql(
    """
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS customer_count
    FROM employees AS e
    JOIN customers AS c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY customer_count DESC
""",
    conn,
)    

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql(
    """
    SELECT p.productName, COUNT(od.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
    FROM products AS p
    JOIN orderDetails AS od ON p.productCode = od.productCode
    GROUP BY p.productCode
    ORDER BY totalunits DESC
""",
    conn,
) 

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql(
    """
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products AS p
    JOIN orderDetails AS od ON p.productCode = od.productCode
    JOIN orders AS o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    ORDER BY numpurchasers DESC
""",
    conn,
)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql(
    """
    SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
    FROM offices AS o
    JOIN employees AS e ON o.officeCode = e.officeCode
    JOIN customers AS c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode
""",
    conn,
)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql(
    """
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
    FROM employees AS e
    JOIN offices AS o ON e.officeCode = o.officeCode
    JOIN customers AS c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders AS ord ON c.customerNumber = ord.customerNumber
    JOIN orderDetails AS od ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT p.productCode
        FROM products AS p
        JOIN orderDetails AS od2 ON p.productCode = od2.productCode
        JOIN orders AS ord2 ON od2.orderNumber = ord2.orderNumber
        GROUP BY p.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName, e.firstName
""",
    conn,
)

conn.close()