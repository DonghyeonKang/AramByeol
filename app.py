from flask import Flask # Flask start 
from flask import render_template # Rendering

app = Flask(__name__)
app.secret_key = 'asd1inldap123jwaw'        # 세션을 암호화하기 위해 비밀키가 서명된 쿠키 사용

if not app.debug: # 디버그 모드가 아니면
    import logging  # 로깅을 하기위한 모듈
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler( # 2000바이트가 넘어가면 로테이팅 백업 진행. 최대 파일 10개
        '../log/arambyeol_error.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.WARNING) # WARNING 수준의 레벨들을 로깅
    app.logger.addHandler(file_handler)

# 웹 페이지 에러났을 때 에러 페이지 보여주기 401, 403, 404, 500
@app.errorhandler(500)
def internal_error(error):
    return render_template('/error/error.html'), 500
@app.errorhandler(404)
def page_not_found(error):
    return render_template('/error/error.html'), 404
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('/error/error.html'), 403
@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('/error/error.html'), 401

# page route
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=False, threaded=True)