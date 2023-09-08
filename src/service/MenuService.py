import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from repository.MenuRepository import *
import repository.MenuRepository as MenuRepository
## 일주일에 한 번 씩 실행될 것임. ##

class MenuService:
    
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