# [AramByeol release version 1.1.3](http://arambyeol.kro.kr/)
아람별은 🏫경상대학교 컴퓨터 과학과 학생들이 만든 기숙사 식단 제공 웹페이지입니다! 
기숙사 식당인 아람관이 더 이상 생활관 어플리케이션에서 식단을 제공되지 않아 불편한 점을 해소하고자 직접 페이지를 만들어 정보를 제공하고자 만들었습니다.
감자별과 아람관을 더해 아람별이 탄생했습니다!!
페이지 주소는 http://arambyeol.kro.kr/ 

Developer: [DonghyeonKang](https://github.com/DonghyeonKang), [SanghyeonKim](https://github.com/limetimeline), [JEONJEYUN](https://github.com/JEONJEYUN), [CooAnt](https://github.com/CooAnt)

Recent Update: 2021-12-18
# UpdateNotes
2021-11-26 - release version 1.0.0
- 초기 버전 완성 및 배포
- 로그인 기능 
- 별점 기능 
- 식단 스크래핑
- 식단 정보 제공

2021-12-18 - release version 1.1.0
- 메인화면 폰트 수정
- 메인화면 Footer 추가

2022-01-05 - release version 1.1.1
- index.js 코드 리팩토링 
- 700 라인 코드 80 라인으로 축소
- 기존 페이지에서 가져오는 카테고리 데이터 변동에 따른 코드 수정량을 2라인으로 대폭 감소 

2022-02-01 - release version 1.1.2
- 식단이 일부 공백일 경우 스크래핑 후 처리 중 공백이 사라지는 버그 수정

2022-02-24 - release version 1.1.3
- 식단 전체가 공백일 경우 스크래핑 후 처리 로직 에러 수정

# Usage
- 페이지 접속 시 아람관 식단을 확인 할 수 있습니다
- 메뉴 클릭시 메뉴의 별점을 확인할 수 있습니다 
- 로그인 시 메뉴에 대한 별점을 남길 수 있습니다

# Directory Structure
```bash
📂/
├─__init__.py
├─chromedriver
├─db.py
├─get_data.py
├─get_auth.py
├─schema.sql
├─user.py
├─📂/static
│   ├─📂/static/css
│   │   ├─📂/static/css/error
│   │   │   └─error.css
│   │   ├─📂/static/css/member
│   │   │   ├─login.css
│   │   │   └─register.css
│   │   └─index.css
│   ├─📂/static/js
│   │   ├─📂/static/js/error
│   │   │   └─error.js
│   │   ├─📂/static/js/member
│   │   │   └─register.js
│   │   └─index.js
│   └─📂/static/images
│       ├─empty_star.png
│       ├─error.png
│       ├─favicon.ico
│       ├─full_star.png
│       ├─login.png
│       ├─logo.png
│       ├─logout.png
│       ├─x_icon.png
│       ├─뒤로가기.png
│       └─홈_로고.png
└─📂/templates
    ├─📂/templates/member
    │   ├─login.html
    │   └─register.html
    ├─📂/templates/error
    │   └─error.html
    └─index.html
```
    
# Requirements
