# 식사 타입이 들어간('아침', '점심', '저녁') 첫번째 인덱스를 제거
def first_index_del(arg, repeat=1):
        for i in range(repeat):
            del arg[0]

# 각각의 인덱스 속 쌍따옴표를 찾아서 모두 삭제.
def double_quorts_del(arg): 
        search = '"'
        for i, word in enumerate(arg):
            arg[i] = word.strip() # 공백도 덤으로 삭제!
            if search in word:
               arg[i] = word.strip(search).strip() # 쌍따옴표 제거하고 공백 제거
        return arg

# 메뉴 데이터를 가공할거임. 2차 가공. 요일 별로 나눔.
def split_menu_data(args):
        count = 0
        day=[]
        day.append([])
        day_count = 0   # 요일 카운트 [요일][메뉴]

        for element in args:
            if count >= 4:  # 공백 개수가 연속으로 4 이상이면
                day.append([])  # 요일 바뀜
                day_count += 1  # 요일 바꾸기
                count = 0   # 공백 개수 초기화
        
            if element == '': # 공백 인덱스면
                count += 1  # 공백 개수를 세고
            else:
                day[day_count].append(element)
                count = 0   # 공백 개수 초기화
        return day

# 필요없는 데이터를 지움
def data_blocking(args):
    data = []
    blockingList = ["공지", "어플연동시", "당일 메뉴 오류가 빈번하게 발생합니다. 학생생활관 홈페이지에서 메뉴를 확인해주세요"]
    for i in args:
        if i not in blockingList:
            data.append(i)
    return data

def mergeMeals(mornings, lunches, dinners, courseList):
    tmp = []
    for i in mornings:
        for j in i:
            if j in courseList:
                i.remove(j)
        tmp = tmp + i

    for i in lunches:
        for j in i:
            if j in courseList:
                i.remove(j)
        tmp = tmp + i

    for i in dinners:
        for j in i:
            if j in courseList:
                i.remove(j)
        tmp = tmp + i
    return tmp