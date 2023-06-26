from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime 
import json

params = json.load(open("./config.json"))['params']

app = Flask(__name__)


# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
app.config.update(
    MAIL_SERVER='smtp@gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = params['contact_mail'],
    MAIL_PASSWORD = params['gmail_app_spec_pass']
)
 
mail = Mail(app)
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
    description = db.Column(db.String(30), nullable = True)
    content = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(20), nullable = True)
    slug = db.Column(db.String(20), nullable = True)
    date = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.id}->{self.slug}->{self.title}'
    
# with app.app_context():
#     # db.create_all()
#     post = Post(title = "Man must explore, and this is exploration at its greatest",
#                 description = "Problems look mighty small from 150 miles up",
#                 content = "Never in all their history have men been able truly to conceive of the world as one: a single sphere, a globe, having the qualities of a globe, a round earth in which all the directions eventually meet, in which there is no center because every point, or none, is center — an equal earth which all men occupy as equals. The airman's earth, if free men make it, will be truly round: a globe in practice, not in theory. Science cuts two ways, of course; its products can be used for both good and evil. But there's no turning back from science. The early warnings about technological dangers also come from science.",
#                 author = "myman",
#                 slug = "eight-post",
#                 )
#     db.session.add(post)
#     db.session.commit()


@app.route("/")
def get_homepage():
    posts = Post.query.all()[:4]
    
    # print(posts)
    return render_template('index.html', params = params, posts = posts)


@app.route("/about")
def get_about():
    return render_template('about.html',params = params)


# Query a post from DB and render it in post.html
@app.route("/post/<string:post_slug>", methods = ['GET'])
def get_post(post_slug):
    req_post = Post.query.filter_by(slug = post_slug).first()
    print(req_post)
    return render_template('post.html',params = params, post = req_post)







@app.route("/contact", methods = ['GET', 'POST'])
def get_contact():
    if  request.method == 'GET':
        return render_template('contact.html',params = params)
    else:
        contact_entry = Contact_request(name = request.form['name'],
                                        email = request.form['email'],
                                        phone_num = request.form['phone_num'],
                                        message = request.form['message'],
                                        )
        db.session.add(contact_entry)
        db.session.commit()
        msg = Message(subject = "Contact request from " + request.form['name'],
                  sender = request.form['email'],
                  recipients = ["shivambhardwajtemp@gmail.com"],
                  body = request.form['message'] + "\n" + request.form['phone_num']
                  )
        try:
            mail.send(msg)
        except:
            print("Mail not sent")
        return redirect('/contact ')



    

app.run(debug = True)