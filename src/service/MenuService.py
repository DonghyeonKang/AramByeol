import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from repository.MenuRepository import *
import repository.MenuRepository as MenuRepository
import json
from flask import jsonify # Return json form to client
from datetime import datetime, timedelta # Time generator
## 일주일에 한 번 씩 실행될 것임. ##

class MenuService:
    week = ['월', '화', '수', '목', '금', '토', '일']
    day = ['today', 'tomorrow', 'theDayAfterTomorrow']
    
    # db 연결
    menuRepository = MenuRepository.MenuRepository()

    # morning, lunch, dinner table 을 초기화 한다. 
    def clearData(self):
        self.menuRepository.db_update()

    # week 테이블에 day, date 값 넣기
    def weekData(self, day_date):
        for day, date in day_date.items():
            self.menuRepository.db_week(day, date)

    # morning 테이블에 day,cource,menu 값 넣기
    def morningData(self, day_morning):
        for day, course_data in day_morning.items():
            morning_course = course_data
            for course, menu in morning_course.items():
                self.menuRepository.db_morning(day, course, menu)


    # lunch 테이블에 day,cource,menu 값 넣기  
    def lunchData(self, day_lunch):
        for day, course_data in day_lunch.items():
            lunch_course = course_data
            for course, menu in lunch_course.items():
                self.menuRepository.db_lunch(day, course, menu)

     # dinner 테이블에 day,cource,menu 값 넣기
    def dinnerData(self, day_dinner):
        for day, course_data in day_dinner.items():
            dinner_course = course_data
            for course, menu in dinner_course.items():
                self.menuRepository.db_dinner(day, course, menu)

    def setMenuData(self, menuData):
        try:
            self.menuRepository.insertMenuData(menuData)
        except: # duplicated key error 시 pass
            pass
        return

    def getMenuApp(self):
        dictData = {}
        cnt = 0

        for i in self.week[datetime.today().weekday():]: # 오늘부터 3일까지만 출력할 거임
            dayMenuData = self.menuRepository.selectMenuByDay(i)
            tmpDict = {}
            
            # 최대 3일까지
            if cnt >= 3:
                break
            else:
                cnt += 1

            # 메뉴 json 형식으로 파싱
            for num, j in enumerate(dayMenuData): # day, 아침 점심 저녁을 하나로 합침
                menuList = []   # morning에 넣을 배열
                courseDict = dict() # morning에 넣을 배열에 넣을 딕셔너리

                if num == 0:
                    for k in j:
                        courseDict['course'] = k['course'] # 코스 생성
                        courseDict['menu'] = [k['menu'].split(", ")] # 메뉴 생성
                    menuList.append(courseDict) 
                    tmpDict["morning"] = menuList
                if num == 1:
                    for k in j:
                        courseDict['course'] = k['course'] # 코스 생성
                        courseDict['menu'] = [k['menu'].split(", ")] # 메뉴 생성
                    menuList.append(courseDict) 
                    tmpDict["lunch"] = menuList
                if num == 2:
                    for k in j:
                        courseDict['course'] = k['course'] # 코스 생성
                        courseDict['menu'] = [k['menu'].split(", ")] # 메뉴 생성
                    menuList.append(courseDict) 
                    tmpDict["dinner"] = menuList
            dictData[self.day[cnt - 1]] = tmpDict # 하나로 합친 tmpDict 를 'today', 'tomorrow', 'theDayAfterTomorrow' 안에 value로 넣음
        return json.dumps(dictData, ensure_ascii=False)

    def getMenuWeb(self):
        # 이번 주의 요일, 날짜 데이터
        rows = self.menuRepository.selectWeekData()

        days = []
        # 한 주의 날짜를 리스트 딕셔너리 형식으로 DB에서 추출
        for i in range(len(rows)):
            temp = []
            day = rows[i]['day'] # db에서 불러올 때 [배열][딕셔너리] 형식으로 들고옴.
            date = rows[i]['date']
            temp.append(day)
            temp.append(date)
            days.append(temp)
        # 오늘, 내일, 모레 날짜를 계산
        day = []
        now = datetime.today().strftime("%Y-%m-%d")
        tomorrow = (datetime.today() + timedelta(1)).strftime("%Y-%m-%d")
        after = (datetime.today() + timedelta(2)).strftime("%Y-%m-%d")
        # 오늘, 내일, 모레에 해당하는 날짜만 추출
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

        # 아침 메뉴 데이터 가져오기
        rows = self.menuRepository.selectMorning()
        # 오늘, 내일, 모레에 해당하는 메뉴들만 추출
        morning = [] # 아침 정보를 제공해줄거얌
        for i in range(len(rows)):
            for j in range(len(day)):
                if day[j] == rows[i]['day']:
                    for k in rows[i]['menu'].split(", "):
                        temp = []
                        temp.append(rows[i]['day'])
                        temp.append(rows[i]['course'])
                        temp.append(k)                
                        test = self.menuRepository.getMenuScore(k)
                        temp.append(test[0]['score'])
                        morning.append(temp)


        rows = self.menuRepository.selectLunch()
        
        lunch = []  # 점심 정보를 제공해 줄거얌
        for i in range(len(rows)):
            for j in range(len(day)):
                if day[j] == rows[i]['day'] :
                    for k in rows[i]['menu'].split(", "):
                        temp = []
                        temp.append(rows[i]['day'])
                        temp.append(rows[i]['course'])
                        temp.append(k)                
                        test = self.menuRepository.getMenuScore(k)
                        temp.append(test[0]['score'])
                        lunch.append(temp)

        rows = self.menuRepository.selectDinner()

        dinner = [] # 저녁 정보를 제공해 줄거얌
        for i in range(len(rows)):
            for j in range(len(day)):
                if day[j] == rows[i]['day'] :
                    for k in rows[i]['menu'].split(", "):
                        temp = []
                        temp.append(rows[i]['day'])
                        temp.append(rows[i]['course'])
                        temp.append(k)                
                        test = self.menuRepository.getMenuScore(k)
                        temp.append(test[0]['score'])
                        dinner.append(temp)

        return json.dumps({'days':days, 'morning':morning, 'lunch':lunch, 'dinner':dinner}, ensure_ascii=False)

    def setMenuScore(self, menu, score):
        data = self.menuRepository.selectMenuData(menu)

        # 가져온 메뉴를 DB의 메뉴와 비교하여 누적 점수를 가져옴
        reviewCount = 0
        db_score = 0
        avg = 0

        # 점수가 하나도 없었다면 None이므로 0이라고 해줌.
        if data['reviewcount'] == None:
            reviewCount = 0
        else:
            reviewCount = data['reviewcount']
        if data['score'] == None:
            db_score = 0
        else: 
            db_score = data['score']

        # 계산 방식 : 1. DB -> (누적점수 / 별점준 사용자 수) = 총점
        # 2. DB <- ((총점 + 부여 점수) / 별점준 사용자 수 + 1)
        db_score = (db_score * reviewCount) + int(score)
        reviewCount = reviewCount + 1
        avg = int(round(db_score / reviewCount))

        try:
            self.menuRepository.updateMenuScore(menu, reviewCount, avg)
            return jsonify({'msg': menu + " 메뉴에 " + str(score) + "점 주셨습니다."})
        except:
            return jsonify({'msg': "Fail"})