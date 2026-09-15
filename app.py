from flask import Flask, render_template, request, redirect, url_for
from  connection import conn

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('layout/base.html')
# Ctegory route
@app.route('/category')
def index_category():
    return render_template('category/index.html')

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


@app.route('/product')
def index_product():
    return render_template('products/index.html')


if __name__=="__main__":
    app.run(debug=True)