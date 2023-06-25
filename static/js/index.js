// DOM 생성후 바로 실행할 함수들

$(document).ready(function () {
  const errorStatus = 1; // 서버 에러시 상태코드 0 == 에러 1 == 정상
  if(errorStatus) {
    const sessionExist = session_check(); // 세션체크 후
    get_daytable(); // 데이터 로딩 후
    event_modal(sessionExist); // 모달 이벤트 처리
    get_views();
    set_cookie();
  }
  else{
    console.log("");
  }
});

const get_views = () => {
  $.ajax({
    type: "GET",
    url: "/api/views",
    async: false,
    data: {},
    success: function (response) {
      $(".views").append(`Total Views ${response["views"][0]["views"]}`)
    },
  });
}

const set_cookie = () => {
  
}

const session_check = () => {
  let sessionExist;
  $.ajax({
    type: "POST",
    url: "/api/session_check",
    async: false, // 세션 체크 후 반환되는 값에 따라 페이지 로딩을 달리해야하므로 동기식으로 처리
    data: {},
    success: function (response) {
      // alert(response)
      if (response == "0") {
        // 세션 없음
        $("#login").append(
          '<a href="/member/login.html" class="login-button" id="login-button">로그인</a>'
        );
        sessionExist = 0;
      } else {
        // 세션 있음
        $("#login").append(
          '<a href="" class="login-button" id="logout-button">로그아웃</a>'
        );
        sessionExist = 1;
        logoutbutton = document.querySelector("#logout-button");
        logoutbutton.addEventListener("click", () => {
          logout();
        });
      }
    },
  });

  return sessionExist;
};

const logout = () => {
  $.ajax({
    type: "POST",
    url: "/logout",
    async: false, //비동기로 하니 오히려 더 잘된다!
    data: {},
    success: function (answer) {
      if (answer == "1") {
        //로그아웃 성공시 새로고침
        location.reload();
      }
    },
  });
};

// 메뉴 테이블에 메뉴들을 받아오는 함수
const get_daytable = () => {
  $.ajax({
    type: "GET",
    url: "/api/list",
    async: false,
    data: {},
    success: function (response) {
      // 오늘, 내일, 모레 날짜 생성
      const date = new Date();
      const day = new Date();
      const tomorrow = new Date(date.setDate(date.getDate() + 1));
      const after_tomorrow = new Date(date.setDate(date.getDate() + 1));
      // 날짜 가공
      const todays =
        day.getFullYear() +
        "-" +
        ("0" + (day.getMonth() + 1)).slice(-2) +
        "-" +
        ("0" + day.getDate()).slice(-2);
      const tomorrows =
        tomorrow.getFullYear() +
        "-" +
        ("0" + (tomorrow.getMonth() + 1)).slice(-2) +
        "-" +
        ("0" + tomorrow.getDate()).slice(-2);
      const after_tomorrows =
        after_tomorrow.getFullYear() +
        "-" +
        ("0" + (after_tomorrow.getMonth() + 1)).slice(-2) +
        "-" +
        ("0" + after_tomorrow.getDate()).slice(-2);
      let this_day;
      let tomorrow_day;
      let after_day;

      // 서버로부터 전달 받은 날짜들..
      const days = response["days"];
      const morning = response["morning"];
      const lunch = response["lunch"];
      const dinner = response["dinner"];
      // 오늘, 내일, 모레 날짜를 서버에서 가져온 날짜와 비교.
      for (let i = 0; i < days.length; i++) {
        if (days[i][1] === todays) {
          this_day = days[i][0];
        }
        if (days[i][1] === tomorrows) {
          tomorrow_day = days[i][0];
        }
        if (days[i][1] === after_tomorrows) {
          after_day = days[i][0];
        }
      }

      // 메뉴가 없을 때(해당 날짜가 없을 때) 해시 태그와 있을 때 해시 태그
      if (this_day === undefined) {
        $(".hash-tag1").append(`<h1>#곧 #1시에 #UPDATE!! #COMMING SOON!</h1>`);
      } else $(".hash-tag1").append(`<h1>#오늘 #과제는 #내일하자👊</h1>`);
      if (tomorrow_day === undefined) {
        $(".hash-tag2").append(`<h1>#매주 #월요일 #1시 #메뉴가 돌아온다!</h1>`);
      } else $(".hash-tag2").append(`<h1>#내일 #부터 #다이어트 #할거임!</h1>`);
      if (after_day === undefined) {
        $(".hash-tag3").append(`<h1>#매주 #월요일 #1시 #UPDATE FOR YOU👉</h1>`);
      } else $(".hash-tag3").append(`<h1>#모레 #는 #맛있을까?</h1>`);

      /* 오늘메뉴 가져오기 */
      let meal_info = "";

      meal_info = edit_menu(morning, this_day)
      $("#morning").append(meal_info);

      // 점심
      meal_info = edit_menu(lunch, this_day)
      $("#lunch").append(meal_info);
      
      // 저녁
      meal_info = edit_menu(dinner, this_day)
      $("#dinner").append(meal_info);

      /* 내일 */
      // 아침
      meal_info = edit_menu(morning, tomorrow_day)
      $("#next-morning").append(meal_info);

      // 점심
      meal_info = edit_menu(lunch, tomorrow_day)
      $("#next-lunch").append(meal_info);

      // 저녁
      meal_info = edit_menu(dinner, tomorrow_day)
      $("#next-dinner").append(meal_info);

      /* 모레 */
      // 아침
      meal_info = edit_menu(morning, after_day)
      $("#double-next-morning").append(meal_info);

      // 점심
      meal_info = edit_menu(lunch, after_day)
      $("#double-next-lunch").append(meal_info);

      // 저녁
      meal_info = edit_menu(dinner, after_day)
      $("#double-next-dinner").append(meal_info);
    }
  });
};

