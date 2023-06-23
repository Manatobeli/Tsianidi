from flask import Flask, request, render_template, flash, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
ADMIN_USR = 'KillerManatobel'
PASSWORD = 'YvelazeDzlieri'


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Coffins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(2500), nullable=False)
    image_name = db.Column(db.String(40), nullable=False)

    def __init__(self,name,price,image_name = "Unnamed"):
        self.name = name
        self.price = price
        self.image_name = image_name

    def __str__(self):
        return self.name


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods = ['POST', 'GET'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.files['image']

        coffin = Coffins(name, price)
        db.session.add(coffin)
        db.session.commit()
        
        filename = secure_filename(image.filename)
        file_extension = os.path.splitext(filename)[1]
        new_filename = str(coffin.id) + file_extension
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        image.save(filepath)
        
        coffin.image_name = new_filename
        db.session.commit()
        
        
    coffins = Coffins.query.all()
                
    return render_template('products.html', coffins = coffins)

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    global ADMIN_USR
    global PASSWORD
    username = request.form.get('username')
    password = request.form.get('password')
    if username == ADMIN_USR and password == PASSWORD:
        flash("The Coffin Has Been Uploaded","info")
        return render_template('admin.html')
    else:
        return redirect('/signin')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/location')
def location():
    return render_template('location.html')


if __name__=="__main__":
    app.run(debug=True)
