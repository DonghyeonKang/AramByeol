import pymysql.cursors # python과 mysql(mariadb) 연동
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                        user='opc',
                        password='111111',
                        db='arambyeol',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def home():
    return render_template('index.html')

# API
@app.route('/api/list', methods=['GET'])
def week():
    cursor = connection.cursor()

    sql = "select * from week"
    cursor.execute(sql)

    rows = cursor.fetchall()
    days = []
    for i in range(len(rows)):
        temp = []
        day = rows[i]['day'] # db에서 불러올 때 [배열][딕셔너리] 형식으로 들고옴.
        date = rows[i]['date']
        temp.append(day)
        temp.append(date)
        days.append(temp)

    day = []
    now = datetime.today().strftime("%Y-%m-%d")
    tomorrow = (datetime.today() + timedelta(1)).strftime("%Y-%m-%d")
    after = (datetime.today() + timedelta(2)).strftime("%Y-%m-%d")

    today_temp = ""
    tomorrow_temp = ""
    after_temp = ""
    for i in range(len(rows)):
        if (now == rows[i]['date']):
            today_temp = rows[i]['day']
        if (tomorrow == rows[i]['date']):
            tomorrow_temp = rows[i]['day']
        if (after == rows[i]['date']):
            after_temp = rows[i]['day']
    day.append(today_temp)
    day.append(tomorrow_temp)
    day.append(after_temp)

    sql = "select * from morning"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    morning = [] # 아침 정보를 제공해줄거얌
    for i in range(len(rows)):
        temp=[]
        for j in range(len(day)):
            if day[j] == rows[i]['day'] :
                temp.append(rows[i]['day'])
                temp.append(rows[i]['course'])
                temp.append(rows[i]['menu'])
                morning.append(temp)


    sql = "select * from lunch"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    lunch = []  # 점심 정보를 제공해 줄거얌
    for i in range(len(rows)):
        temp=[]
        for j in range(len(day)):
            if day[j] == rows[i]['day'] :
                temp.append(rows[i]['day'])
                temp.append(rows[i]['course'])
                temp.append(rows[i]['menu'])
                lunch.append(temp)
    

    sql = "select * from dinner"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    dinner = [] # 저녁 정보를 제공해 줄거얌
    for i in range(len(rows)):
        temp=[]
        for j in range(len(day)):
            if day[j] == rows[i]['day'] :
                temp.append(rows[i]['day'])
                temp.append(rows[i]['course'])
                temp.append(rows[i]['menu'])
                dinner.append(temp)
    # connection.commit()
    # connection.close()
    return jsonify({'days':days, 'morning':morning, 'lunch':lunch, 'dinner':dinner}) # js와 매칭



if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True, threaded=True)
    print("Starting app on port %d" % port)


