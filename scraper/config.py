# 메뉴 파싱 설정
MENU_BLOCKING_PATTERNS = [
    '[공지]',
    '어플연동시',
    '당일 메뉴 오류',
    '학생생활관 홈페이지',
]

# 메뉴 길이 제한
MAX_MENU_LENGTH = 50
MAX_COURSE_LENGTH = 20

# 식사 타입
MEAL_TYPES = ['아침', '점심', '저녁']

# 식사 타입 매핑
MEAL_TYPE_MAPPING = {
    '아침': 'BREAKFAST',
    '점심': 'LUNCH',
    '저녁': 'DINNER'
} 