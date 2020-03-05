from flask import Flask, redirect, url_for, request
import deep
import json
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   jso=deep.detect(name)
   with open("data.json", "w") as write_file:
   	write_file.write(jso)
   #return deep.detect(name)
   return jso+'\n'+'\njson file created in the folder from where code is being executed'

@app.route('/',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)