// 메뉴 출력 함수
const edit_menu = (meal, this_day) => {
  let menu_info = "";
  const courseList = ['A', 'B', 'C', '테이크아웃', 'T/O', '일품', '베이커리', '한식', '죽', '죽식', 'A코스', 'B코스', 'C코스', 'A코스/한식', 'B코스/베이커리', 'C코스/죽', '◆공지◆', 'B코스/일품', '공지', 'A코스 /한식', 'B코스 /베이커리', 'B코스 /일품'];
  let courseMode = new Array(courseList.length).fill(0);

  menu_info = menu_info + "<td>";
  for (let i = 0; i < meal.length; i++) {
    if (this_day === meal[i][0]) {
      if (courseList.indexOf(meal[i][1]) !== -1) {
        const idx = courseList.indexOf(meal[i][1]);
        if (courseMode[idx] == 0) {
          courseMode[idx] = 1;
          menu_info = menu_info + '<p class="course">' + meal[i][1] +'</p></br>';
        }
        if (meal[i][3] == null) {
          menu_info =
          menu_info +
          '<span class="open_today">' +
          meal[i][2] + 
          "</span> </br>";
        } else {
          menu_info =
          menu_info +
          '<span class="open_today">' +
          meal[i][2] + 
          '</span><span class="score_menu"> ' +
          meal[i][3] +
          "</span></br>";
        }
      } 
      if (meal[i][1] === "none") { // none이면 
        menu_info =
        menu_info +
        '<span class="open_today">' +
        meal[i][2] +
        "</span></br>";
      }
    }
  }
  menu_info = menu_info + "</td>";
  menu_info = menu_info + "<td>";
  return menu_info;
}


