import src.repository.MenuRepository as MenuRepository
import json
from flask import jsonify
from datetime import datetime

class MenuService:
    menuRepository = MenuRepository.MenuRepository()
    courseList = ['A', 'B', 'C', '테이크아웃', 'T/O', '한식', '일품', 'A코스', 'B코스', 'C코스', '베이커리', '죽', '죽식', 'none'
                          'A코스/한식', 'B코스/베이커리', 'C코스/죽', '◆공지◆', 'B코스/일품', '공지']
    week = ['월', '화', '수', '목', '금', '토', '일']
    day = ['today', 'tomorrow', 'theDayAfterTomorrow']

    def selectMenuList(self):
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
                courseDict = {}

                if num == 0:
                    for k in j:
                        if k['course'] in courseDict:  # 코스가 추가되었으면
                            courseDict[k['course']].append(k['menu'])
                        else:   # 코스가 추가되어있지 않다면
                            courseDict[k['course']] = [k['menu']]
                    tmpDict["morning"] = courseDict
                elif num == 1:
                    for k in j:
                        if k['course'] in courseDict:  # 코스가 추가되었으면
                            courseDict[k['course']].append(k['menu'])
                        else:   # 코스가 추가되어있지 않다면
                            courseDict[k['course']] = [k['menu']]
                    tmpDict["lunch"] = courseDict
                elif num == 2:
                    for k in j:
                        if k['course'] in courseDict:  # 코스가 추가되었으면
                            courseDict[k['course']].append(k['menu'])
                        else:   # 코스가 추가되어있지 않다면
                            courseDict[k['course']] = [k['menu']]
                    tmpDict["dinner"] = courseDict
            dictData[self.day[cnt - 1]] = tmpDict # 하나로 합친 tmpDict 를 'today', 'tomorrow', 'theDayAfterTomorrow' 안에 value로 넣음

        return json.dumps(dictData, ensure_ascii=False)