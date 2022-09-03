from get_data import *
import pymysql.cursors  # python과 mysql(mariadb) 연동
import security.db_auth as db_auth
## 일주일에 한 번 씩 실행될 것임. ##

# get_menu_data에서 스크래핑한 값들을 가져옴
day = days
day_morning = day_mornings
day_lunch = day_lunches
day_dinner = day_dinners
 
# Connect to the DB
login = db_auth.db_login
connection = pymysql.connect(host=login['host'],
                             user=login['user'],
                             password=login['password'],
                             db=login['db'],
                             charset=login['charset'],
                             cursorclass=pymysql.cursors.DictCursor)
# cursorclass=pymysql.cursors.DictCursor 딕셔너리 형태로 리턴. 없으면 그냥 배열로 리턴

try:
    cursor = connection.cursor()
    # 지속적으로 변동될 WEEK, MORNING, LUNCH, DINNER 테이블 삭제 후 다시 생성.

    def init_db_setting():  # 해당 테이블이 없으면 만들어라! menudata, review, user
        if not (cursor.execute("SHOW TABLES LIKE %s", 'menudata')):
            cursor.execute(
                "CREATE TABLE menudata(id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,menu VARCHAR(50) UNIQUE,score INT(10),reviewcount INT(10))")
        if not (cursor.execute("SHOW TABLES LIKE %s", 'review')):
            cursor.execute(
                "CREATE TABLE review(user_id VARCHAR(50) NOT NULL,menu VARCHAR(50) NOT NULL, score INT(10) NOT NULL)")
        if not(cursor.execute("SHOW TABLES LIKE %s", 'users')):
            cursor.execute(
                "CREATE TABLE users(id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, user_id VARCHAR(50) NOT NULL, user_pw TEXT NOT NULL)")

    def week_update():
        print(day)
        for i in range(0, len(day), 2):
            arr = (day[i], day[i+1])
            print(arr)
            cursor.execute("INSERT INTO week (day, date) VALUES(%s, %s)", arr)

    def db_update():  # 이미 있는 테이블이면 지우고 다시 만들어라!
        if cursor.execute("SHOW TABLES LIKE %s", 'week') or cursor.execute("SHOW TABLES LIKE %s", 'morning') or cursor.execute("SHOW TABLES LIKE %s", 'lunch') or cursor.execute("SHOW TABLES LIKE %s", 'dinner'):
            cursor.execute("DROP TABLE week")
            cursor.execute("DROP TABLE morning")
            cursor.execute("DROP TABLE lunch")
            cursor.execute("DROP TABLE dinner")

        cursor.execute(
            "CREATE TABLE week(day VARCHAR(2) NOT NULL primary key,date VARCHAR(11) NOT NULL)")
        cursor.execute(
            "CREATE TABLE morning(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(50) NOT NULL)")
        cursor.execute(
            "CREATE TABLE lunch(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(50) NOT NULL)")
        cursor.execute(
            "CREATE TABLE dinner(day VARCHAR(2) NOT NULL,course VARCHAR(50),menu VARCHAR(50) NOT NULL)")

    def update_menudata():  # 중복이면 입력안함(무시).
        cursor.execute(
            "INSERT IGNORE INTO menudata (menu) SELECT menu FROM morning")
        cursor.execute(
            "INSERT IGNORE INTO menudata (menu) SELECT menu FROM lunch")
        cursor.execute(
            "INSERT IGNORE INTO menudata (menu) SELECT menu FROM dinner")
        # id값 1부터 다시 세기.
        cursor.execute("ALTER TABLE menudata AUTO_INCREMENT=1")
        cursor.execute("SET @COUNT = 0")
        cursor.execute("UPDATE menudata SET id = @COUNT:=@COUNT+1")

    # 아침, 점심, 저녁을 DB의 각 테이블에 저장할 함수
    # 각 배열을 넘겨주고 opt로 테이블 선택 opt=0:MORNING, opt=1:LUNCH, opt=2:DINNER
    def update_db_menu(arg, opt):
        for i in range(len(arg)):   # 2차원 배열이므로 첫번째는 요일
            tag = ''    # 코스 기록
            if i == 0:    # 0:일, 1:월, 2:화, 3:수, 4:목, 5:금, 6:토
                day = '월'
            elif i == 1:
                day = '화'
            elif i == 2:
                day = '수'
            elif i == 3:
                day = '목'
            elif i == 4:
                day = '금'
            elif i == 5:
                day = '토'
            elif i == 6:
                day = '일'

            courseList = ['A', 'B', 'C', '테이크아웃', 'T/O', '한식', '일품', 'A코스', 'B코스', 'C코스', '베이커리', '죽',
                          'A코스/한식', 'B코스/베이커리', 'C코스/죽', '◆공지◆', 'B코스/일품', '공지']   # 새로운 코스 등장하면 여기에 추가!
            for j in range(len(arg[i])):  # 두번째는 요일별 전체 메뉴
                if(arg[i][j] in courseList):
                    tag = arg[i][j]  # A,B,C,테이크아웃 코스인 경우 tag에 저장하고 건너뛰기
                    continue
                elif not arg[i][0] in courseList:
                    tag = 'none'    # 코스가 아닌경우 tag에 none

                arr = (day, tag, arg[i][j])
                if(opt == 0):  # MORNING 테이블에 저장
                    cursor.execute(
                        "INSERT INTO morning (day, course, menu) VALUES(%s, %s, %s)", arr)
                elif(opt == 1):  # LUNCH 테이블에 저장
                    cursor.execute(
                        "INSERT INTO lunch (day, course, menu) VALUES(%s, %s, %s)", arr)
                elif(opt == 2):   # DINNER 테이블에 저장
                    cursor.execute(
                        "INSERT INTO dinner (day, course, menu) VALUES(%s, %s, %s)", arr)

    # 실행부분
    init_db_setting()  # 초기에 한 번만 실행함. review, user, menudata 테이블을 생성.
    db_update()   # week, morning, lunch, dinner 테이블에 스크래핑 결과를 저장.
    week_update()  # WEEK 테이블에 데이터 업데이트.

    # 각 테이블에 데이터 업데이트. opt:0 = morning table, opt:1 = lunch table, opt:2 = dinner table
    update_db_menu(day_morning, 0)
    update_db_menu(day_lunch, 1)
    update_db_menu(day_dinner, 2)

    update_menudata()  # menudata 테이블 업데이트

    menu = cursor.execute("select * from menudata")
    menu = cursor.fetchall()
    str = []
    for i in range(len(menu)):
        temp = menu[i]['menu']
        str.append(temp)

finally:
    connection.commit()  # 실행한 문장들 적용
    connection.close()
