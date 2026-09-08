import pymysql

def connectDB():
    return pymysql.connect(
        host = "localhost",
        user = "root",
        password='',
        port = 3309,
        database='crud_product'
    )

conn = connectDB()

if conn:
    print("Connect to database successfully!")
else:
    print("Connect to database failed!")