// 페이지가 로딩될 때 바로 실행할 함수들
$(document).ready(function () {
  const sessionExist = session_check(); // 세션체크 후
  setEventListener(sessionExist);
  get_daytable(); // 데이터 로딩 후
  event_modal(sessionExist); // 모달 이벤트 처리
});

const session_check = () => {
  let sessionExist;
  $.ajax({
    type: "POST",
    url: "/api/session_check",
    async: false,
    data: {},
    success: function (response) {
      if (response == "0") {
        // 세션 없음
        $("#login").append(
          '<a href="/member/login.html" id="login-button"><img src="/static/images/login.png" alt="Login"></a>'
        );
        sessionExist = 0;
      } else {
        // 세션 있음
        $("#login").append(
          '<a href="" id="logout-button"><img src="/static/images/logout.png" alt="Login"></a>'
        );
        sessionExist = 1;
      }
    },
  });

  return sessionExist;
};

const logout = () => {
  $.ajax({
    type: "POST",
    url: "/logout",
    async: true,
    data: {},
    success: function (answer) {
      if (answer == "1") {
        //로그아웃 성공시 새로고침
        location.reload();
      }
    },
  });
};

const setEventListener = (sessionExist) => {
  if (sessionExist == 1) {
    logoutbutton = document.querySelector("#logout-button");
    logoutbutton.addEventListener("click", () => {
      logout();
    });
  }
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
        $(".hash-tag2").append(`<h1>#매주 #일요일 #1시 #메뉴가 돌아온다!</h1>`);
      } else $(".hash-tag2").append(`<h1>#내일 #메뉴</h1>`);
      if (after_day === undefined) {
        $(".hash-tag3").append(`<h1>#매주 #일요일 #1시 #UPDATE FOR YOU👉</h1>`);
      } else $(".hash-tag3").append(`<h1>#모레 #는 #멀다</h1>`);

      /* 오늘메뉴 가져오기 */
      let morning_info = "";
      let lunch_info = "";
      let dinner_info = "";
      let A=B=C=T=0;

      // 아침
      morning_info = morning_info + "<td>";
      for (let i = 0; i < morning.length; i++) {
        if (this_day === morning[i][0]) {
          if (morning[i][1] === "none")
            morning_info =
              morning_info +
              '<span class="open_today">' +
              morning[i][2] +
              "</span></br>";
          else if (morning[i][1] === "A") {
            if (A==0) {
              A = 1;
              morning_info = morning_info + '<p class="course">A</p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open_today">' +
              morning[i][2] +
              "</span></br>";
          } else if (morning[i][1] === "B") {
            if (B == 0) {
              B = 1;
              morning_info = morning_info + '<p class="course">B</p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open_today">' +
              morning[i][2] +
              "</span></br>";
          } else if (morning[i][1] === "C") {
            if (C == 0) {
              C = 1;
              morning_info = morning_info + '<p class="course">C</p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open_today">' +
              morning[i][2] +
              "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              morning_info =
                morning_info + '<p class="course">테이크아웃</p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open_today">' +
              morning[i][2] +
              "</span>" +
              "</br>";
          }
        }
      }
      A=B=C=T=0;
      morning_info = morning_info + "</td>";
      morning_info = morning_info + "<td>";
      $("#morning").append(morning_info);

      // 점심
      lunch_info = lunch_info + "<td>";
      for (let i = 0; i < lunch.length; i++) {
        if (this_day === lunch[i][0]) {
          if (lunch[i][1] === "none")
            lunch_info =
              lunch_info +
              '<span class="open_today">' +
              lunch[i][2] +
              "</span></br>";
          else if (lunch[i][1] === "A") {
            if (A == 0) {
              A = 1;
              lunch_info = lunch_info + '<p class="course"> A </p></br>';
            }
            lunch_info =
              lunch_info +
              '<span class="open_today">' +
              lunch[i][2] +
              "</span></br>";
          } else if (lunch[i][1] === "B") {
            if (B == 1) {
              B = 1;
              lunch_info = lunch_info + '<p class="course"> B </p></br>';
            }
            lunch_info =
              lunch_info +
              '<span class="open_today">' +
              lunch[i][2] +
              "</span></br>";
          } else if (lunch[i][1] === "C") {
            if (C == 0) {
              C = 1;
              lunch_info = lunch_info + '<p class="course"> C </p></br>';
            }
            lunch_info =
              lunch_info +
              '<span class="open_today">' +
              lunch[i][2] +
              "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              lunch_info =
                lunch_info + '<p class="course"> 테이크아웃 </p></br>';
            }
            lunch_info =
              lunch_info +
              '<span class="open_today">' +
              lunch[i][2] +
              "</span></br>";
          }
        }
      }
      A=B=C=T=0;
      lunch_info = lunch_info + "</td>";
      lunch_info = lunch_info + "<td>";
      $("#lunch").append(lunch_info);

      // 저녁
      dinner_info = dinner_info + "<td>";
      for (let i = 0; i < dinner.length; i++) {
        if (this_day === dinner[i][0]) {
          if (dinner[i][1] === "none")
            dinner_info =
              dinner_info +
              '<span class="open_today">' +
              dinner[i][2] +
              "</span></br>";
          else if (dinner[i][1] === "A") {
            if (A == 0) {
              A = 1;
              dinner_info = dinner_info + '<p class="course"> A </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open_today">' +
              dinner[i][2] +
              "</span></br>";
          } else if (dinner[i][1] === "B") {
            if (B == 0) {
              B = 1;
              dinner_info = dinner_info + '<p class="course"> B </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open_today">' +
              dinner[i][2] +
              "</span></br>";
          } else if (dinner[i][1] === "C") {
            if (C == 0) {
              C = 1;
              dinner_info = dinner_info + '<p class="course"> C </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open_today">' +
              dinner[i][2] +
              "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              dinner_info =
                dinner_info + '<p class="course"> 테이크아웃 </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open_today">' +
              dinner[i][2] +
              "</span></br>";
          }
        }
      }
      A=B=C=T=0;
      dinner_info = dinner_info + "</td>";
      dinner_info = dinner_info + "<td>";
      $("#dinner").append(dinner_info);

      /* 내일 */
      morning_info = "";
      lunch_info = "";
      dinner_info = "";

       // 아침
      morning_info = morning_info + "<td>";
      for (let i = 0; i < morning.length; i++) {
        if (tomorrow_day === morning[i][0]) {
          if (morning[i][1] === "none")
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          else if (morning[i][1] === "A") {
            if (A == 0) {
              A = 1;
              morning_info = morning_info + '<p class="course"> A </p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          } else if (morning[i][1] === "B") {
            if (B == 0) {
              B = 1;
              morning_info = morning_info + '<p class="course"> B </p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          } else if (morning[i][1] === "C") {
            if (C == 0) {
              C = 1;
              morning_info = morning_info + '<p class="course"> C </p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              morning_info =
                morning_info + '<p class="course"> 테이크아웃 </p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          }
        }
      }
      A=B=C=T=0;
      morning_info = morning_info + "</td>";
      morning_info = morning_info + "<td>";
      $("#nextmorning").append(morning_info);

      // 점심
      lunch_info = lunch_info + "<td>";
      for (let i = 0; i < lunch.length; i++) {
        if (tomorrow_day === lunch[i][0]) {
          if (lunch[i][1] === "none")
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          else if (lunch[i][1] === "A") {
            if (A == 0) {
              A = 1;
              lunch_info = lunch_info + '<p class="course"> A </p></br>';
            }
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          } else if (lunch[i][1] === "B") {
            if (B == 0) {
              B = 1;
              lunch_info = lunch_info + '<p class="course"> B </p></br>';
            }
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          } else if (lunch[i][1] === "C") {
            if (C == 0) {
              C = 1;
              lunch_info = lunch_info + '<p class="course"> C </p></br>';
            }
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              lunch_info =
                lunch_info + '<p class="course"> 테이크아웃 </p></br>';
            }
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          }
        }
      }

      A=B=C=T=0;
      lunch_info = lunch_info + "</td>";
      lunch_info = lunch_info + "<td>";
      $("#nextlunch").append(lunch_info);

      // 저녁
      dinner_info = dinner_info + "<td>";
      for (let i = 0; i < dinner.length; i++) {
        if (tomorrow_day === dinner[i][0]) {
          if (dinner[i][1] === "none")
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          else if (dinner[i][1] === "A") {
            if (A == 0) {
              A = 1;
              dinner_info = dinner_info + '<p class="course"> A </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          } else if (dinner[i][1] === "B") {
            if (B == 0) {
              B = 1;
              dinner_info = dinner_info + '<p class="course"> B </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          } else if (dinner[i][1] === "C") {
            if (C == 0) {
              C = 1;
              dinner_info = dinner_info + '<p class="course"> C </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              dinner_info =
                dinner_info + '<p class="course"> 테이크아웃 </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          }
        }
      }
      A=B=C=T=0;
      dinner_info = dinner_info + "</td>";
      dinner_info = dinner_info + "<td>";
      $("#nextdinner").append(dinner_info);

      /* 모레 */
      morning_info = "";
      lunch_info = "";
      dinner_info = "";

      //아침
      morning_info = morning_info + "<td>";
      for (let i = 0; i < morning.length; i++) {
        if (after_day === morning[i][0]) {
          if (morning[i][1] === "none")
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          else if (morning[i][1] === "A") {
            if (A == 0) {
              A = 1;
              morning_info = morning_info + '<p class="course"> A </p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          } else if (morning[i][1] === "B") {
            if (B == 0) {
              B = 1;
              morning_info = morning_info + '<p class="course"> B </p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          } else if (morning[i][1] === "C") {
            if (C == 0) {
              C = 1;
              morning_info = morning_info + '<p class="course"> C </p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              morning_info =
                morning_info + '<p class="course"> 테이크아웃 </p></br>';
            }
            morning_info =
              morning_info +
              '<span class="open">' +
              morning[i][2] +
              "</span></br>";
          }
        }
      }
      A=B=C=T=0;
      morning_info = morning_info + "</td>";
      $("#doublenextmorning").append(morning_info);

      //점심
      lunch_info = lunch_info + "<td>";
      for (let i = 0; i < lunch.length; i++) {
        if (after_day === lunch[i][0]) {
          if (lunch[i][1] === "none")
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          else if (lunch[i][1] === "A") {
            if (A == 0) {
              A = 1;
              lunch_info = lunch_info + '<p class="course"> A </p></br>';
            }
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          } else if (lunch[i][1] === "B") {
            if (B == 0) {
              B = 1;
              lunch_info = lunch_info + '<p class="course"> B </p></br>';
            }
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          } else if (lunch[i][1] === "C") {
            if (C == 0) {
              C = 1;
              lunch_info = lunch_info + '<p class="course"> C </p></br>';
            }
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              lunch_info =
                lunch_info + '<p class="course"> 테이크아웃 </p></br>';
            }
            lunch_info =
              lunch_info + '<span class="open">' + lunch[i][2] + "</span></br>";
          }
        }
      }
      A=B=C=T=0;
      lunch_info = lunch_info + "</td>";
      $("#doublenextlunch").append(lunch_info);

      //저녁
      dinner_info = dinner_info + "<td>";
      for (let i = 0; i < dinner.length; i++) {
        if (after_day === dinner[i][0]) {
          if (dinner[i][1] === "none")
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          else if (dinner[i][1] === "A") {
            if (A == 0) {
              A = 1;
              dinner_info = dinner_info + '<p class="course"> A </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          } else if (dinner[i][1] === "B") {
            if (B == 0) {
              B = 1;
              dinner_info = dinner_info + '<p class="course"> B </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          } else if (dinner[i][1] === "C") {
            if (C == 0) {
              C = 1;
              dinner_info = dinner_info + '<p class="course"> C </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          } else {
            if (T == 0) {
              T = 1;
              dinner_info =
                dinner_info + '<p class="course"> 테이크아웃 </p></br>';
            }
            dinner_info =
              dinner_info +
              '<span class="open">' +
              dinner[i][2] +
              "</span></br>";
          }
        }
      }
      A=B=C=T=0;
      dinner_info = dinner_info + "</td>";
      $("#doublenextdinner").append(dinner_info);
    },
  });
};

// modal event
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
  for (let i = 0; i < open_today.length; i++) {   // today
    open_today[i].addEventListener("click", () => {
      modal.style.opacity = 1;
      modal.style.visibility = "visible";
      if(sessionExist == "1") {
        menu_evaluation.style.display = "block";
        modal_footer.style.display = "none";
      } else {
        menu_evaluation.style.display = "none";
      }

      name = set_modal_inner_header(open_today[i]);
    });
  }
  for (let i = 0; i < open_after_today.length; i++) {   // tomorrow, the day after tomorrow
    open_after_today[i].addEventListener("click", () => {
      modal.style.opacity = 1;
      modal.style.visibility = "visible";
      menu_evaluation.style.display = "none";
      if(sessionExist == "1") {
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
      for(let i = 0; i < 5; i++){
        score[i] = 0;
      }
    });
  }

  // submit modal
  submit.addEventListener("click", () => {
    // modifing css
    let score_result = 0;
    modal.style.opacity = 0;
    modal.style.visibility = "hidden";

    // initializing star
    clear_star();
    // add up the scores and initializing
    for (let i = 0; i < score.length; i++) {
      score_result += score[i];
      score[i] = 0;
    }
    // send api, 별점주기
    if (score_result > 0) {
      $.ajax({
        type: "POST",
        url: "/api/score",
        data: { menu_name: name, menu_score: score_result },
        success: function (response) {
          alert(response["msg"]);
        },
      });
    }
  });
};

// 별점 이미지 초기화
const clear_star = () => {
  const star = document.querySelectorAll(".star img");
  const empty_star = "/static/images/empty_star.png";

  for (let i = 0; i < 5; i++) {
    star[i].src = empty_star;
  }
};

// 모달 내부 헤더 부분
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

// 모달 내부 내용 부분
const set_modal_inner_content = (sessionExist) => {
  const score = [0, 0, 0, 0, 0];
  const modal_footer = document.querySelector(".modal-footer");
  const login_link = document.querySelector(".login_link");
  const star = document.querySelectorAll(".star img");

  //세션 존재하면 별점 기능 사용, 없으면 로그인 링크 사용
  if (sessionExist == 1) {
    modal_footer.style.display = "none";

    for (let i = 0; i < 5; i++) {
      star[i].addEventListener("click", () => {
        for (let j = 0; j < 5; j++) {
          if (j <= i && score[j] == 0) {
            star[j].src = "/static/images/full_star.png";
            score[j] = 1;
          }
          if (j > i && score[j] == 1) {
            star[j].src = "/static/images/empty_star.png";
            score[j] = 0;
          }
        }
      });
    }
  } else {
    modal_footer.style.display = "inline-block";
    login_link.style.display="block";
  }
  return score
}