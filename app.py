# Configuration
from flask import *
import os
import flask_mysqldb

app = Flask(__name__)

# Continue with database initialization using secret username / password.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CarbonCrash'
app.config['MYSQL_DB'] = 'invoicetracking'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config['SECRET_KEY'] = 'secret!'
mysql = flask_mysqldb.MySQL(app)

# Routes 

@app.route('/', methods=["POST"])
def home():
    data = request.json
    group = data.get("group")
    
    ar_columns, ar_cursor = ar_invoices(group)
    ap_columns, ap_cursor = ap_invoices(group)
        
    json_response = {
        "ar_columns": ar_columns,
        "ar_cursor": ar_cursor,
        "ap_columns": ap_columns,
        "ap_cursor": ap_cursor
    }

    return json_response

def ar_invoices(group):
    if group == "invoice":
        columns, cursor = ar_invoices_invoice()
    elif group == "customervendor":
        columns, cursor = ar_invoices_customer()
    elif group == "invoicedate":
        columns, cursor = ar_invoices_invoicedate()
    elif group == "duedate":
        columns, cursor = ar_invoices_duedate()
    return columns, cursor

def ar_invoices_invoice():
    columns = ("Invoice", "Amount")
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT
            Invoice AS "Invoice",
            SUM(Amount) AS "Amount"
        FROM ARInvoices
        GROUP BY
            Invoice;
        """)
    return columns, cursor.fetchall()

def ar_invoices_customer():
    columns = ("Customer Name", "Amount")
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT
            CustomerName AS "Customer Name",
            SUM(Amount) AS "Amount"
        FROM ARInvoices
        GROUP BY
            CustomerName;
        """)
    return columns, cursor.fetchall()

def ar_invoices_invoicedate():
    columns = ("Invoice Date", "Amount")
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT
            InvoiceDate AS "Invoice Date",
            SUM(Amount) AS "Amount"
        FROM ARInvoices
        GROUP BY
            InvoiceDate;
        """)
    return columns, cursor.fetchall()

def ar_invoices_duedate():
    columns = ("Due Date", "Amount")
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT
            DueDate AS "Due Date",
            SUM(Amount) AS "Amount"
        FROM ARInvoices
        GROUP BY
            DueDate;
        """)
    return columns, cursor.fetchall()

def ap_invoices(group):
    if group == "invoice":
        columns, cursor = ap_invoices_invoice()
    elif group == "customervendor":
        columns, cursor = ap_invoices_vendor()
    elif group == "invoicedate":
        columns, cursor = ap_invoices_invoicedate()
    elif group == "duedate":
        columns, cursor = ap_invoices_duedate()
    return columns, cursor

def ap_invoices_invoice():
    columns = ("Invoice", "Amount")
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT
            Invoice AS "Invoice",
            SUM(Amount) AS "Amount"
        FROM APInvoices
        GROUP BY
            Invoice;
        """)
    return columns, cursor.fetchall()

def ap_invoices_vendor():
    columns = ("Vendor Name", "Amount")
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT
            VendorName AS "Vendor Name",
            SUM(Amount) AS "Amount"
        FROM APInvoices
        GROUP BY
            VendorName;
        """)
    return columns, cursor.fetchall()

def ap_invoices_invoicedate():
    columns = ("Invoice Date", "Amount")
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT
            InvoiceDate AS "Invoice Date",
            SUM(Amount) AS "Amount"
        FROM APInvoices
        GROUP BY
            InvoiceDate;
        """)
    return columns, cursor.fetchall()

def ap_invoices_duedate():
    columns = ("Due Date", "Amount")
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT
            DueDate AS "Due Date",
            SUM(Amount) AS "Amount"
        FROM APInvoices
        GROUP BY
            DueDate;
        """)
    return columns, cursor.fetchall()

# Listener

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 50003)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port)