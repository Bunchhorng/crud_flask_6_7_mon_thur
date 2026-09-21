from flask import Flask, render_template, request, redirect, url_for
from  connection import conn
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/products'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def dashboard():
    return render_template('layout/base.html')
# Ctegory route
@app.route('/category')
def index_category():
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    return render_template('category/index.html', categories=categories)

@app.route('/category/create', methods=['GET', 'POST'])
def create_category():
    if request.method == "POST":
        name = request.form['name']
        status = request.form['status']

        db = conn
        cursor = db.cursor()
        cursor.execute("INSERT INTO categories(name,status)" \
        "VALUES(%s, %s)", (name, status))
        db.commit()
        cursor.close()
        return redirect(url_for('index_category'))
    return render_template('category/create.html')


@app.route('/category/update/<int:id>', methods=['GET', 'POST'])
def update_category(id):
    cursor = conn.cursor()

    if request.method=="POST":
        newName = request.form['name']
        newStatus = request.form['status']

        sql = "UPDATE categories SET name=%s, status=%s WHERE id=%s"
        cursor.execute(sql,(newName, newStatus, id))
        conn.commit()
        cursor.close()
        return redirect(url_for('index_category'))

    cursor.execute("SELECT * FROM categories WHERE id=%s", (id,))
    category = cursor.fetchone()
    if not category:
        return "404 Not Found"
    
    return render_template('category/update.html', category=category)


@app.route('/category/delete/<int:id>', methods=['GET', 'POST'])
def delete_category(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('index_category'))


@app.route('/product')
def index_product():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return render_template('products/index.html', products=products)

@app.route('/product/create', methods=['GET', 'POST'])
def create_product():
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        
        image_file = request.files.get('image')
        image_name = None

        if image_file and image_file.filename != '':
            image_name = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        
            image_file.save(image_path)
        cursor = conn.cursor()
        sql = """
            INSERT INTO products(name, price, stock, image)
            VALUES(%s, %s, %s, %s)
        """
        cursor.execute(sql, (name, price, stock, image_name))
        conn.commit()
        cursor.close()
        
        return redirect(url_for('index_product'))
        
    return render_template('products/create.html')

if __name__=="__main__":
    app.run(debug=True)