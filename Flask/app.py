from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import pyshorteners


app = Flask(__name__)

######################SQL ALCHEMY CONFIGURATION#######################

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#pass Application to SQLite class
db=SQLAlchemy(app)
Migrate(app,db)

########################Create a Model##########################

class URL_Shortener(db.Model):
    __tablename__='url'
    id=db.Column(db.Integer,primary_key=True)
    long_url=db.Column(db.String(1000))
    short_url=db.Column(db.String(1000))
    def __init__(self,long_url,short_url):
        self.long_url= long_url
        self.short_url= short_url
##################################################
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/',methods=["GET","POST"])

def home_function():
    long_url=""
    short_url=""
    
    if request.method=='POST':
        long_url=request.form.get('url_link')
        url=pyshorteners.Shortener()
        short_url=url.tinyurl.short(long_url)
        save_value=URL_Shortener(long_url,short_url)
        db.session.add(save_value)
        db.session.commit()    
    return render_template('Home.html',shorter_url=short_url)

@app.route('/History')
def history_function():
    li=URL_Shortener.query.all()
    return render_template('History.html',li=li)

############################################

if __name__ == '__main__':
    app.run(debug=True)