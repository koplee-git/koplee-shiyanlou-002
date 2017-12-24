from flask import render_template,Flask
from flask.ext.sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTH_RELOAD']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
db=SQLAlchemy(app)
class File(db.Model):
    __tablename__='file'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time=db.Column(db.DateTime)
    category = db.Column(db.String)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category=db.relationship('Category',backref=db.backref('files'))
    content=db.Column(db.Text)
    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content
    def __repr__(self):
        return "<File%r>"%self.id
class Category(db.Model):
    __tablename__='category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return "<Caegory%r>"%self.name
@app.route('/')
def index():
    newfilelst=[]
    for  _,_,filelst in os.walk('/home/shiyanlou/files'):
        for file in filelst:
                with open('/home/shiyanlou/files/'+ file,'r') as f:
                    dic_file=json.loads(f.read())
                    newfilelst.append(dic_file['title'])
    return render_template('index.html',newfilelst=newfilelst)

@app.route('/files/<filename>')
def file(fileid):
    filename='/home/shiyanlou/files/'+ str(filename) + '.json'
    print(filename)
    if os.path.exists(filename) :
        print("ok")
        with open(filename,'r') as f:
            dic_file=json.loads(f.read())
        return render_template('file.html',dic_file=dic_file)
    else:
        return render_template('404.html')
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404
