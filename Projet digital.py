import sqlite3
import requests

dbase = sqlite3.connect('database_proj.db', isolation_level=None)
print('Database opened')

dbase.execute('''DROP TABLE IF EXISTS customer''')
dbase.execute('''DROP TABLE IF EXISTS companies''')
dbase.execute('''DROP TABLE IF EXISTS quote''')
dbase.execute('''DROP TABLE IF EXISTS invoice''')
dbase.execute('''DROP TABLE IF EXISTS subscription''')

dbase.execute(''' 
            CREATE TABLE IF NOT EXISTS customer(
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            family_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            bank_account INTEGER NOT NULL) 
            ''')

dbase.execute(''' 
        CREATE TABLE IF NOT EXISTS companies(
            VAT_id INTEGER PRIMARY KEY NOT NULL,
            company_name TEXT NOT NULL,
            bank_account INT NOT NULL,
            city TEXT NOT NULL,
            zip_code INTEGER NOT NULL,
            street_name TEXT NOT NULL,
            box_number INTEGER NOT NULL) 
            ''')

dbase.execute(''' 
        CREATE TABLE IF NOT EXISTS invoice(
            reference_number INTEGER PRIMARY KEY NOT NULL,
            subscript_id INTEGER NOT NULL,
            payment_status BOOL,
            FOREIGN KEY (subscript_id) REFERENCES companies(subscription_id))
            ''')


dbase.execute (''' 
        CREATE TABLE IF NOT EXISTS subscription(
            subscription_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            companies_id INTEGER NOT NULL,
            custom_id INTEGER NOT NULL,
            activation_status BOOL NOT NULL,
            FOREIGN KEY (companies_id) REFERENCES companies(VAT_id),
            FOREIGN KEY (custom_id) REFERENCES customer(customer_id))
            ''')

dbase.execute (''' 
        CREATE TABLE IF NOT EXISTS quote(
            quote_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            sub_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price FLOAT NOT NULL,
            currency STRING NOT NULL,
            FOREIGN KEY (sub_id) REFERENCES subscription(subscription_id))
            ''')

def insert_in_customer(family_name, first_name, bank_account):
    dbase.execute(
                    ''' 
                    INSERT INTO customer(family_name, first_name, bank_account)
                    VALUES(?,?,?)
                    ''', (family_name, first_name, bank_account))

def insert_in_companies(VAT_id, company_name, bank_account,city,zip_code,street_name,box_number):
    dbase.execute(
                    ''' 
                    INSERT INTO companies(VAT_id,company_name,bank_account,city,zip_code,street_name,box_number)
                    VALUES(?,?,?,?,?,?,?)
                    ''', (VAT_id, company_name, bank_account,city,zip_code,street_name,box_number))

def insert_in_invoice(reference_number, payment_status,subscript_id):
    dbase.execute(
                    ''' 
                    INSERT INTO invoice(reference_number,payment_status,subscript_id)
                    VALUES(?,?,?)
                    ''', (reference_number, payment_status, subscript_id))

def insert_in_quote(quantity, price, currency,sub_id):
    dbase.execute(
                    ''' 
                    INSERT INTO quote(quantity,price,currency,sub_id)
                    VALUES(?,?,?,?)
                    ''', (quantity, price, currency,sub_id))
                
def insert_in_subscription(activation_status, companies_id,custom_id):
    dbase.execute(
                    ''' 
                    INSERT INTO subscription(activation_status,companies_id,custom_id)
                    VALUES(?,?,?)
                    ''', (activation_status, companies_id,custom_id))

insert_in_customer('Adeline', 'Wouters', 1 )
insert_in_companies(123, 'Saas',2,'BX',1180,'Guillaume',76)
insert_in_invoice(1,1,1)
insert_in_subscription (1,123,1)
insert_in_quote(2,140,'USD',1)

insert_in_customer('Quentin', 'Wouters', 2 )
insert_in_companies(125, 'Saas',2,'BX',1180,'Guillaume',76)
insert_in_invoice(2,1,125)
insert_in_subscription (1,125,2)
insert_in_quote(5,300,'EUR',2)

#exchange rate
url = 'https://v6.exchangerate-api.com/v6/1d87a25927f327d52c8b48ff/latest/USD'

response = requests.get(url)
json_data = response.json()
conv_rate = float(json_data.get('conversion_rates').get('EUR'))
print(json_data.get('conversion_rates').get('EUR'))

def read_data_quote(quote_id):
    price_list = dbase.execute(''' SELECT * FROM quote ''').fetchall()
    currency = price_list[quote_id-1][4]
    if (currency != str('EUR')):
    #first element is ID -1, second is the price (third position)
        price_adj = price_list[(quote_id)-1][3]
        price_adj = price_adj*conv_rate
    else: 
        price_adj = price_list[(quote_id)-1][3]

    return price_adj

#prix déjà en EUR donc ne change pas
records = read_data_quote(2)
print(records)
#prix en USD de base donc change
records = read_data_quote(1)
print(records)

dbase.close()
print('Database Closed')

