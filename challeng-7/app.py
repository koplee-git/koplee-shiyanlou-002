from flask import render_template,Flask
from flask.ext.sqlalchemy import SQLAlchemy
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
    newfilelst=File.query.all()
    return render_template('index.html',newfilelst=newfilelst)

@app.route('/files/<fileid>')
def file(fileid):
    fileobject = File.query.get_or_404(fileid)
    return render_template('file.html',fileobject=fileobject)
    
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404
