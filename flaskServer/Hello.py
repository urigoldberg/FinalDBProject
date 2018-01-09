from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello World"

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))


@app.route('/')
def index():
   return '<html><body><h1>Hello World'</h1></body></html>'

@app.route('/')
def index():
   return render_template('hello.html')

if __name__ == '__main__':
   app.run(host='localhost', port=40123, threaded=True)
