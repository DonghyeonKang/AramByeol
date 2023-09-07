from get_data import *
from repository.MenuRepository import *
## 일주일에 한 번 씩 실행될 것임. ##

class MenuService:
    
    # db 연결
    global connection 
    global cursor
    connection = MenuRepository.db_connection()
    cursor = connection.cursor()

    # get_data 에서 스크래핑한 값들 대입
    day_date = day_date
    day_morning = morning
    day_lunch = lunch
    day_dinner = dinner


    # week 테이블에 day, date 값 넣기
    def weekData():
        MenuRepository.db_update()
        for day, date in day_date.items():
            cursor.execute(MenuRepository.db_week(), (day, date))

        connection.commit()
        connection.close()


    # morning 테이블에 day,cource,menu 값 넣기
    def morningData():
        MenuRepository.db_update()
        for day, course_data in day_morning.items():
            morning_course = course_data
            for course, menu in morning_course.items():
                cursor.execute(MenuRepository.db_morning(),(day, course, menu))

        connection.commit()
        connection.close()


    # lunch 테이블에 day,cource,menu 값 넣기  
    def lunchData():
        MenuRepository.db_update()
        for day, course_data in day_lunch.items():
            lunch_course = course_data
            for course, menu in lunch_course.items():
                cursor.execute(MenuRepository.db_lunch(),(day, course, menu))
        
        connection.commit()
        connection.close()


     # dinner 테이블에 day,cource,menu 값 넣기
    def dinnerData():
        MenuRepository.db_update()
        for day, course_data in day_dinner.items():
            dinner_course = course_data
            for course, menu in dinner_course.items():
                cursor.execute(MenuRepository.db_dinner(),(day, course, menu))

        connection.commit()
        connection.close()
        