// modal event = open, close, score, submit
const event_modal = (sessionExist) => {
  const modal = document.querySelector("#modal");
  const open_today = document.querySelectorAll(".open_today");
  const open_after_today = document.querySelectorAll(".open");
  const close = document.querySelectorAll(".close-btn");
  const submit = document.querySelector(".submit");
  const menu_evaluation = document.querySelector(".menu-evaluation");
  const modal_footer = document.querySelector(".modal-footer");
  let name = "";

  // open event
  for (let i = 0; i < open_today.length; i++) {
    // today
    open_today[i].addEventListener("click", () => {
      modal.style.opacity = 1;
      modal.style.visibility = "visible";
      if (sessionExist == "1") {
        menu_evaluation.style.display = "block";
        modal_footer.style.display = "none";
      } else {
        menu_evaluation.style.display = "none";
      }
      name = set_modal_inner_header(open_today[i]);
    });
  }
  for (let i = 0; i < open_after_today.length; i++) {
    // tomorrow, the day after tomorrow
    open_after_today[i].addEventListener("click", () => {
      modal.style.opacity = 1;
      modal.style.visibility = "visible";
      menu_evaluation.style.display = "none";
      if (sessionExist == "1") {
        modal_footer.style.display = "inline-block";
        menu_evaluation.style.display = "none";
      }
      name = set_modal_inner_header(open_after_today[i]);
    });
  }

  // score event
  const score = set_modal_inner_content(sessionExist);

  // close event
  for (let i = 0; i < close.length; i++) {
    close[i].addEventListener("click", () => {
      modal.style.opacity = 0;
      modal.style.visibility = "hidden";
      // initializing star and score
      clear_star();
      for (let i = 0; i < 5; i++) {
        score[i] = 0;
      }
    });
  }

  // submit event
  submit.addEventListener("click", () => {
    // modifing css
    let score_result = 0;
    modal.style.opacity = 0;
    modal.style.visibility = "hidden";

    // initializing star
    clear_star();
    // add up the scores and initialize score
    for (let i = 0; i < score.length; i++) {
      score_result += score[i];
      score[i] = 0;
    }
    // send api, 별점주기
    if (score_result > 0) {
      $.ajax({
        type: "POST", // post 방식 
        url: "/api/score", // url
        data: { menu_name: name, menu_score: score_result }, //데이터 전송
        success: function (response) { // 성공하면
          alert(response["msg"]); // 메세지 출력
        },
      });
    }
  });
};

// initialize star images
const clear_star = () => {
  const star = document.querySelectorAll(".star img");
  const empty_star = "/static/images/empty_star.png";

  for (let i = 0; i < 5; i++) {
    star[i].src = empty_star;
  }
};

// set modal inner header
const set_modal_inner_header = (open_today) => {
  let name = "";
  $(".menu-name").empty();
  temp_html = `
              <a>${open_today.innerHTML}</a>                        
              `;
  $(".menu-name").append(temp_html);

  // queryselector가 &를 가져올 때 &amp;로 가져오기 때문에 &로 변환해줘야 한다.
  name = open_today.innerHTML.replace("&amp;", "&");
  // DB에서 누적 별점 가져오기
  $.ajax({
    type: "POST",
    url: "/api/menu_score",
    data: { menu_name: name },
    success: function (response) {
      $(".menu-score").empty();
      const score = response["score"];
      for (let i = 1; i <= 5; i++) {
        if (i <= score) $(".menu-score").append(`★`);
        else $(".menu-score").append(`☆`);
      }
    },
  });
  return name;
};

// set modal inner content
const set_modal_inner_content = (sessionExist) => {
  const score = [0, 0, 0, 0, 0];
  const modal_footer = document.querySelector(".modal-footer");
  const login_link = document.querySelector(".login-link");
  const star = document.querySelectorAll(".star img");

  //세션 존재하면 별점 기능 사용
  if (sessionExist == 1) {
    modal_footer.style.display = "none"; // .modal-footer css none으로 설정

    for (let i = 0; i < 5; i++) {
      // for 문으로 5개 별의 클릭 이벤트를 설정한다.
      star[i].addEventListener("click", () => {
        for (let j = 0; j < 5; j++) {
          // 바뀌어야 하는 부분만 바뀌도록 score 배열을 이용한다. score 배열의 값이 1이면, 꽉찬 별, 0이면 빈 별 이미지를 의미한다.
          if (j <= i && score[j] == 0) {
            // score 배열의 클릭한 별의 인덱스(i)까지 0이면 1로 설정하고, star[j] img 태그의 src를 꽉찬 별로 설정한다.
            star[j].src = "/static/images/full_star.png";
            score[j] = 1;
          }
          if (j > i && score[j] == 1) {
            // score 배열의 클릭한 별의 인덱스(i)를 넘어가서 1이면 0으로 설정하고, star[j] img 태그의 src를 빈 별로 설정한다.
            star[j].src = "/static/images/empty_star.png";
            score[j] = 0;
          }
        }
      });
    }
  } else {
    // 세션이 존재하지 않으면 로그인 링크 사용
    modal_footer.style.display = "inline-block"; // .modal-footer css inline-block으로 설정
    login_link.style.display = "block"; // .login-link css block으로 설정
  }
  return score; // score 배열 리턴
};
