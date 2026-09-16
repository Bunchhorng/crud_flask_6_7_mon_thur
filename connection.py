import pymysql

def connectDB():
    return pymysql.connect(
        host = "localhost",
        user = "root",
        password='',
        port = 3309,
        database='inventory_flask_6_7_db',
        cursorclass=pymysql.cursors.DictCursor,
    )

conn = connectDB()

if conn:
    print("Connect to database successfully!")
else:
    print("Connect to database failed!")