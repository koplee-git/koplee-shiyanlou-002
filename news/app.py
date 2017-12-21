from flask import render_template,Flask
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTH_RELOAD']=True

@app.route('/')
def index():
    filedic={}
    for  _,_,filelst in os.walk('/home/shiyanlou/files'):
        for file in filelst:
            with open('/home/shiyanlou/files/'+ file,'r') as f:
                dic_file=json.loads(f.read())
            filedic.update(dic_file)

    return render_template('/home/shiyanlou/templates/file.html',filedic=filedic)

@app.route('/files/<filename>')
def file(filename):
    if os.path.exit(filename) :
        with open(filename,'r') as f:
            dic_file=json.loads(f.read())
        return render_tempate('file.html',filedic=filedic)
    else:
        return render_template('404.html')
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404
