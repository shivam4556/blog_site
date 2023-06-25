from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_site.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
 

class Contact_request(db.Model):
    # id, name, email, phone_num, message
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(20), nullable = False)
    phone_num = db.Column(db.String(10), nullable = True)
    message = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.id}->{self.name}'

class Post(db.Model):
    # id, name, email, phone_num, message
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable = False)
    content = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(20), nullable = True)
    date = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.id}->{self.title}'
    
# with app.app_context():
#     db.create_all()

@app.route("/")
def get_homepage():
    return render_template('index.html')

@app.route("/about")
def get_about():
    return render_template('about.html')

@app.route("/contact", methods = ['GET', 'POST'])
def get_contact():
    if  request.method == 'GET':
        return render_template('contact.html')
    else:
        contact_entry = Contact_request(name = request.form['name'],
                                        email = request.form['email'],
                                        phone_num = request.form['phone_num'],
                                        message = request.form['message'],
                                        )
        db.session.add(contact_entry)
        db.session.commit()
        return redirect('/contact ')

@app.route("/post")
def get_post():
    return render_template('post.html')

app.run(debug = True)