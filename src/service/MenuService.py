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
                menuList = []   # morning에 넣을 배열
                courseDict = dict() # morning에 넣을 배열에 넣을 딕셔너리
                courseList = [] # morning에 넣을 배열에 넣을 딕셔너리에 코스별로 음식명을 넣기위한 임시 리스트

                if num == 0:
                    for k in j:
                        if k['course'] in courseList: # 기존에 있던 코스의 메뉴라면
                            courseDict['menu'].append(k['menu']) # 메뉴 추가
                        else:   # 새로운 코스의 메뉴가 등장하면 
                            if len(courseDict) > 0: # courseDict에 내용물이 있을 떄, 
                                menuList.append(courseDict) # 기존의 courseDict는 menuList에 추가
                                courseDict = dict()
                            if k['course'] == 'none':
                                courseDict['course'] = ''
                            else:
                                courseDict['course'] = k['course'] # 코스 생성
                            courseDict['menu'] = [k['menu']] # 메뉴 생성
                            courseList.append(k['course'])
                    menuList.append(courseDict) # 마지막으로 생성한 courseDict도 menuList에 추가
                    tmpDict["morning"] = menuList
                if num == 1:
                    for k in j:
                        if k['course'] in courseList: # 기존에 있던 코스의 메뉴라면
                            courseDict['menu'].append(k['menu']) # 메뉴 추가
                        else:   # 새로운 코스의 메뉴가 등장하면 
                            if len(courseDict) > 0: # courseDict에 내용물이 있을 떄, 
                                menuList.append(courseDict) # 기존의 courseDict는 menuList에 추가
                                courseDict = dict()
                            if k['course'] == 'none':
                                courseDict['course'] = ''
                            else:
                                courseDict['course'] = k['course'] # 코스 생성
                            courseDict['menu'] = [k['menu']] # 메뉴 생성
                            courseList.append(k['course'])
                    menuList.append(courseDict) # 마지막으로 생성한 courseDict도 menuList에 추가
                    tmpDict["lunch"] = menuList
                if num == 2:
                    for k in j:
                        if k['course'] in courseList: # 기존에 있던 코스의 메뉴라면
                            courseDict['menu'].append(k['menu']) # 메뉴 추가
                        else:   # 새로운 코스의 메뉴가 등장하면 
                            if len(courseDict) > 0: # courseDict에 내용물이 있을 떄, 
                                menuList.append(courseDict) # 기존의 courseDicts는 menuList에 추가
                                courseDict = dict()
                            if k['course'] == 'none':
                                courseDict['course'] = ''
                            else:
                                courseDict['course'] = k['course'] # 코스 생성
                            courseDict['menu'] = [k['menu']] # 메뉴 생성
                            courseList.append(k['course'])
                    menuList.append(courseDict) # 마지막으로 생성한 courseDict도 menuList에 추가
                    tmpDict["dinner"] = menuList
            dictData[self.day[cnt - 1]] = tmpDict # 하나로 합친 tmpDict 를 'today', 'tomorrow', 'theDayAfterTomorrow' 안에 value로 넣음
        return json.dumps(dictData, ensure_ascii=False)