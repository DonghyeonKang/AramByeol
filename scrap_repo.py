import pymysql.cursors
import src.security.db_auth as db_auth

class ScrappingRepository:
    def __init__(self, courses) -> None:
        self.login = db_auth.db_login
        self.courseList = courses

    def getConnection(self):
        self.connection = pymysql.connect(host=self.login['host'],
                                     user=self.login['user'],
                                     password=self.login['password'],
                                     db=self.login['db'],
                                     charset=self.login['charset'],
                                     cursorclass=pymysql.cursors.DictCursor)

    def closeConnection(self):
        self.connection.close()

    def initaializeDB(self):
        self.getConnection()
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("TRUNCATE week")
            self.cursor.execute("TRUNCATE morning")
            self.cursor.execute("TRUNCATE lunch")
            self.cursor.execute("TRUNCATE dinner")
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "Error: Database Initialize Error"
        finally:
            self.closeConnection()

    def week_update(self, days):
        self.getConnection()
        try:
            for i in range(0, len(days), 2):
                arr = (days[i], days[i+1])
            self.cursor = self.connection.cursor()
            self.cursor.execute("INSERT INTO week (day, date) VALUES(%s, %s)", arr)
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "Error: Database Initialize Error"
        finally:
            self.closeConnection()

    # menu data table에 menu 추가
    def update_menudata(self, data):
        self.getConnection()
        try:
            self.cursor = self.connection.cursor()
            # sql 만들기
            sql = "INSERT IGNORE INTO menudata(menu) VALUES ('%s') " % data[0]
            del data[0]
            tmp = ""
            for i in data:
                tmp += ", ('" + str(i) + "')"
            sql += tmp
            self.cursor.execute(sql)
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "Error: Database Insert Error"
        finally:
            self.closeConnection()

    # 1주일치 메뉴 업데이트
    def update_week_menu(self, data, opt):
        self.getConnection()
        try:
            self.cursor = self.connection.cursor()
            # day 만들기
            for i in range(len(data)):   # 2차원 배열이므로 첫번째는 요일
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

                for j in range(len(data[i])):  # 두번째는 요일별 전체 메뉴
                    if(data[i][j] in self.courseList):
                        tag = data[i][j]  # A,B,C,테이크아웃 코스인 경우 tag에 저장하고 건너뛰기
                        continue
                    elif not data[i][0] in self.courseList:
                        tag = 'none'    # 코스가 아닌경우 tag에 none
                    arr = (day, tag, data[i][j])
                    if(opt == 0):  # MORNING 테이블에 저장
                        self.cursor.execute(
                            "INSERT INTO morning (day, course, menu_id) VALUES(%s, %s, (SELECT menu_id FROM menudata WHERE menu=%s))", arr)
                    elif(opt == 1):  # LUNCH 테이블에 저장
                        self.cursor.execute(
                            "INSERT INTO lunch (day, course, menu_id) VALUES(%s, %s, (SELECT menu_id FROM menudata WHERE menu=%s))", arr)
                    elif(opt == 2):   # DINNER 테이블에 저장
                        self.cursor.execute(
                            "INSERT INTO dinner (day, course, menu_id) VALUES(%s, %s, (SELECT menu_id FROM menudata WHERE menu=%s))", arr)
            self.connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "Error: Database Insert Error"
        finally:
            self.closeConnection()

    # 임시 저장된 스크래핑 데이터 가져오기
    def getTmpData(self):
        self.getConnection()
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT * FROM tmpScrap")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result[0]
        except Exception as e:
            print(e)
            return "Error: Database Select Error"
        finally:
            self.closeConnection()