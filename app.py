from pymongo import MongoClient
from flask import render_template,Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['TEMPLATES_AUTH_RELOAD']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
db=SQLAlchemy(app)
mongo=MongoClient('127.0.0.1',27017).shiyanlou
class File(db.Model):
    __tablename__='file'
    tag_namelst=[]
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
    def add_tag(self,tag_name):
        if tag_name not in self.tag_namelst:
            self.tag_namelst.append(tag_name)
            files={'name':self.title,'tag':self.tag_namelst}
            mongo.files.insert_one(files)
        print([item for item in mongo.files.find()])
    def remove_tag(self,tag_name):
        if tag_name in self.tag_namelst:
            dicfile=mongo.files.find_one({'name':self.title})
            self.tag_namelst=dicfile['tag'].remove(tag_name)
            mongo.files.update_one({'name'.self.title},{'$set':{'tag':self.tag_namelst}})
    @property
    def tags(self):
        return [item['tag']for item in mongo.files.find()]
class Category(db.Model):
    __tablename__='category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return "<Caegory%r>"%self.name
def insert_datas():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')
@app.route('/')
def index():
    newfilelst=File.query.all()
    return render_template('index.html',newfilelst=newfilelst)

@app.route('/files/<fileid>')
def file(fileid):
    fileobject = File.query.get_or_404(fileid)
    return render_template('file.html',fileobject=fileobject)
    
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404
if __name__=='__main__':
    insert_datas()
    app.run()
