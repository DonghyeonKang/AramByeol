from flask import Flask # flask start 
from flask import request # html request 
from flask import render_template # rendering
from flask import session # session
from flask import redirect # move page

app = Flask(__name__)

# page routing => 없어도 된다.
@app.route('/')
def view_home():
    return redirect('./templates/index.html')

@app.route('/member/review')  
def view_review():  
    return redirect('./templates/review/review.html')

# register request
@app.route('/member/register', methods=['GET', 'POST'])
def register():
    return redirect('./templates/member/login.html')

# login request
@app.route('/member/login', methods=['GET','POST'])
def login():
    return redirect('./templates/index.html')

# review request
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)