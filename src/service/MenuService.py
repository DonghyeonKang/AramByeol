import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from repository.MenuRepository import *
import repository.MenuRepository as MenuRepository
import json
from flask import jsonify
from datetime import datetime
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
        return 1