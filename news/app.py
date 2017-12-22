from flask import render_template,Flask
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTH_RELOAD']=True

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
def file(filename):
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
