from flask import Flask
app = Flask(__name__)

@app.route('/aggregate')
def get_aggregate():
   return 'Hello'

if __name__ == '__main__':
   app.run(debug = True)
