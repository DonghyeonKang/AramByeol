import src.menu.menu_repository as menu_repository
import json

class MenuService:
    menuRepository = menu_repository.MenuRepository()

    def __init__(self) -> None:
        pass

    def selectMenuList(self):
        week = ['월', '화', '수', '목', '금', '토', '일']
        dictData = {}
        for i in week: # week
            tmpDict = {}
            dayMenuData = self.menuRepository.selectMenuByDay(i)
            for num, j in enumerate(dayMenuData): # day, 아침 점심 저녁을 하나로 합침
                if num == 0:
                    tmpDict["morning"] = j
                elif num == 1:
                    tmpDict["lunch"] = j
                elif num == 2:
                    tmpDict["dinner"] = j
            dictData[i] = tmpDict # 하나로 합친 tmpDict 를 요일 안에 value로 넣음
        return json.dumps(dictData, ensure_ascii=False)

    def selectMenuReview(self, menu_id):
        data = self.menuRepository.selectMenuReview(menu_id)
        return data

    def updateMenuReview(self, reviewData):
        data = []
        for i in reviewData:
            arr = self.menuRepository.updateMenuReview(i['menu_id'], i['score'], i['user_id'])
            data.append(arr[0])
        return json.dumps(data, ensure_ascii=False)
