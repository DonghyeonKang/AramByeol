from get_data import *
from putData_Repository import *
## 일주일에 한 번 씩 실행될 것임. ##

# get_data 에서 스크래핑한 값들 대입
day_date = day_date
day_morning = morning
day_lunch = lunch
day_dinner = dinner
        

# week 테이블에 day, date 값 넣기
db_update()
for day, date in day_date.items():
    cursor.execute(week_sql, (day, date))


# morning 테이블에 day,cource,menu 값 넣기
for day, course_data in day_morning.items():
    morning_course = course_data
    for course, menu in morning_course.items():
        cursor.execute(morning_sql,(day, course, menu))


# lunch 테이블에 day,cource,menu 값 넣기
for day, course_data in day_lunch.items():
    lunch_course = course_data
    for course, menu in lunch_course.items():
        cursor.execute(lunch_sql,(day, course, menu))


# dinner 테이블에 day,cource,menu 값 넣기
for day, course_data in day_dinner.items():
    dinner_course = course_data
    for course, menu in dinner_course.items():
        cursor.execute(dinner_sql,(day, course, menu))


connection.commit()
connection.close()